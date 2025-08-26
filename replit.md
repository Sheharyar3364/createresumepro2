# Overview

<<<<<<< HEAD
CreateProResume is a professional resume writing service web application built with Flask. The platform connects job seekers with expert resume writers, offering multiple service packages from basic resume rewrites to comprehensive career packages. The application features user authentication, order management, payment processing through Stripe, an admin dashboard for order tracking, and a referral program that rewards users for successful referrals.
=======
This is a professional resume writing service web application built with Flask that allows customers to order resume writing services through a tiered pricing system (Basic, Standard, Premium). The platform includes an order management system with Stripe payment integration, file upload capabilities for resumes and cover letters, email notifications, and an admin dashboard for order management.
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
<<<<<<< HEAD
- **Styling**: Custom CSS with Bootstrap dark theme and Font Awesome icons
- **JavaScript**: Vanilla JavaScript for client-side interactions (file uploads, clipboard operations, form validation)
- **User Interface**: Clean, professional design with separate interfaces for customers and administrators

## Backend Architecture
- **Framework**: Flask web framework with Blueprint-based routing
- **Authentication**: Flask-Login for session management with user roles (customer/admin)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Form Handling**: WTForms with Flask-WTF for secure form processing and CSRF protection
- **Email System**: Flask-Mail for transactional emails (order confirmations, status updates)

## Data Storage
- **Primary Database**: SQLAlchemy ORM with configurable database backend (SQLite for development, PostgreSQL for production)
- **Models**: User accounts, orders, admin profiles, contact messages, referral rewards
- **File Storage**: Local file system for uploaded resumes and completed work
- **Session Management**: Flask sessions with configurable lifetime

## Authentication & Authorization
- **User Authentication**: Password hashing with Werkzeug security
- **Role-Based Access**: Customer and admin user types with separate dashboards
- **Session Security**: CSRF protection and secure session configuration
- **Admin Controls**: Restricted admin routes with role verification

## Business Logic
- **Service Packages**: Three-tier pricing (Basic $99, Standard $149, Premium $199)
- **Order Workflow**: Order creation → payment processing → admin fulfillment → completion
- **Referral System**: 10% discount for new customers, 50% commission for referrers
- **File Management**: Secure file upload with size limits and type validation

# External Dependencies

## Payment Processing
- **Stripe**: Complete payment processing with webhooks for order fulfillment
- **Pricing**: Dynamic pricing with referral discount calculations

## Email Services
- **SMTP Provider**: Gmail SMTP for transactional emails
- **Email Types**: Order confirmations, status updates, admin notifications

## Development Tools
- **Bootstrap CDN**: Frontend styling framework
- **Font Awesome CDN**: Icon library for UI elements
- **Environment Variables**: Configuration management for sensitive data

## Hosting & Deployment
- **Replit Deployment**: Configured for Replit hosting environment
- **Proxy Configuration**: ProxyFix middleware for proper request handling
- **Database Flexibility**: Environment-based database URL configuration
=======
- **Styling**: Custom CSS with CSS variables for consistent theming, Google Fonts (Inter, Poppins)
- **JavaScript**: Vanilla JavaScript for form validation, file uploads, and interactive components
- **UI Components**: Multi-step order forms, pricing calculators, admin dashboard with statistics

## Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM using DeclarativeBase pattern
- **Database Models**: Admin users, Services (with tiered pricing), Orders, and ContactMessages
- **Authentication**: Flask-Login for admin authentication with session management
- **Form Handling**: Flask-WTF with comprehensive validation for order forms and file uploads
- **File Management**: Secure file upload handling for resumes, cover letters, and job descriptions

## Configuration Management
- **Environment-based**: Separate development and production configurations
- **Security**: CSRF protection, proxy fix for production deployment
- **Session Management**: 24-hour session lifetime with secure session handling

## Payment Processing
- **Stripe Integration**: Handles payment processing for different service tiers
- **Order Flow**: Submit order → Payment processing → Success/Cancel handling
- **Pricing Structure**: Three-tier system (Basic/Standard/Premium) per service type

## Data Storage
- **Primary Database**: PostgreSQL with connection pooling and health checks
- **File Storage**: Local file system with configurable upload directory (16MB limit)
- **Session Storage**: Flask session management for order tracking

# External Dependencies

## Payment Services
- **Stripe**: Payment processing with separate price IDs for each service tier
- **Webhook Support**: Handles payment confirmation and order status updates

## Email Services
- **Flask-Mail**: Email notifications for order confirmations and status updates
- **SMTP Configuration**: Supports Gmail SMTP with TLS encryption
- **Email Templates**: Automated emails for order processing workflow

## File Handling
- **Upload Support**: PDF, DOC, DOCX, and TXT files
- **Security**: File type validation and secure filename handling
- **Storage**: Configurable upload directory with size limits

## UI Libraries
- **Bootstrap 5**: Responsive design framework
- **Font Awesome**: Icon library for UI components
- **Google Fonts**: Typography enhancement (Inter, Poppins families)

## Development Tools
- **Flask-WTF**: Form handling and CSRF protection
- **Werkzeug**: WSGI utilities and security helpers
- **SQLAlchemy**: Database ORM with PostgreSQL support
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d
