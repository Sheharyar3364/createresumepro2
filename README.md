# CreateProResume - Professional Resume Writing Service

A complete Flask web application for professional resume writing services with Stripe payment integration, file uploads, and admin dashboard.

## Features

- **Professional Homepage** with service descriptions and pricing
- **Multi-tier Pricing** (Basic $99, Standard $199, Premium $299)
- **Order System** with file uploads for resumes, cover letters, and job descriptions  
- **Stripe Payment Integration** for secure transactions
- **Email Notifications** for orders, payments, and status updates
- **Admin Dashboard** for order management and tracking
- **Contact System** with automated email responses
- **Responsive Design** with Bootstrap 5

## Technology Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Frontend:** Jinja2 templates, Bootstrap 5, Vanilla JavaScript
- **Payments:** Stripe
- **Email:** Flask-Mail with SMTP
- **Deployment:** Gunicorn, Heroku-ready

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/sheharyar3364/createproresume.git
cd createproresume
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
DATABASE_URL=your_postgresql_url
STRIPE_SECRET_KEY=your_stripe_secret_key
MAIL_USERNAME=your_email_username
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=your_email@domain.com
```

4. Run the application:
```bash
python main.py
```

## Admin Access

- **Username:** admin
- **Password:** admin123

## Deployment

This application is ready for deployment on platforms like:
- Heroku
- Railway
- Vercel
- DigitalOcean

## Contact

For questions or support, contact: msheharyar2020@gmail.com

## License

MIT License - feel free to use for your projects.