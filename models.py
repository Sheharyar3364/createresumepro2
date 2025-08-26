from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import func

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_basic = db.Column(db.Float, nullable=False)
    price_standard = db.Column(db.Float, nullable=False)
    price_premium = db.Column(db.Float, nullable=False)
    features_basic = db.Column(db.Text)
    features_standard = db.Column(db.Text)
    features_premium = db.Column(db.Text)
    stripe_price_id_basic = db.Column(db.String(100))
    stripe_price_id_standard = db.Column(db.String(100))
    stripe_price_id_premium = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now())
    
    # Relationship
    orders = db.relationship('Order', backref='service', lazy=True)
    
    def __repr__(self):
        return f'<Service {self.name}>'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Customer information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    
    # Service details
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service_tier = db.Column(db.String(20), nullable=False)  # basic, standard, premium
    total_amount = db.Column(db.Float, nullable=False)
    
    # Career information
    current_position = db.Column(db.String(100))
    target_position = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    career_goals = db.Column(db.Text)
    special_requirements = db.Column(db.Text)
    
    # File uploads
    uploaded_resume_path = db.Column(db.String(255))
    uploaded_cover_letter_path = db.Column(db.String(255))
    uploaded_job_description_path = db.Column(db.String(255))
    
    # Order status
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    stripe_session_id = db.Column(db.String(255))
    stripe_payment_intent_id = db.Column(db.String(255))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    completed_at = db.Column(db.DateTime)
    
    # Admin notes
    admin_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Order {self.id} - {self.first_name} {self.last_name}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def status_badge_class(self):
        status_classes = {
            'pending': 'badge-warning',
            'in_progress': 'badge-info',
            'completed': 'badge-success',
            'cancelled': 'badge-danger'
        }
        return status_classes.get(self.status, 'badge-secondary')
    
    @property
    def payment_status_badge_class(self):
        payment_classes = {
            'pending': 'badge-warning',
            'paid': 'badge-success',
            'failed': 'badge-danger',
            'refunded': 'badge-secondary'
        }
        return payment_classes.get(self.payment_status, 'badge-secondary')

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    responded = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<ContactMessage {self.name} - {self.subject}>'
