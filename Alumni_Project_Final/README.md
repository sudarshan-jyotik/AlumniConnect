# AlumniConnect — Backend (`Alumni_Project_Final`)

FastAPI + PostgreSQL backend for the AlumniConnect placement referral platform. Handles auth, referral request workflows, and admin approvals behind a role-based REST API.

> Part of the [AlumniConnect monorepo](../README.md). See the [frontend README](../Alumni_Frontend/README.md) for the React/TypeScript client.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org)

## Features

- Role-based authentication (Student, Alumni, Admin) with JWT access + refresh tokens
- Referral request workflow with admin approval/rejection
- Company management
- Alumni verification process
- 8-table relational schema — foreign-key constraints, cascade deletes, indexed columns on frequently-queried fields
- RESTful API, documented via Swagger/ReDoc

## Tech Stack

Python 3.11+ · FastAPI · SQLAlchemy · Alembic · PostgreSQL · JWT · pytest

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 15+

### Installation

```bash
git clone https://github.com/sudarshan-jyotik/alumniconnect.git
cd alumniconnect/Alumni_Project_Final

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env            # set DATABASE_URL, JWT_SECRET

createdb alumniconnect
alembic upgrade head

# optional: seed demo data
python scripts/seed_data.py

uvicorn app.main:app --reload
```

### Access
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Demo credentials (local/dev seed data only)

| Role | Email | Password |
|---|---|---|
| Admin | admin@alumniconnect.com | Admin123 |
| Student | student@example.com | Student123 |
| Alumni | alumni@example.com | Alumni123 |

## API Reference

### Auth
```http
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/verify/{token}
```

### Referral Requests
```http
GET    /api/v1/referral-requests/
POST   /api/v1/referral-requests/
GET    /api/v1/referral-requests/{id}
PUT    /api/v1/referral-requests/{id}
POST   /api/v1/referral-requests/{id}/submit
DELETE /api/v1/referral-requests/{id}
```

### Admin
```http
GET  /api/v1/admin/pending-requests
POST /api/v1/admin/requests/{id}/approve
POST /api/v1/admin/requests/{id}/reject
```

Full schema and try-it-out available at `/docs` once running.

## Database Schema

8 tables — users, student profiles, alumni profiles, companies, referral requests, roles/permissions, and status/audit tracking — with foreign-key constraints, cascade deletes, and indexes on frequently-queried columns (e.g. `user_id`, `status`) for query performance.

## Testing

```bash
pytest                                    # run all tests
pytest --cov=app --cov-report=html        # with coverage report
pytest tests/integration/test_auth.py -v  # a specific test file
```

## CORS

The API is configured to accept requests from the frontend's origin (`http://localhost:3000` in development) via `CORSMiddleware`. Update `allow_origins` in `app/main.py` for other environments.

## Project Structure

```
Alumni_Project_Final/
├── app/
│   ├── core/              # config, security helpers
│   ├── models/             # SQLAlchemy models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── repositories/        # data access layer
│   ├── services/             # business logic
│   ├── routers/               # API endpoints
│   ├── dependencies/           # FastAPI dependency injection (auth guards, etc.)
│   ├── middleware/
│   └── main.py                 # application entry point
├── tests/
├── alembic/                # database migrations
├── scripts/                # seed_data.py and other utility scripts
└── requirements.txt
```

## Roadmap

Ideas for future iterations — not yet built:
- Email notifications on referral status changes
- Rate limiting per user/role
- Audit logging for admin actions

## License

MIT
