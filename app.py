import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
<<<<<<< HEAD
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
=======
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import redis
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()
<<<<<<< HEAD
=======
csrf = CSRFProtect()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Database configuration
<<<<<<< HEAD
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///resume_service.db")
=======
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://localhost/resume_service")
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
<<<<<<< HEAD
    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@createproresume.com')
    
    # Upload configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['COMPLETED_FOLDER'] = 'completed'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Stripe configuration
    app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')
=======
    # Upload configuration
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
    
    # Mail configuration - Mailtrap for testing
    app.config["MAIL_SERVER"] = "sandbox.smtp.mailtrap.io"
    app.config["MAIL_PORT"] = 2525
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = "f37375f3b6e4f9"
    app.config["MAIL_PASSWORD"] = "0784b16e5f4274"
    app.config["MAIL_DEFAULT_SENDER"] = "hello@createproresume.com"
    app.config["ADMIN_EMAIL"] = "msheharyar2020@gmail.com"
    
    # Stripe configuration
    app.config["STRIPE_SECRET_KEY"] = os.environ.get("STRIPE_SECRET_KEY")
    app.config["STRIPE_PUBLISHABLE_KEY"] = os.environ.get("STRIPE_PUBLISHABLE_KEY")
    
    # Redis and Caching configuration
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = redis_url
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300
    
    # Rate limiting configuration
    app.config["RATELIMIT_STORAGE_URL"] = redis_url
    app.config["RATELIMIT_DEFAULT"] = "100 per hour"
    
    # Session configuration
    app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 24 hours
    
    # Feature flags
    app.config["ENABLE_TESTIMONIALS"] = True
    app.config["ENABLE_PORTFOLIO"] = True
    app.config["ENABLE_LIVE_CHAT"] = True
    app.config["ENABLE_REFERRALS"] = True
    app.config["ENABLE_ANALYTICS"] = True
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
<<<<<<< HEAD
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['COMPLETED_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from routes import main_bp, auth_bp, services_bp, dashboard_bp, admin_bp, referral_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(referral_bp, url_prefix='/referral')
    
    # Create database tables
    with app.app_context():
        import models
        db.create_all()
        
        # Create default admin user
        from models import User, Admin
        from werkzeug.security import generate_password_hash
        
        admin_user = User.query.filter_by(email='admin@createproresume.com').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@createproresume.com',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin_user)
            db.session.commit()
            
            admin_profile = Admin(user_id=admin_user.id)
            db.session.add(admin_profile)
            db.session.commit()
    
    return app

# Create app instance
=======
    csrf.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = "admin_login"  # type: ignore
    login_manager.login_message = "Please log in to access the admin dashboard."
    login_manager.login_message_category = "info"
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import Admin
        return Admin.query.get(int(user_id))
    
    # Create upload directory
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    with app.app_context():
        # Import models
        import models
        
        # Create tables
        db.create_all()
        
        # Create default admin user if not exists
        from models import Admin, Service
        from werkzeug.security import generate_password_hash
        
        admin = Admin.query.filter_by(username="admin").first()
        if not admin:
            admin = Admin(  # type: ignore
                username="admin",
                email="admin@resumeservice.com",
                password_hash=generate_password_hash("admin123")
            )
            db.session.add(admin)
            logging.info("Default admin user created: admin/admin123")
        
        # Create default services if not exist
        services_data = [
            {
                'name': 'Professional Resume Writing',
                'description': 'Expert-crafted resumes that get you noticed by employers and pass ATS systems.',
                'price_basic': 99.00,
                'price_standard': 199.00,
                'price_premium': 299.00,
                'features_basic': 'Professional Resume, ATS-Optimized Format, 1 Revision Round, PDF & Word Formats, 3-5 Day Delivery',
                'features_standard': 'Professional Resume, Custom Cover Letter, LinkedIn Profile Optimization, 2 Revision Rounds, Multiple Formats, 2-4 Day Delivery',
                'features_premium': 'Professional Resume, Custom Cover Letter, LinkedIn Profile Optimization, Thank You Letter Template, Unlimited Revisions, 1-2 Day Rush Delivery, 60-Day Follow-up Support'
            },
            {
                'name': 'Cover Letter Writing',
                'description': 'Compelling cover letters that tell your story and convince employers.',
                'price_basic': 49.00,
                'price_standard': 89.00,
                'price_premium': 129.00,
                'features_basic': 'Custom Cover Letter, Professional Format, 1 Revision Round, 3-5 Day Delivery',
                'features_standard': 'Custom Cover Letter, Company Research, 2 Revision Rounds, Multiple Formats, 2-4 Day Delivery',
                'features_premium': 'Custom Cover Letter, Company Research, Industry Analysis, Unlimited Revisions, 1-2 Day Rush Delivery, Follow-up Support'
            },
            {
                'name': 'LinkedIn Profile Optimization',
                'description': 'Complete LinkedIn makeover to increase visibility and attract recruiters.',
                'price_basic': 79.00,
                'price_standard': 149.00,
                'price_premium': 199.00,
                'features_basic': 'Profile Headline, Summary Optimization, 1 Revision Round, 3-5 Day Delivery',
                'features_standard': 'Complete Profile Overhaul, Keyword Optimization, Experience Descriptions, 2 Revision Rounds, 2-4 Day Delivery',
                'features_premium': 'Complete Profile Transformation, Advanced SEO, Skills Section, Recommendations Template, Unlimited Revisions, 1-2 Day Rush Delivery'
            }
        ]
        
        for service_data in services_data:
            existing_service = Service.query.filter_by(name=service_data['name']).first()
            if not existing_service:
                service = Service(**service_data)
                db.session.add(service)
                logging.info(f"Created default service: {service_data['name']}")
        
        db.session.commit()
    
    # Register routes
    from routes import register_routes
    register_routes(app)
    
    return app

>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d
app = create_app()
