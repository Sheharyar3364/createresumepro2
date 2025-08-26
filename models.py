from app import db
from flask_login import UserMixin
from datetime import datetime, timezone
import secrets
import string

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Referral system
    referral_code = db.Column(db.String(20), unique=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    referral_earnings = db.Column(db.Float, default=0.0)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    referrals = db.relationship('User', backref=db.backref('referrer', remote_side=[id]), lazy=True)
    admin_profile = db.relationship('Admin', backref='user', uselist=False)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
    
    def generate_referral_code(self):
        """Generate a unique referral code"""
        while True:
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if not User.query.filter_by(referral_code=code).first():
                return code
    
    def is_admin(self):
        """Check if user is an admin"""
        return self.admin_profile is not None
    
    def get_referral_count(self):
        """Get count of successful referrals"""
        return len(self.referrals)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Order details
    service_type = db.Column(db.String(50), nullable=False)  # 'basic', 'standard', 'premium'
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, delivered
    
    # Contact information
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    
    # Job details
    target_position = db.Column(db.String(200))
    industry = db.Column(db.String(100))
    experience_level = db.Column(db.String(50))
    special_requirements = db.Column(db.Text)
    
    # File uploads (customer submitted documents)
    resume_file = db.Column(db.String(255))
    cover_letter_file = db.Column(db.String(255))
    job_description_file = db.Column(db.String(255))
    
    # Completed documents (admin uploads)
    completed_resume = db.Column(db.String(255))
    completed_cover_letter = db.Column(db.String(255))
    
    # Payment
    stripe_payment_id = db.Column(db.String(255))
    payment_status = db.Column(db.String(50), default='pending')
    
    # Referral
    referral_used = db.Column(db.String(20))  # referral code used
    referral_discount = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime)
    
    def get_status_badge_class(self):
        """Return Bootstrap badge class for status"""
        status_classes = {
            'pending': 'bg-warning',
            'processing': 'bg-info',
            'completed': 'bg-success',
            'delivered': 'bg-primary'
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    def get_service_display_name(self):
        """Return display name for service type"""
        service_names = {
            'basic': 'Basic Resume ($99)',
            'standard': 'Standard Package ($199)',
            'premium': 'Premium Package ($299)'
        }
        return service_names.get(self.service_type, self.service_type.title())

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    responded = db.Column(db.Boolean, default=False)

class ReferralReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    reward_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    paid = db.Column(db.Boolean, default=False)
    
    # Relationships
    referrer = db.relationship('User', foreign_keys=[referrer_id], backref='given_rewards')
    referred = db.relationship('User', foreign_keys=[referred_id], backref='received_rewards')
    order = db.relationship('Order', backref='referral_reward')
