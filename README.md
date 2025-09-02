# VPS Reseller System

A comprehensive VPS (Virtual Private Server) reseller system built with Django 5.0, integrated with Contabo API for automated VPS management, and featuring PayPal/2Checkout payment processing.

## 🚀 Features

### Core Functionality
- **VPS Management**: Complete integration with Contabo API for VPS creation, management, and monitoring
- **User Authentication**: Django-based authentication with Admin and Client roles
- **Payment Processing**: PayPal and 2Checkout integration with webhook support
- **Automated Billing**: Recurring billing, invoice generation, and payment tracking
- **Email Notifications**: Automated emails for VPS creation, billing, and system updates

### Admin Features
- **User Management**: Comprehensive user and profile management
- **VPS Package Management**: Create and manage VPS hosting packages
- **Order Management**: Track and manage customer orders
- **Support System**: Built-in ticketing system for customer support
- **Analytics**: Dashboard with usage statistics and revenue tracking
- **System Monitoring**: Real-time status monitoring and maintenance windows

### Client Features
- **Dashboard**: Intuitive client dashboard with VPS overview
- **VPS Control**: Start, stop, restart, rebuild, and manage VPS instances
- **Backup Management**: Create, restore, and manage VPS backups
- **SSH Key Management**: Upload and manage SSH keys
- **Billing Portal**: View invoices, payment history, and billing information
- **Support Tickets**: Create and manage support tickets

### Technical Features
- **Responsive Design**: Mobile-first Bootstrap 5 interface
- **API Integration**: RESTful Contabo API integration with error handling
- **Security**: CSRF protection, input validation, and encrypted password storage
- **Scalability**: PostgreSQL database with optimized queries
- **Monitoring**: Activity logging and API usage tracking

## 🛠️ Technology Stack

- **Backend**: Django 5.0, Python 3.13
- **Database**: PostgreSQL (SQLite for development)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript (Vanilla)
- **Payment Gateways**: PayPal REST SDK, 2Checkout
- **VPS Provider**: Contabo API
- **Email**: SendGrid (configurable)
- **Task Queue**: Celery with Redis
- **Deployment**: Docker-ready, Gunicorn, Whitenoise

## 📋 Prerequisites

- Python 3.13+
- PostgreSQL 12+
- Redis (for Celery)
- Git

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd vps-reseller
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://username:password@localhost:5432/vps_reseller

# Contabo API Credentials
CONTABO_CLIENT_ID=your-contabo-client-id
CONTABO_CLIENT_SECRET=your-contabo-client-secret
CONTABO_API_USER=your-contabo-api-user
CONTABO_API_PASSWORD=your-contabo-api-password

# Payment Gateways
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox

# Email Settings
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Create Sample Data (Optional)
```bash
python manage.py shell
```
```python
from vps.models import VPSPackage
from decimal import Decimal

# Create sample VPS packages
VPSPackage.objects.create(
    name="Starter VPS",
    description="Perfect for small projects and development",
    cpu_cores=1,
    ram_gb=2,
    storage_gb=25,
    bandwidth_gb=1000,
    monthly_price=Decimal('9.99'),
    contabo_image_id="ubuntu-20.04",
    contabo_product_id="vps-1",
    is_active=True
)
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 🔧 Configuration

### Contabo API Setup
1. Register for a Contabo account
2. Generate API credentials in the Contabo customer panel
3. Update the `.env` file with your credentials

### Payment Gateway Setup

#### PayPal
1. Create a PayPal developer account
2. Create a new application
3. Add your client ID and secret to `.env`

#### 2Checkout
1. Register for a 2Checkout account
2. Get your account number and secret key
3. Add credentials to `.env`

### Email Configuration
Configure your preferred email service in `.env`:
- SendGrid (recommended)
- SMTP server
- Console backend (development)

## 🚀 Deployment

### Using Docker (Recommended)
```bash
# Build the image
docker build -t vps-reseller .

# Run with docker-compose
docker-compose up -d
```

### Manual Deployment
1. Set up PostgreSQL and Redis
2. Configure environment variables
3. Run migrations and collect static files
4. Use Gunicorn with nginx

## 📝 API Documentation

### Contabo API Integration
The system integrates with Contabo's REST API for:
- VPS instance management
- Image and product catalog
- SSH key management
- Backup operations
- Usage statistics

### Webhook Endpoints
- PayPal: `/payments/webhooks/paypal/`
- 2Checkout: `/payments/webhooks/2checkout/`

## 🔒 Security Features

- CSRF protection enabled
- Input validation and sanitization
- Password encryption for VPS credentials
- Secure session management
- SQL injection prevention
- XSS protection

## 📊 Monitoring & Logging

- Activity logging for all user actions
- API usage tracking
- System status monitoring
- Error logging and reporting
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the documentation
2. Create an issue on GitHub
3. Contact the development team

## 🔄 Updates & Maintenance

Regular updates include:
- Security patches
- API compatibility updates
- Feature enhancements
- Bug fixes

## 📱 Mobile Support

The application is fully responsive and optimized for:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

---

**Note**: This is a production-ready VPS reseller system with comprehensive features for managing VPS hosting business operations. Ensure proper security measures and testing before deploying to production.
