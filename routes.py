import os
import logging
import stripe
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from urllib.parse import urljoin

from app import db, mail
from models import User, Order, ContactMessage, Admin, ReferralReward
from forms import LoginForm, RegisterForm, OrderForm, ContactForm, AdminOrderUpdateForm
from utils import allowed_file, calculate_referral_discount, send_email_notification

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Blueprint definitions
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
services_bp = Blueprint('services', __name__)
dashboard_bp = Blueprint('dashboard', __name__)
admin_bp = Blueprint('admin', __name__)
referral_bp = Blueprint('referral', __name__)

# Get domain for Stripe redirects
def get_domain():
    if os.environ.get('REPLIT_DEPLOYMENT'):
        return os.environ.get('REPLIT_DEV_DOMAIN')
    return request.host

# Main routes
@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        
        # Send notification email
        send_email_notification('contact', message.email, message.name)
        
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.customer' if not current_user.is_admin() else 'admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.customer' if not user.is_admin() else 'admin.dashboard'))
        flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.customer'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html', form=form)
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
            return render_template('auth/register.html', form=form)
        
        # Check referral code
        referrer = None
        if form.referral_code.data:
            referrer = User.query.filter_by(referral_code=form.referral_code.data).first()
            if not referrer:
                flash('Invalid referral code.', 'warning')
                return render_template('auth/register.html', form=form)
        
        # Create user
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            referred_by=referrer.id if referrer else None
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# Services routes
@services_bp.route('/pricing')
def pricing():
    return render_template('services/pricing.html')

@services_bp.route('/order/<service_type>')
@login_required
def order(service_type):
    pricing = {
        'basic': 99,
        'standard': 199,
        'premium': 299
    }
    
    if service_type not in pricing:
        flash('Invalid service type.', 'danger')
        return redirect(url_for('services.pricing'))
    
    form = OrderForm()
    form.service_type.data = service_type
    
    # Pre-fill form with user data
    if current_user:
        form.full_name.data = current_user.get_full_name()
        form.email.data = current_user.email
    
    return render_template('services/order.html', form=form, service_type=service_type, price=pricing[service_type])

@services_bp.route('/submit_order', methods=['POST'])
@login_required
def submit_order():
    form = OrderForm()
    
    if form.validate_on_submit():
        service_type = form.service_type.data
        pricing = {'basic': 99, 'standard': 199, 'premium': 299}
        
        if service_type not in pricing:
            flash('Invalid service type.', 'danger')
            return redirect(url_for('services.pricing'))
        
        price = pricing[service_type]
        
        # Apply referral discount
        referral_discount = 0
        referrer = None
        if form.referral_code.data:
            referrer = User.query.filter_by(referral_code=form.referral_code.data).first()
            if referrer and referrer.id != current_user.id:
                referral_discount = calculate_referral_discount(price)
                price -= referral_discount
        
        # Create order
        order = Order(
            user_id=current_user.id,
            service_type=service_type,
            price=price,
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            target_position=form.target_position.data,
            industry=form.industry.data,
            experience_level=form.experience_level.data,
            special_requirements=form.special_requirements.data,
            referral_used=form.referral_code.data if referrer else None,
            referral_discount=referral_discount
        )
        
        # Handle file uploads
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        if form.resume_file.data:
            filename = secure_filename(f"resume_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{form.resume_file.data.filename}")
            filepath = os.path.join(upload_folder, filename)
            form.resume_file.data.save(filepath)
            order.resume_file = filename
        
        if form.cover_letter_file.data:
            filename = secure_filename(f"cover_letter_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{form.cover_letter_file.data.filename}")
            filepath = os.path.join(upload_folder, filename)
            form.cover_letter_file.data.save(filepath)
            order.cover_letter_file = filename
        
        if form.job_description_file.data:
            filename = secure_filename(f"job_desc_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{form.job_description_file.data.filename}")
            filepath = os.path.join(upload_folder, filename)
            form.job_description_file.data.save(filepath)
            order.job_description_file = filename
        
        db.session.add(order)
        db.session.commit()
        
        # Create Stripe checkout session
        try:
            domain = get_domain()
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': order.get_service_display_name(),
                        },
                        'unit_amount': int(price * 100),  # Stripe expects cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'https://{domain}/payment/success?order_id={order.id}',
                cancel_url=f'https://{domain}/payment/cancel?order_id={order.id}',
                metadata={'order_id': str(order.id)}
            )
            
            # Update order with Stripe session ID
            order.stripe_payment_id = checkout_session.id
            db.session.commit()
            
            return redirect(checkout_session.url, code=303)
            
        except Exception as e:
            logging.error(f"Stripe error: {str(e)}")
            flash('Payment processing error. Please try again.', 'danger')
            return redirect(url_for('services.order', service_type=service_type))
    
    flash('Please correct the errors below.', 'danger')
    return render_template('services/order.html', form=form)

