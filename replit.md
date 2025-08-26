# Overview

CreateProResume is a professional resume writing service web application built with Flask. The platform connects job seekers with expert resume writers, offering multiple service packages from basic resume rewrites to comprehensive career packages. The application features user authentication, order management, payment processing through Stripe, an admin dashboard for order tracking, and a referral program that rewards users for successful referrals.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
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