# Alumni Referral System - Complete with Comprehensive Tests

A FastAPI-based alumni referral platform connecting students with alumni for job referrals.

## 🎯 Project Status

✅ **Complete Implementation**  
✅ **Comprehensive Test Suite** (80-85% Coverage)  
✅ **PostgreSQL Enum Issues Fixed**  
✅ **Production Ready**

---

## 📋 Features

### Core Functionality
- ✅ User authentication (JWT-based)
- ✅ Role-based access control (Student, Alumni, Admin)
- ✅ Email verification workflow
- ✅ Referral request management
- ✅ Admin approval system
- ✅ Company database
- ✅ Alumni profiles
- ✅ Endorsement system
- ✅ Notification system

### Technical Features
- ✅ RESTful API with FastAPI
- ✅ PostgreSQL database
- ✅ SQLAlchemy ORM
- ✅ Alembic migrations
- ✅ JWT authentication
- ✅ Rate limiting
- ✅ CORS middleware
- ✅ Security headers
- ✅ Comprehensive error handling

---

## 🧪 Testing

### Test Coverage: 80-85%

**150+ Comprehensive Tests** covering:

#### Unit Tests (90+ tests)
- ✅ Repository layer (40+ tests)
  - User, Company, Referral Request repositories
  - CRUD operations, queries, relationships
- ✅ Service layer (35+ tests)
  - Authentication, Referral Request services
  - Business logic, validation, authorization
- ✅ Utility functions (25+ tests)
  - Enum normalization, password hashing
- ✅ Dependencies (15+ tests)
  - JWT token creation and validation

#### Integration Tests (60+ tests)
- ✅ Authentication endpoints (20 tests)
- ✅ Referral request endpoints (25 tests)
- ✅ Company endpoints (15 tests)
- ✅ Admin operations

### Running Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_services/test_auth_service.py
```

For detailed testing documentation, see:
- **[TESTING.md](TESTING.md)** - Complete testing guide
- **[TEST_COVERAGE_SUMMARY.md](TEST_COVERAGE_SUMMARY.md)** - Detailed coverage breakdown

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- pip

### Installation

1. **Clone and setup**
```bash
cd Alumni_Project_Final
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. **Initialize database**
```bash
alembic upgrade head
```

4. **Run application**
```bash
uvicorn app.main:app --reload
```

5. **Run tests**
```bash
pytest
```

The API will be available at `http://localhost:8000`  
API documentation at `http://localhost:8000/docs`

---

## 📁 Project Structure

```
Alumni_Project_Final/
├── app/
│   ├── core/                    # Core functionality
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database setup
│   │   ├── exceptions.py       # Custom exceptions
│   │   ├── rate_limit.py       # Rate limiting
│   │   └── security.py         # Password hashing
│   ├── dependencies/           # FastAPI dependencies
│   │   ├── auth.py            # JWT auth
│   │   └── roles.py           # Role checks
│   ├── middleware/            # Custom middleware
│   ├── models/                # SQLAlchemy models
│   ├── repositories/          # Data access layer
│   ├── routers/               # API endpoints
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── utils/                 # Utility functions
│   └── main.py                # Application entry
├── alembic/                   # Database migrations
├── tests/                     # Comprehensive test suite
│   ├── conftest.py           # Test fixtures
│   ├── unit/                 # Unit tests
│   │   ├── test_repositories/
│   │   ├── test_services/
│   │   ├── test_utils/
│   │   └── test_dependencies/
│   └── integration/          # Integration tests
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
├── TESTING.md               # Testing documentation
├── TEST_COVERAGE_SUMMARY.md # Coverage details
└── README.md                # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/alumni_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
```

