# BoltTrip 🏖️

*"Where journeys begin with just one click!"*

A comprehensive Django-based travel management platform that streamlines the entire travel booking experience. From discovering destinations to managing bookings, BoltTrip provides a seamless solution for travelers and travel agencies.

[![Django](https://img.shields.io/badge/Django-4.2.1-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com/)

## 🌟 Features

### 🧳 **Travel Management**
- **Comprehensive Package System**: Create and manage travel packages with detailed itineraries
- **Multi-destination Support**: Handle complex multi-city travel plans
- **Dynamic Pricing**: Flexible pricing structures with currency support
- **Category Organization**: Organize packages by destination, theme, and duration

### 🏨 **Hotel Booking**
- **Hotel Management**: Complete hotel inventory with room types and amenities
- **Availability Tracking**: Real-time room availability and booking management
- **Amenity Management**: Detailed amenity tracking and guest preferences

### ✈️ **Flight Management**
- **Flight Database**: Comprehensive flight information with airline partnerships
- **Route Management**: Efficient flight route and schedule handling
- **Search Integration**: Advanced flight search with multiple criteria

### 👥 **User Management**
- **Multi-role System**: Separate interfaces for travelers, guides, and administrators
- **Guide Profiles**: Professional guide management with expertise tracking
- **User Authentication**: Secure JWT-based authentication with OTP verification
- **Profile Management**: Comprehensive user profile and preference system

### 📊 **Booking & Payments**
- **Integrated Booking**: Seamless booking flow across all travel services
- **Payment Processing**: Secure payment handling with transaction tracking
- **Booking Management**: Complete booking lifecycle management
- **Cancellation Policies**: Flexible cancellation and refund policies

### 🎯 **Additional Features**
- **Activity Management**: Curated activity recommendations and bookings
- **Content Management**: Blog posts, testimonials, and promotional content
- **Notification System**: Real-time notifications and email alerts
- **Wishlist Management**: Save and organize favorite destinations
- **Review & Rating System**: User feedback and rating capabilities

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2.1 with Django REST Framework
- **Language**: Python 3.9+
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery with Redis broker

### Frontend
- **Templates**: Django Templates with Bootstrap
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Forms**: Django Crispy Forms

### DevOps & Deployment
- **Containerization**: Docker & Docker Compose
- **Web Server**: Gunicorn (production)
- **Reverse Proxy**: Nginx (recommended)
- **Monitoring**: Django logging with structured output

### Security & Quality
- **Authentication**: JWT tokens with refresh mechanism
- **Authorization**: Role-based permissions (Admin/User/Guide)
- **Rate Limiting**: Configurable throttling
- **Testing**: Django Test Framework
- **Code Quality**: Pre-commit hooks and linting

## 📋 Prerequisites

Before running BoltTrip, ensure you have the following installed:

- **Python 3.9+**: [Download Python](https://python.org/downloads/)
- **Docker & Docker Compose**: [Install Docker](https://docs.docker.com/get-docker/)
- **Git**: [Install Git](https://git-scm.com/downloads)

## 🚀 Installation & Setup

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahmadsaif12/BoltTrip.git
   cd BoltTrip/bolttrip
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and Start Services**
   ```bash
   docker-compose up --build
   ```

4. **Run Database Migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create Superuser (Optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Option 2: Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/ahmadsaif12/BoltTrip.git
   cd BoltTrip/bolttrip
   ```

2. **Create Virtual Environment**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Configure your .env file
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
POSTGRES_DB=bolttrip
POSTGRES_USER=bolttrip_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=localhost  # or 'db' for Docker
POSTGRES_PORT=5432

# Redis Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Database Setup

The application supports PostgreSQL. For Docker deployment, the database is automatically configured. For local development, ensure PostgreSQL is running and create the database:

```sql
CREATE DATABASE bolttrip;
CREATE USER bolttrip_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE bolttrip TO bolttrip_user;
```

## 📖 Usage

### Accessing the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

### API Endpoints

The REST API provides comprehensive endpoints for all features:

#### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/token/refresh/` - Token refresh

#### Travel Packages
- `GET /api/packages/` - List packages
- `POST /api/packages/` - Create package (Admin only)
- `GET /api/packages/{id}/` - Package details

#### Bookings
- `GET /api/bookings/` - User bookings
- `POST /api/bookings/` - Create booking

#### Hotels
- `GET /api/hotel/hotels/` - List hotels
- `POST /api/hotel/hotels/` - Add hotel (Admin only)

### User Roles

1. **Travelers**: Book packages, manage profiles, view bookings
2. **Guides**: Manage profiles, view assigned bookings
3. **Administrators**: Full system management, content creation

## 🧪 Testing

### Running Tests

```bash
# Docker
docker-compose exec web python manage.py test

# Local
python manage.py test
```

### Test Coverage

Run tests with coverage reporting:

```bash
pip install coverage
coverage run manage.py test
coverage report
```

## 📚 API Documentation

Complete API documentation is available via Swagger UI:

- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

The documentation includes:
- Interactive API testing
- Request/response examples
- Authentication instructions
- Schema definitions

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure production database
- [ ] Set up proper SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL/TLS certificates
- [ ] Configure email settings
- [ ] Set up monitoring and logging
- [ ] Configure backup strategies

### Docker Production Deployment

1. **Update docker-compose.yml** for production settings
2. **Configure reverse proxy** (nginx recommended)
3. **Set up SSL certificates**
4. **Configure environment variables**
5. **Run database migrations**
6. **Collect static files**

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** and add tests
4. **Run tests**: `python manage.py test`
5. **Commit changes**: `git commit -am 'Add new feature'`
6. **Push to branch**: `git push origin feature/your-feature`
7. **Create Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- DRF for powerful API capabilities
- All contributors and users of BoltTrip

## 📞 Support

For support and questions:
- **Issues**: [GitHub Issues](https://github.com/ahmadsaif12/BoltTrip/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ahmadsaif12/BoltTrip/discussions)
- **Email**: ahmadsaif12@example.com

---

**Happy Traveling with BoltTrip! 🌍✈️**
