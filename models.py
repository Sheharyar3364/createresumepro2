from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import func, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid

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
    
    # New relationships
    tracking_updates = db.relationship('OrderTracking', backref='order', lazy=True, cascade='all, delete-orphan')
    discount_applied = db.relationship('OrderDiscount', backref='order', uselist=False, cascade='all, delete-orphan')
    
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
    admin_response = db.Column(db.Text)
    response_date = db.Column(db.DateTime)
    priority = db.Column(db.String(10), default='normal')  # low, normal, high, urgent
    
    def __repr__(self):
        return f'<ContactMessage {self.name} - {self.subject}>'

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_title = db.Column(db.String(100))
    customer_company = db.Column(db.String(100))
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    testimonial_text = db.Column(db.Text, nullable=False)
    customer_photo = db.Column(db.String(255))  # path to photo
    industry = db.Column(db.String(100))
    service_used = db.Column(db.String(100))
    featured = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<Testimonial {self.customer_name} - {self.rating} stars>'

class FAQ(db.Model):
    __tablename__ = 'faqs'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # pricing, process, delivery, etc.
    order_index = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<FAQ {self.question[:50]}...>'

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    industry = db.Column(db.String(100))
    job_level = db.Column(db.String(50))  # entry, mid, senior, executive
    before_image = db.Column(db.String(255))  # path to before resume image
    after_image = db.Column(db.String(255))   # path to after resume image
    results_achieved = db.Column(db.Text)  # e.g., "Got interview at Google"
    featured = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<Portfolio {self.title}>'

class DiscountCode(db.Model):
    __tablename__ = 'discount_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    discount_type = db.Column(db.String(20), nullable=False)  # percentage, fixed
    discount_value = db.Column(db.Float, nullable=False)
    minimum_order = db.Column(db.Float, default=0)
    maximum_uses = db.Column(db.Integer)
    current_uses = db.Column(db.Integer, default=0)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now())
    
    # Relationships
    order_discounts = db.relationship('OrderDiscount', backref='discount_code', lazy=True)
    
    def __repr__(self):
        return f'<DiscountCode {self.code}>'
    
    @property
    def is_valid(self):
        now = datetime.utcnow()
        return (self.active and 
                self.valid_from <= now <= self.valid_until and
                (not self.maximum_uses or self.current_uses < self.maximum_uses))

class Referral(db.Model):
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_email = db.Column(db.String(120), nullable=False)
    referrer_name = db.Column(db.String(100), nullable=False)
    referred_email = db.Column(db.String(120), nullable=False)
    referred_name = db.Column(db.String(100))
    referral_code = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, rewarded
    reward_amount = db.Column(db.Float, default=0)
    reward_claimed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    completed_at = db.Column(db.DateTime)
    
    # Relationship to order when referral is used
    referred_order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    
    def __repr__(self):
        return f'<Referral {self.referrer_email} -> {self.referred_email}>'

class OrderTracking(db.Model):
    __tablename__ = 'order_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    created_by = db.Column(db.String(100))  # admin username or system
    created_at = db.Column(db.DateTime, default=func.now())
    estimated_completion = db.Column(db.DateTime)
    customer_notified = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<OrderTracking Order:{self.order_id} Status:{self.status}>'

class Template(db.Model):
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # resume, cover_letter, linkedin
    industry = db.Column(db.String(100))
    job_level = db.Column(db.String(50))
    file_path = db.Column(db.String(255))  # path to template file
    preview_image = db.Column(db.String(255))  # path to preview image
    premium_only = db.Column(db.Boolean, default=False)
    download_count = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<Template {self.name}>'

class NewsletterSubscriber(db.Model):
    __tablename__ = 'newsletter_subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    subscribed_at = db.Column(db.DateTime, default=func.now())
    active = db.Column(db.Boolean, default=True)
    preferences = db.Column(db.String(200))  # JSON string of preferences
    
    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'

class LiveChat(db.Model):
    __tablename__ = 'live_chats'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    customer_email = db.Column(db.String(120))
    customer_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, closed, transferred
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_at = db.Column(db.DateTime, default=func.now())
    closed_at = db.Column(db.DateTime)
    
    # Relationship to messages
    messages = db.relationship('ChatMessage', backref='chat', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<LiveChat {self.session_id}>'

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('live_chats.id'), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # customer, admin, system
    sender_name = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<ChatMessage {self.sender_type}: {self.message[:50]}...>'

class OrderDiscount(db.Model):
    __tablename__ = 'order_discounts'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    discount_code_id = db.Column(db.Integer, db.ForeignKey('discount_codes.id'), nullable=False)
    original_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, nullable=False)
    final_amount = db.Column(db.Float, nullable=False)
    applied_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<OrderDiscount Order:{self.order_id} Discount:{self.discount_amount}>'

class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # page_view, order_started, etc.
    event_data = db.Column(db.Text)  # JSON string
    user_id = db.Column(db.String(100))  # session ID or user identifier
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    referrer = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<Analytics {self.event_type} at {self.created_at}>'