---

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/verify/{token}` - Verify email

### Referral Requests
- `GET /api/v1/referral-requests/` - List requests
- `POST /api/v1/referral-requests/` - Create request
- `GET /api/v1/referral-requests/{id}` - Get request
- `PUT /api/v1/referral-requests/{id}` - Update request
- `DELETE /api/v1/referral-requests/{id}` - Delete request
- `POST /api/v1/referral-requests/{id}/submit` - Submit for approval

### Admin
- `GET /api/v1/admin/pending-requests` - Get pending requests
- `POST /api/v1/admin/requests/{id}/approve` - Approve request
- `POST /api/v1/admin/requests/{id}/reject` - Reject request

### Companies
- `GET /api/v1/companies/` - List companies
- `POST /api/v1/companies/` - Create company (admin)
- `GET /api/v1/companies/{id}` - Get company
- `PUT /api/v1/companies/{id}` - Update company (admin)
- `DELETE /api/v1/companies/{id}` - Delete company (admin)

Full API documentation available at `/docs` when running the application.

---

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Register or login to receive tokens
2. Include token in Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```
3. Tokens expire after 30 minutes (configurable)
4. Use refresh token to get new access token

---

## 👥 User Roles

### Student
- Create and manage referral requests
- View own requests
- Submit requests for approval

### Alumni
- View approved requests
- Submit referrals
- Endorse requests

### Admin
- Approve/reject requests
- Manage companies
- View all requests
- Administrative operations

---

## 🐛 Bug Fixes

### PostgreSQL Enum Case-Sensitivity Fixed

This version includes comprehensive fixes for PostgreSQL enum case sensitivity issues:

- ✅ Fixed hardcoded enum strings in routers
- ✅ Enhanced enum normalization utilities
- ✅ Proper enum value conversion throughout the codebase
- ✅ All enum values use lowercase to match PostgreSQL schema

See [COMPLETE_ENUM_FIXES_V2.md](COMPLETE_ENUM_FIXES_V2.md) for details.

---

## 📦 Dependencies

### Core
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- PostgreSQL (psycopg2-binary 2.9.9)
- Alembic 1.13.1

### Authentication
- python-jose 3.3.0
- passlib 1.7.4

### Testing
- pytest 7.4.4
- pytest-cov 4.1.0
- pytest-asyncio 0.23.3
- httpx 0.26.0

See [requirements.txt](requirements.txt) for complete list.

---

## 🧩 Database Schema

### Main Tables
- **users** - User accounts with roles
- **companies** - Company database
- **alumni_profiles** - Alumni profiles and experience
- **referral_requests** - Job referral requests
- **referral_submissions** - Alumni referral submissions
- **endorsements** - Request endorsements
- **notifications** - User notifications
- **refresh_tokens** - JWT refresh tokens

### Enums
- UserRole: student, alumni, admin
- UserStatus: pending, active, suspended, inactive
- RequestStatus: draft, pending, approved, rejected, fulfilled, closed
- RequestPriority: low, medium, high, urgent
- SubmissionStatus: pending, approved, rejected, submitted_to_company, etc.
- NotificationType: Various notification types

---

## 🔄 Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View history
alembic history
```

---

## 🚦 Development Workflow

1. **Create feature branch**
2. **Write tests first** (TDD)
3. **Implement feature**
4. **Run tests**: `pytest`
5. **Check coverage**: `pytest --cov`
6. **Commit with meaningful message**
7. **Create pull request**

---

## 📈 Performance

- Rate limiting: 60 requests/minute (configurable)
- Connection pooling enabled
- Query optimization with indexes
- Efficient pagination
- Minimal N+1 queries

---

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- CORS configuration
- Security headers middleware
- SQL injection prevention (SQLAlchemy)
- XSS protection
- Rate limiting

---

## 📝 Code Quality

### Standards
- PEP 8 compliant
- Type hints throughout
- Comprehensive docstrings
- Error handling
- Input validation

### Tools
- black - Code formatting
- isort - Import sorting
- flake8 - Linting
- pytest - Testing

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Write tests for new features
4. Ensure tests pass
5. Maintain or improve coverage
6. Submit pull request

---

## 📄 License

MIT License

---

## 📞 Support

For issues or questions:
- Check existing documentation
- Review test examples
- Check API documentation at `/docs`

---

## 🎉 Acknowledgments

- FastAPI framework
- SQLAlchemy ORM
- Pytest testing framework
- PostgreSQL database

---

**Version**: 2.0  
**Last Updated**: February 13, 2026  
**Status**: Production Ready with Comprehensive Tests