@services_bp.route('/payment/success')
def payment_success():
    order_id = request.args.get('order_id')
    if order_id:
        order = Order.query.get_or_404(order_id)
        order.payment_status = 'completed'
        order.status = 'processing'
        db.session.commit()
        
        # Process referral reward
        if order.referral_used:
            referrer = User.query.filter_by(referral_code=order.referral_used).first()
            if referrer:
                reward_amount = order.referral_discount * 0.5  # 50% of discount as reward
                reward = ReferralReward(
                    referrer_id=referrer.id,
                    referred_id=order.user_id,
                    order_id=order.id,
                    reward_amount=reward_amount
                )
                referrer.referral_earnings += reward_amount
                db.session.add(reward)
                db.session.commit()
        
        # Send confirmation email
        send_email_notification('order_confirmation', order.email, order.full_name, order=order)
        
    return render_template('success.html', order=order if order_id else None)

@services_bp.route('/payment/cancel')
def payment_cancel():
    order_id = request.args.get('order_id')
    order = None
    if order_id:
        order = Order.query.get(order_id)
    return render_template('cancel.html', order=order)

# Dashboard routes
@dashboard_bp.route('/customer')
@login_required
def customer():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('dashboard/customer.html', orders=orders, user=current_user)

@dashboard_bp.route('/download/<int:order_id>/<file_type>')
@login_required
def download_file(order_id, file_type):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns the order
    if order.user_id != current_user.id:
        abort(403)
    
    # Check if order is completed
    if order.status != 'completed' and order.status != 'delivered':
        flash('Files are not yet available for download.', 'warning')
        return redirect(url_for('dashboard.customer'))
    
    # Get the appropriate file
    filename = None
    folder = current_app.config['COMPLETED_FOLDER']
    
    if file_type == 'resume' and order.completed_resume:
        filename = order.completed_resume
    elif file_type == 'cover_letter' and order.completed_cover_letter:
        filename = order.completed_cover_letter
    
    if not filename:
        flash('File not found.', 'danger')
        return redirect(url_for('dashboard.customer'))
    
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        flash('File not found on server.', 'danger')
        return redirect(url_for('dashboard.customer'))
    
    # Update order status to delivered on first download
    if order.status == 'completed':
        order.status = 'delivered'
        db.session.commit()
    
    return send_file(filepath, as_attachment=True, download_name=f"{file_type}_{order.id}.pdf")

# Admin routes
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin():
        abort(403)
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    total_orders = len(orders)
    pending_orders = len([o for o in orders if o.status == 'pending'])
    completed_orders = len([o for o in orders if o.status == 'completed'])
    
    return render_template('dashboard/admin.html', 
                         orders=orders, 
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         completed_orders=completed_orders)

@admin_bp.route('/order/<int:order_id>')
@login_required
def view_order(order_id):
    if not current_user.is_admin():
        abort(403)
    
    order = Order.query.get_or_404(order_id)
    form = AdminOrderUpdateForm()
    return render_template('admin/order_detail.html', order=order, form=form)

@admin_bp.route('/update_order/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
    if not current_user.is_admin():
        abort(403)
    
    order = Order.query.get_or_404(order_id)
    form = AdminOrderUpdateForm()
    
    if form.validate_on_submit():
        order.status = form.status.data
        order.updated_at = datetime.now(timezone.utc)
        
        # Handle completed file uploads
        completed_folder = current_app.config['COMPLETED_FOLDER']
        
        if form.completed_resume.data:
            filename = secure_filename(f"completed_resume_{order.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{form.completed_resume.data.filename}")
            filepath = os.path.join(completed_folder, filename)
            form.completed_resume.data.save(filepath)
            order.completed_resume = filename
        
        if form.completed_cover_letter.data:
            filename = secure_filename(f"completed_cover_letter_{order.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{form.completed_cover_letter.data.filename}")
            filepath = os.path.join(completed_folder, filename)
            form.completed_cover_letter.data.save(filepath)
            order.completed_cover_letter = filename
        
        if form.status.data == 'completed':
            order.completed_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        # Send status update email
        send_email_notification('status_update', order.email, order.full_name, order=order)
        
        flash('Order updated successfully!', 'success')
    
    return redirect(url_for('admin.view_order', order_id=order_id))

@admin_bp.route('/download/<int:order_id>/<file_type>')
@login_required
def download_customer_file(order_id, file_type):
    if not current_user.is_admin():
        abort(403)
    
    order = Order.query.get_or_404(order_id)
    
    # Get the appropriate file
    filename = None
    folder = current_app.config['UPLOAD_FOLDER']
    
    if file_type == 'resume' and order.resume_file:
        filename = order.resume_file
    elif file_type == 'cover_letter' and order.cover_letter_file:
        filename = order.cover_letter_file
    elif file_type == 'job_description' and order.job_description_file:
        filename = order.job_description_file
    
    if not filename:
        flash('File not found.', 'danger')
        return redirect(url_for('admin.view_order', order_id=order_id))
    
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        flash('File not found on server.', 'danger')
        return redirect(url_for('admin.view_order', order_id=order_id))
    
    return send_file(filepath, as_attachment=True, download_name=f"customer_{file_type}_{order.id}.pdf")

# Referral routes
@referral_bp.route('/dashboard')
@login_required
def dashboard():
    rewards = ReferralReward.query.filter_by(referrer_id=current_user.id).all()
    return render_template('referral/dashboard.html', user=current_user, rewards=rewards)
