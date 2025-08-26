import os
import stripe
import json
import uuid
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, send_file, jsonify, current_app, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import func, desc, asc, or_

from app import db, mail, cache, limiter
from models import (Admin, Service, Order, ContactMessage, Testimonial, FAQ, 
                   Portfolio, DiscountCode, Referral, OrderTracking, Template,
                   NewsletterSubscriber, LiveChat, ChatMessage, Analytics, OrderDiscount)
from forms import (OrderForm, ContactForm, AdminLoginForm, OrderStatusForm,
                  TestimonialForm, FAQForm, DiscountCodeForm, ReferralForm,
                  NewsletterForm, LiveChatForm, AdminResponseForm, DiscountApplicationForm)
from utils import (track_event, validate_discount_code, apply_discount_to_order,
                  save_uploaded_file, calculate_estimated_delivery, generate_referral_code,
                  generate_session_id, format_price, get_service_features_list,
                  log_user_action, send_admin_notification_email)

def register_enhanced_routes(app):
    
    # Configure Stripe
    @app.before_request
    def set_stripe_key():
        stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
        
        # Set user session for analytics
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
    
    # Enhanced Home Page with testimonials, portfolio, and features
    @app.route('/')
    @cache.cached(timeout=300)  # Cache for 5 minutes
    def index():
        track_event('page_view', {'page': 'home'})
        
        services = Service.query.filter_by(active=True).all()
        testimonials = Testimonial.query.filter_by(featured=True, approved=True).limit(6).all()
        portfolio_items = Portfolio.query.filter_by(featured=True, active=True).limit(4).all()
        faqs = FAQ.query.filter_by(active=True).order_by(FAQ.order_index.asc()).limit(5).all()
        
        return render_template('index.html', 
                             services=services, 
                             testimonials=testimonials,
                             portfolio_items=portfolio_items,
                             faqs=faqs)
    
    # Testimonials Page
    @app.route('/testimonials')
    @cache.cached(timeout=600)  # Cache for 10 minutes
    def testimonials():
        track_event('page_view', {'page': 'testimonials'})
        
        page = request.args.get('page', 1, type=int)
        industry_filter = request.args.get('industry', 'all')
        rating_filter = request.args.get('rating', 'all', type=str)
        
        query = Testimonial.query.filter_by(approved=True)
        
        if industry_filter != 'all':
            query = query.filter(Testimonial.industry == industry_filter)
        if rating_filter != 'all':
            query = query.filter(Testimonial.rating >= int(rating_filter))
        
        testimonials = query.order_by(desc(Testimonial.created_at)).paginate(
            page=page, per_page=12, error_out=False
        )
        
        # Get unique industries for filter
        industries = db.session.query(Testimonial.industry).distinct().filter(
            Testimonial.industry.isnot(None), Testimonial.approved == True
        ).all()
        industries = [i[0] for i in industries if i[0]]
        
        return render_template('testimonials.html', 
                             testimonials=testimonials,
                             industries=industries,
                             current_industry=industry_filter,
                             current_rating=rating_filter)
    
    # Portfolio Showcase
    @app.route('/portfolio')
    @cache.cached(timeout=600)
    def portfolio():
        track_event('page_view', {'page': 'portfolio'})
        
        page = request.args.get('page', 1, type=int)
        industry_filter = request.args.get('industry', 'all')
        level_filter = request.args.get('level', 'all')
        
        query = Portfolio.query.filter_by(active=True)
        
        if industry_filter != 'all':
            query = query.filter(Portfolio.industry == industry_filter)
        if level_filter != 'all':
            query = query.filter(Portfolio.job_level == level_filter)
        
        portfolio_items = query.order_by(desc(Portfolio.created_at)).paginate(
            page=page, per_page=9, error_out=False
        )
        
        # Get filter options
        industries = db.session.query(Portfolio.industry).distinct().filter(
            Portfolio.industry.isnot(None), Portfolio.active == True
        ).all()
        industries = [i[0] for i in industries if i[0]]
        
        levels = ['entry', 'mid', 'senior', 'executive']
        
        return render_template('portfolio.html',
                             portfolio_items=portfolio_items,
                             industries=industries,
                             levels=levels,
                             current_industry=industry_filter,
                             current_level=level_filter)
    
    # FAQ Page
    @app.route('/faq')
    @cache.cached(timeout=600)
    def faq():
        track_event('page_view', {'page': 'faq'})
        
        category_filter = request.args.get('category', 'all')
        
        query = FAQ.query.filter_by(active=True)
        if category_filter != 'all':
            query = query.filter(FAQ.category == category_filter)
            
        faqs = query.order_by(FAQ.order_index.asc(), FAQ.created_at.desc()).all()
        
        # Group FAQs by category
        faq_categories = {}
        for faq_item in faqs:
            if faq_item.category not in faq_categories:
                faq_categories[faq_item.category] = []
            faq_categories[faq_item.category].append(faq_item)
        
        categories = ['general', 'pricing', 'process', 'delivery', 'revisions']
        
        return render_template('faq.html',
                             faq_categories=faq_categories,
                             categories=categories,
                             current_category=category_filter)
    
    # Enhanced Order Form with discount codes
    @app.route('/order')
    @limiter.limit("5 per minute")
    def order():
        track_event('page_view', {'page': 'order'})
        
        form = OrderForm()
        discount_form = DiscountApplicationForm()
        services = Service.query.filter_by(active=True).all()
        form.service_id.choices = [(s.id, s.name) for s in services]
        
        # Check for referral code in URL
        referral_code = request.args.get('ref')
        discount_applied = session.get('discount_applied')
        
        return render_template('order.html', 
                             form=form, 
                             discount_form=discount_form,
                             services=services,
                             referral_code=referral_code,
                             discount_applied=discount_applied)
    
    # Apply Discount Code
    @app.route('/apply-discount', methods=['POST'])
    @limiter.limit("10 per minute")
    def apply_discount():
        form = DiscountApplicationForm()
        
        if form.validate_on_submit():
            service_id = request.form.get('service_id', type=int)
            service_tier = request.form.get('service_tier')
            
            if not service_id or not service_tier:
                return jsonify({'success': False, 'message': 'Please select a service and tier first'})
            
            service = Service.query.get(service_id)
            if not service:
                return jsonify({'success': False, 'message': 'Invalid service selected'})
            
            # Get original price
            tier_prices = {
                'basic': service.price_basic,
                'standard': service.price_standard,
                'premium': service.price_premium
            }
            original_amount = tier_prices.get(service_tier)
            
            # Validate discount
            discount_info, error = validate_discount_code(form.discount_code.data, original_amount)
            
            if error:
                return jsonify({'success': False, 'message': error})
            
            # Store discount in session
            session['discount_applied'] = {
                'code': form.discount_code.data.upper(),
                'original_amount': original_amount,
                'discount_amount': discount_info['discount_amount'],
                'final_amount': discount_info['final_amount']
            }
            
            track_event('discount_applied', {'code': form.discount_code.data})
            
            return jsonify({
                'success': True, 
                'message': 'Discount applied successfully!',
                'discount_amount': discount_info['discount_amount'],
                'final_amount': discount_info['final_amount']
            })
        
        return jsonify({'success': False, 'message': 'Invalid discount code format'})
    
    # Enhanced Order Submission
    @app.route('/submit-order', methods=['POST'])
    @limiter.limit("3 per minute")
    def submit_order():
        form = OrderForm()
        services = Service.query.filter_by(active=True).all()
        form.service_id.choices = [(s.id, s.name) for s in services]
        
        if form.validate_on_submit():
            track_event('order_started', {
                'service_id': form.service_id.data,
                'service_tier': form.service_tier.data
            })
            
            # Get selected service
            service = Service.query.get(form.service_id.data)
            if not service:
                flash('Invalid service selected.', 'error')
                return render_template('order.html', form=form, services=services)
            
            # Calculate total amount
            tier_prices = {
                'basic': service.price_basic,
                'standard': service.price_standard,
                'premium': service.price_premium
            }
            original_amount = tier_prices.get(form.service_tier.data)
            final_amount = original_amount
            
            # Create order
            order = Order(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                service_id=form.service_id.data,
                service_tier=form.service_tier.data,
                total_amount=final_amount,
                current_position=form.current_position.data,
                target_position=form.target_position.data,
                industry=form.industry.data,
                experience_years=form.experience_years.data,
                career_goals=form.career_goals.data,
                special_requirements=form.special_requirements.data
            )
            
            # Handle file uploads
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            if form.current_resume.data:
                filename = save_uploaded_file(form.current_resume.data, upload_folder, "resume")
                order.uploaded_resume_path = filename
            
            if form.cover_letter.data:
                filename = save_uploaded_file(form.cover_letter.data, upload_folder, "cover")
                order.uploaded_cover_letter_path = filename
            
            if form.job_description.data:
                filename = save_uploaded_file(form.job_description.data, upload_folder, "job")
                order.uploaded_job_description_path = filename
            
            db.session.add(order)
            db.session.commit()
            
            # Apply discount if exists
            discount_applied = session.get('discount_applied')
            if discount_applied:
                discount_info, _ = validate_discount_code(discount_applied['code'], original_amount)
                if discount_info:
                    apply_discount_to_order(order, discount_info)
                    # Clear discount from session
                    session.pop('discount_applied', None)
            
            # Create initial tracking entry
            tracking = OrderTracking(
                order_id=order.id,
                status='pending',
                description='Order received and awaiting payment',
                created_by='system'
            )
            db.session.add(tracking)
            db.session.commit()
            
            # Send confirmation email
            try:
                send_order_confirmation_email(order)
            except Exception as e:
                current_app.logger.error(f"Failed to send confirmation email: {e}")
            
            track_event('order_created', {'order_id': order.id})
            
            # Redirect to payment
            return redirect(url_for('create_checkout_session', order_id=order.id))
        
        return render_template('order.html', form=form, services=services)
    
    # Order Tracking for Customers
    @app.route('/track-order')
    def track_order():
        order_id = request.args.get('order_id')
        email = request.args.get('email')
        
        if not order_id or not email:
            return render_template('track_order.html')
        
        order = Order.query.filter_by(id=order_id, email=email).first()
        if not order:
            flash('Order not found. Please check your order ID and email.', 'error')
            return render_template('track_order.html')
        
        tracking_updates = OrderTracking.query.filter_by(order_id=order.id).order_by(
            OrderTracking.created_at.desc()).all()
        
        track_event('order_tracked', {'order_id': order.id})
        
        return render_template('track_order.html', order=order, tracking_updates=tracking_updates)
    
    # Referral System
    @app.route('/refer', methods=['GET', 'POST'])
    def refer_friend():
        form = ReferralForm()
        
        if form.validate_on_submit():
            # Check if referral already exists
            existing = Referral.query.filter_by(
                referrer_email=form.referrer_email.data,
                referred_email=form.referred_email.data
            ).first()
            
            if existing:
                flash('You have already referred this person!', 'warning')
                return render_template('referral.html', form=form)
            
            # Create referral
            referral_code = generate_referral_code()
            referral = Referral(
                referrer_email=form.referrer_email.data,
                referrer_name=form.referrer_name.data,
                referred_email=form.referred_email.data,
                referred_name=form.referred_name.data,
                referral_code=referral_code,
                reward_amount=25.0  # $25 reward
            )
            
            db.session.add(referral)
            db.session.commit()
            
            # Send referral emails
            try:
                send_referral_emails(referral)
                flash('Referral sent successfully! Your friend will receive an email with your special offer.', 'success')
                track_event('referral_sent', {'referral_code': referral_code})
            except Exception as e:
                current_app.logger.error(f"Referral email error: {e}")
                flash('Referral created but email could not be sent. Please contact support.', 'warning')
            
            return redirect(url_for('refer_friend'))
        
        return render_template('referral.html', form=form)
    
    # Newsletter Subscription
    @app.route('/newsletter-signup', methods=['POST'])
    @limiter.limit("5 per hour")
    def newsletter_signup():
        form = NewsletterForm()
        
        if form.validate_on_submit():
            existing = NewsletterSubscriber.query.filter_by(email=form.email.data).first()
            
            if existing:
                if not existing.active:
                    existing.active = True
                    db.session.commit()
                    flash('Welcome back! You have been re-subscribed to our newsletter.', 'success')
                else:
                    flash('You are already subscribed to our newsletter!', 'info')
            else:
                subscriber = NewsletterSubscriber(
                    email=form.email.data,
                    name=form.name.data
                )
                db.session.add(subscriber)
                db.session.commit()
                
                # Send welcome email
                try:
                    send_newsletter_welcome_email(subscriber)
                except Exception as e:
                    current_app.logger.error(f"Newsletter welcome email error: {e}")
                
                flash('Thank you for subscribing! Check your email for a welcome message.', 'success')
                track_event('newsletter_signup', {'email': form.email.data})
        
        return redirect(request.referrer or url_for('index'))
    
    # Live Chat System
    @app.route('/chat')
    def live_chat():
        if not current_app.config.get('ENABLE_LIVE_CHAT', False):
            flash('Live chat is currently unavailable.', 'info')
            return redirect(url_for('contact'))
        
        session_id = session.get('chat_session_id')
        if not session_id:
            session_id = generate_session_id()
            session['chat_session_id'] = session_id
            
            # Create new chat session
            chat = LiveChat(session_id=session_id)
            db.session.add(chat)
            db.session.commit()
        
        chat = LiveChat.query.filter_by(session_id=session_id).first()
        messages = ChatMessage.query.filter_by(chat_id=chat.id).order_by(
            ChatMessage.created_at.asc()).all() if chat else []
        
        return render_template('live_chat.html', chat=chat, messages=messages)
    
    # Templates Download
    @app.route('/templates')
    @cache.cached(timeout=600)
    def templates():
        category_filter = request.args.get('category', 'all')
        industry_filter = request.args.get('industry', 'all')
        
        query = Template.query.filter_by(active=True)
        
        if category_filter != 'all':
            query = query.filter(Template.category == category_filter)
        if industry_filter != 'all':
            query = query.filter(Template.industry == industry_filter)
        
        templates = query.order_by(desc(Template.created_at)).all()
        
        # Get filter options
        categories = ['resume', 'cover_letter', 'linkedin']
        industries = db.session.query(Template.industry).distinct().filter(
            Template.industry.isnot(None), Template.active == True
        ).all()
        industries = [i[0] for i in industries if i[0]]
        
        track_event('templates_viewed')
        
        return render_template('templates.html',
                             templates=templates,
                             categories=categories,
                             industries=industries,
                             current_category=category_filter,
                             current_industry=industry_filter)
    
    # Download Template
    @app.route('/download-template/<int:template_id>')
    @limiter.limit("10 per hour")
    def download_template(template_id):
        template = Template.query.get_or_404(template_id)
        
        if not template.active:
            abort(404)
        
        if template.premium_only:
            # Check if user has premium access (implement your logic here)
            flash('This template is only available for premium customers.', 'warning')
            return redirect(url_for('templates'))
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'templates', template.file_path)
        
        if not os.path.exists(file_path):
            flash('Template file not found.', 'error')
            return redirect(url_for('templates'))
        
        # Update download count
        template.download_count += 1
        db.session.commit()
        
        track_event('template_downloaded', {'template_id': template_id})
        
        return send_file(file_path, as_attachment=True, download_name=f"{template.name}.{template.file_path.split('.')[-1]}")
    
    # Keep all existing routes from original routes.py
    # (Payment processing, admin routes, etc. - I'll add these in the next section)
    
    # ... [Continue with existing payment and admin routes]
    
    return app

