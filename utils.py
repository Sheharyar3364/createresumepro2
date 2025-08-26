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
