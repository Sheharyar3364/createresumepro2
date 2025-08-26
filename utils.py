import os
<<<<<<< HEAD
import logging
from flask import current_app
from flask_mail import Message
from app import mail

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_referral_discount(price):
    """Calculate referral discount (10% of order value)"""
    return round(price * 0.10, 2)

def send_email_notification(notification_type, to_email, user_name, order=None):
    """Send email notifications"""
    try:
        if notification_type == 'order_confirmation':
            subject = '✅ Order Confirmation - CreateProResume'
            body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Confirmation</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #2563eb 0%, #64748b 100%); color: white; padding: 30px 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">CreateProResume</h1>
            <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Professional Resume Writing Service</p>
        </div>
        
        <!-- Main Content -->
        <div style="padding: 40px;">
            <h2 style="color: #2563eb; margin: 0 0 20px 0; font-size: 24px;">🎉 Thank You for Your Order!</h2>
            
            <p style="font-size: 16px; margin-bottom: 25px;">Dear <strong>{user_name}</strong>,</p>
            
            <p style="font-size: 16px; margin-bottom: 25px;">We're excited to help you create an outstanding resume that will make you stand out to employers. Your order has been successfully received and our expert writers will begin working on it shortly.</p>
            
            <!-- Order Details Card -->
            <div style="background-color: #f8f9fa; border: 2px solid #e9ecef; border-radius: 10px; padding: 25px; margin: 25px 0;">
                <h3 style="color: #2563eb; margin: 0 0 15px 0; font-size: 18px;">📋 Order Details</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-weight: 600;">Order ID:</td>
                        <td style="padding: 8px 0; font-weight: bold;">#{order.id}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-weight: 600;">Service:</td>
                        <td style="padding: 8px 0; font-weight: bold; color: #2563eb;">{order.get_service_display_name()}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-weight: 600;">Amount Paid:</td>
                        <td style="padding: 8px 0; font-weight: bold; color: #059669; font-size: 18px;">${order.price:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-weight: 600;">Status:</td>
                        <td style="padding: 8px 0;"><span style="background-color: #fbbf24; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">{order.status.upper()}</span></td>
                    </tr>
                </table>
            </div>
            
            <!-- What's Next -->
            <div style="background-color: #eff6ff; border-left: 4px solid #2563eb; padding: 20px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                <h3 style="color: #2563eb; margin: 0 0 15px 0; font-size: 18px;">🚀 What Happens Next?</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    <li style="margin-bottom: 8px;">Our certified writers will review your information</li>
                    <li style="margin-bottom: 8px;">We'll create your professional documents tailored to your industry</li>
                    <li style="margin-bottom: 8px;">You'll receive email updates throughout the process</li>
                    <li style="margin-bottom: 8px;">Completed documents will be available in your dashboard within 3-5 business days</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <p style="margin-bottom: 20px; color: #666;">Track your order progress anytime:</p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f8f9fa; padding: 25px 40px; text-align: center; border-top: 1px solid #e9ecef;">
            <p style="margin: 0; color: #666; font-size: 14px;">Need help? Contact us at <a href="mailto:support@createproresume.com" style="color: #2563eb; text-decoration: none;">support@createproresume.com</a></p>
            <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">&copy; 2025 CreateProResume. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
            """
        
        elif notification_type == 'status_update':
            subject = f'📋 Order Status Update - CreateProResume (#{order.id})'
            status_message = "Your completed documents are now ready for download in your dashboard!" if order.status == 'completed' else "We'll continue to keep you updated on your order progress."
            status_color = "#059669" if order.status == 'completed' else "#fbbf24"
            body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Status Update</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #2563eb 0%, #64748b 100%); color: white; padding: 30px 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">CreateProResume</h1>
            <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Professional Resume Writing Service</p>
        </div>
        
        <!-- Main Content -->
        <div style="padding: 40px;">
            <h2 style="color: #2563eb; margin: 0 0 20px 0; font-size: 24px;">📋 Order Status Update</h2>
            
            <p style="font-size: 16px; margin-bottom: 25px;">Dear <strong>{user_name}</strong>,</p>
            
            <p style="font-size: 16px; margin-bottom: 25px;">Great news! Your order status has been updated. Here are the latest details:</p>
            
            <!-- Status Update Card -->
            <div style="background-color: #f8f9fa; border: 2px solid #e9ecef; border-radius: 10px; padding: 25px; margin: 25px 0;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-weight: 600;">Order ID:</td>
                        <td style="padding: 8px 0; font-weight: bold;">#{order.id}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-weight: 600;">Service:</td>
                        <td style="padding: 8px 0; font-weight: bold; color: #2563eb;">{order.get_service_display_name()}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-weight: 600;">New Status:</td>
                        <td style="padding: 8px 0;"><span style="background-color: {status_color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: bold;">{order.status.upper()}</span></td>
                    </tr>
                </table>
            </div>
            
            <!-- Status Message -->
            <div style="background-color: #eff6ff; border-left: 4px solid #2563eb; padding: 20px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                <p style="margin: 0; font-size: 16px; color: #333;">{status_message}</p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f8f9fa; padding: 25px 40px; text-align: center; border-top: 1px solid #e9ecef;">
            <p style="margin: 0; color: #666; font-size: 14px;">Need help? Contact us at <a href="mailto:support@createproresume.com" style="color: #2563eb; text-decoration: none;">support@createproresume.com</a></p>
            <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">&copy; 2025 CreateProResume. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
            """
        
        elif notification_type == 'contact':
            subject = '💬 Thank you for contacting CreateProResume'
            body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You for Contacting Us</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #2563eb 0%, #64748b 100%); color: white; padding: 30px 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">CreateProResume</h1>
            <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Professional Resume Writing Service</p>
        </div>
        
        <!-- Main Content -->
        <div style="padding: 40px;">
            <h2 style="color: #2563eb; margin: 0 0 20px 0; font-size: 24px;">💬 Thank You for Reaching Out!</h2>
            
            <p style="font-size: 16px; margin-bottom: 25px;">Dear <strong>{user_name}</strong>,</p>
            
            <p style="font-size: 16px; margin-bottom: 25px;">Thank you for contacting CreateProResume! We've received your message and truly appreciate you taking the time to reach out to us.</p>
            
            <!-- Response Promise -->
            <div style="background-color: #f0fdf4; border: 2px solid #bbf7d0; border-radius: 10px; padding: 25px; margin: 25px 0;">
                <h3 style="color: #059669; margin: 0 0 15px 0; font-size: 18px;">⏱️ What's Next?</h3>
                <p style="margin: 0; font-size: 16px; color: #333;">Our team will review your message and get back to you within <strong>24 hours</strong>. We're committed to providing you with the best possible service and answering all your questions.</p>
            </div>
            
            <!-- Services Reminder -->
            <div style="background-color: #eff6ff; border-left: 4px solid #2563eb; padding: 20px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                <h3 style="color: #2563eb; margin: 0 0 15px 0; font-size: 18px;">🚀 Ready to Get Started?</h3>
                <p style="margin: 0; font-size: 16px; color: #333;">While you wait for our response, feel free to explore our professional resume writing packages. We offer:</p>
                <ul style="margin: 10px 0 0 20px; color: #333;">
                    <li style="margin-bottom: 5px;">Basic Resume Writing ($99)</li>
                    <li style="margin-bottom: 5px;">Standard Package with Cover Letter ($199)</li>
                    <li style="margin-bottom: 5px;">Premium Career Package ($299)</li>
                </ul>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f8f9fa; padding: 25px 40px; text-align: center; border-top: 1px solid #e9ecef;">
            <p style="margin: 0; color: #666; font-size: 14px;">Questions? Email us at <a href="mailto:support@createproresume.com" style="color: #2563eb; text-decoration: none;">support@createproresume.com</a></p>
            <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">&copy; 2025 CreateProResume. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
            """
        
        else:
            return False
        
        msg = Message(
            subject=subject,
            recipients=[to_email],
            html=body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        logging.error(f"Email sending failed: {str(e)}")
        return False
=======
import uuid
import json
from datetime import datetime, timedelta
from flask import session, request, current_app
from werkzeug.utils import secure_filename
from models import Analytics, DiscountCode, OrderDiscount
from app import db

def generate_referral_code():
    """Generate a unique referral code"""
    return str(uuid.uuid4()).replace('-', '').upper()[:8]

def generate_session_id():
    """Generate a unique session ID for live chat"""
    return str(uuid.uuid4())

def track_event(event_type, event_data=None, user_id=None):
    """Track analytics event"""
    if not current_app.config.get('ENABLE_ANALYTICS', False):
        return
    
    try:
        analytics_entry = Analytics(
            event_type=event_type,
            event_data=json.dumps(event_data) if event_data else None,
            user_id=user_id or session.get('user_id', 'anonymous'),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            referrer=request.referrer
        )
        db.session.add(analytics_entry)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Analytics tracking error: {e}")

def validate_discount_code(code, order_amount):
    """Validate and apply discount code"""
    if not code:
        return None, "Please enter a discount code"
    
    discount = DiscountCode.query.filter_by(code=code.upper(), active=True).first()
    
    if not discount:
        return None, "Invalid discount code"
    
    if not discount.is_valid:
        return None, "This discount code has expired or reached its usage limit"
    
    if order_amount < discount.minimum_order:
        return None, f"Minimum order amount of ${discount.minimum_order:.2f} required for this discount"
    
    # Calculate discount amount
    if discount.discount_type == 'percentage':
        discount_amount = order_amount * (discount.discount_value / 100)
    else:  # fixed amount
        discount_amount = discount.discount_value
    
    # Ensure discount doesn't exceed order amount
    discount_amount = min(discount_amount, order_amount)
    final_amount = order_amount - discount_amount
    
    return {
        'discount_code': discount,
        'original_amount': order_amount,
        'discount_amount': discount_amount,
        'final_amount': final_amount
    }, None

def apply_discount_to_order(order, discount_info):
    """Apply discount to order and update discount usage"""
    if not discount_info:
        return
    
    # Create order discount record
    order_discount = OrderDiscount(
        order_id=order.id,
        discount_code_id=discount_info['discount_code'].id,
        original_amount=discount_info['original_amount'],
        discount_amount=discount_info['discount_amount'],
        final_amount=discount_info['final_amount']
    )
    
    # Update order total
    order.total_amount = discount_info['final_amount']
    
    # Update discount usage
    discount_info['discount_code'].current_uses += 1
    
    db.session.add(order_discount)
    db.session.commit()

def get_file_extension(filename):
    """Get file extension safely"""
    if not filename:
        return ''
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension"""
    return get_file_extension(filename) in allowed_extensions

def save_uploaded_file(file, upload_folder, prefix=""):
    """Save uploaded file with unique name"""
    if not file or file.filename == '':
        return None
    
    filename = secure_filename(file.filename)
    if not filename:
        return None
    
    # Add timestamp and prefix to filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    unique_filename = f"{prefix}_{timestamp}_{name}{ext}" if prefix else f"{timestamp}_{filename}"
    
    file_path = os.path.join(upload_folder, unique_filename)
    
    try:
        file.save(file_path)
        return unique_filename
    except Exception as e:
        current_app.logger.error(f"File upload error: {e}")
        return None

def calculate_estimated_delivery(service_tier):
    """Calculate estimated delivery date based on service tier"""
    days_map = {
        'basic': 5,      # 3-5 days
        'standard': 3,   # 2-4 days  
        'premium': 2     # 1-2 days
    }
    
    days = days_map.get(service_tier, 5)
    return datetime.now() + timedelta(days=days)

def format_price(amount):
    """Format price with currency symbol"""
    return f"${amount:.2f}"

def get_service_features_list(features_text):
    """Convert features text to list"""
    if not features_text:
        return []
    return [feature.strip() for feature in features_text.split(',')]

def generate_order_tracking_code():
    """Generate a unique tracking code for orders"""
    return f"CPR{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4()).replace('-', '').upper()[:6]}"

def get_user_timezone_offset():
    """Get user timezone offset from session or default to UTC"""
    return session.get('timezone_offset', 0)

def convert_to_user_timezone(dt):
    """Convert datetime to user's timezone"""
    if not dt:
        return None
    
    offset = get_user_timezone_offset()
    return dt + timedelta(hours=offset)

def truncate_text(text, max_length=100, suffix="..."):
    """Truncate text with suffix"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def get_client_ip():
    """Get client IP address considering proxies"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def is_mobile_device():
    """Check if request is from mobile device"""
    user_agent = request.headers.get('User-Agent', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'tablet', 'phone']
    return any(keyword in user_agent for keyword in mobile_keywords)

def generate_seo_friendly_slug(text):
    """Generate SEO-friendly slug from text"""
    import re
    
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().replace(' ', '-')
    
    # Remove special characters except hyphens
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug[:50]  # Limit length

def calculate_completion_percentage(order):
    """Calculate order completion percentage based on status"""
    status_percentages = {
        'pending': 10,
        'in_progress': 50,
        'completed': 100,
        'cancelled': 0
    }
    return status_percentages.get(order.status, 0)

def get_order_status_color(status):
    """Get Bootstrap color class for order status"""
    colors = {
        'pending': 'warning',
        'in_progress': 'info', 
        'completed': 'success',
        'cancelled': 'danger'
    }
    return colors.get(status, 'secondary')

def send_admin_notification_email(subject, message):
    """Send notification email to admin"""
    from flask_mail import Message as MailMessage
    from app import mail
    
    try:
        admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@createproresume.com')
        msg = MailMessage(
            subject=f"[CreateProResume Admin] {subject}",
            recipients=[admin_email],
            body=message
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Admin notification email error: {e}")
        return False

def log_user_action(action, details=None):
    """Log user actions for admin review"""
    try:
        track_event('user_action', {
            'action': action,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        current_app.logger.error(f"User action logging error: {e}")

def get_popular_services(limit=3):
    """Get most popular services based on order count"""
    from models import Service, Order
    from sqlalchemy import func
    
    try:
        return db.session.query(Service, func.count(Order.id).label('order_count'))\
                        .join(Order, Service.id == Order.service_id)\
                        .filter(Service.active == True)\
                        .group_by(Service.id)\
                        .order_by(func.count(Order.id).desc())\
                        .limit(limit).all()
    except Exception as e:
        current_app.logger.error(f"Popular services query error: {e}")
        return []
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d
