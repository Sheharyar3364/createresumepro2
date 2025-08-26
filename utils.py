import os
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
            subject = 'Order Confirmation - CreateProResume'
            body = f"""
Dear {user_name},

Thank you for your order! We have received your request for our {order.get_service_display_name()}.

Order Details:
- Order ID: #{order.id}
- Service: {order.get_service_display_name()}
- Amount Paid: ${order.price:.2f}
- Status: {order.status.title()}

We will begin working on your order shortly and keep you updated on the progress.

Best regards,
CreateProResume Team
            """
        
        elif notification_type == 'status_update':
            subject = f'Order Status Update - CreateProResume (#{order.id})'
            body = f"""
Dear {user_name},

Your order status has been updated:

Order ID: #{order.id}
New Status: {order.status.title()}
Service: {order.get_service_display_name()}

{f"Your completed documents are now ready for download in your dashboard!" if order.status == 'completed' else "We'll continue to keep you updated on your order progress."}

Best regards,
CreateProResume Team
            """
        
        elif notification_type == 'contact':
            subject = 'Thank you for contacting CreateProResume'
            body = f"""
Dear {user_name},

Thank you for reaching out to us! We have received your message and will get back to you within 24 hours.

We appreciate your interest in our services.

Best regards,
CreateProResume Team
            """
        
        else:
            return False
        
        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        logging.error(f"Email sending failed: {str(e)}")
        return False
