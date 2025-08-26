# Overview

This is a professional resume writing service web application built with Flask that allows customers to order resume writing services through a tiered pricing system (Basic, Standard, Premium). The platform includes an order management system with Stripe payment integration, file upload capabilities for resumes and cover letters, email notifications, and an admin dashboard for order management.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
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