# Email helper functions
def send_order_confirmation_email(order):
    """Send enhanced order confirmation email"""
    if not mail:
        return
    
    estimated_delivery = calculate_estimated_delivery(order.service_tier)
    
    msg = Message(
        subject=f'Order Confirmation #{order.id} - {order.service.name}',
        recipients=[order.email]
    )
    
    msg.html = render_template('emails/order_confirmation.html', 
                              order=order, 
                              estimated_delivery=estimated_delivery)
    
    msg.body = f"""
Dear {order.full_name},

Thank you for choosing CreateProResume! We have received your order for {order.service.name} ({order.service_tier.title()} package).

Order Details:
- Order ID: #{order.id}
- Service: {order.service.name} - {order.service_tier.title()}
- Total Amount: ${order.total_amount:.2f}
- Target Position: {order.target_position}
- Estimated Delivery: {estimated_delivery.strftime('%B %d, %Y')}

Your order is currently pending payment. Once payment is completed, our professional writers will begin working on your resume.

You can track your order progress at: {url_for('track_order', order_id=order.id, email=order.email, _external=True)}

Best regards,
The CreateProResume Team
"""
    
    mail.send(msg)

def send_referral_emails(referral):
    """Send referral emails to both referrer and referred person"""
    if not mail:
        return
    
    # Email to referred person
    referred_msg = Message(
        subject=f'{referral.referrer_name} referred you to CreateProResume - Get $25 Off!',
        recipients=[referral.referred_email]
    )
    
    referred_msg.body = f"""
Hi {referral.referred_name or 'there'}!

Great news! {referral.referrer_name} has referred you to CreateProResume and you'll receive $25 off your first order!

Use referral code: {referral.referral_code}

CreateProResume offers professional resume writing services that help you land your dream job. Our expert writers create ATS-optimized resumes that get noticed by employers.

Ready to get started? Visit: {url_for('order', ref=referral.referral_code, _external=True)}

This offer is valid for 30 days from today.

Best regards,
The CreateProResume Team
"""
    
    # Email to referrer
    referrer_msg = Message(
        subject='Thank you for referring a friend to CreateProResume!',
        recipients=[referral.referrer_email]
    )
    
    referrer_msg.body = f"""
Hi {referral.referrer_name}!

Thank you for referring {referral.referred_name} to CreateProResume! 

We've sent them a special offer for $25 off their first order. When they complete their order using referral code {referral.referral_code}, you'll receive a $25 credit that can be used towards your next order.

Keep spreading the word - there's no limit to how many friends you can refer!

Best regards,
The CreateProResume Team
"""
    
    mail.send(referred_msg)
    mail.send(referrer_msg)

def send_newsletter_welcome_email(subscriber):
    """Send welcome email to newsletter subscriber"""
    if not mail:
        return
    
    msg = Message(
        subject='Welcome to CreateProResume Newsletter!',
        recipients=[subscriber.email]
    )
    
    msg.body = f"""
Hi {subscriber.name or 'there'}!

Welcome to the CreateProResume newsletter! You'll now receive:

• Career tips and job search strategies
• Resume writing best practices  
• Industry insights and trends
• Exclusive offers and discounts
• Success stories from our clients

As a welcome gift, here's a 10% discount code for your first order: WELCOME10

Ready to transform your career? Visit: {url_for('index', _external=True)}

Best regards,
The CreateProResume Team

P.S. You can unsubscribe at any time by clicking the link in our emails.
"""
    
    mail.send(msg)