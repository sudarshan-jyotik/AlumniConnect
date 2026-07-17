# AlumniConnect — Placement Referral Platform

A full-stack platform that connects students seeking job referrals with alumni willing to help — with role-based access, an admin approval workflow, and a typed REST API contract between a FastAPI backend and a React/TypeScript frontend.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6.svg)](https://www.typescriptlang.org)

## Overview

Students post referral requests for specific companies/roles; alumni review and submit referrals; admins approve or reject requests. Built as two connected projects in one repo — a FastAPI backend and a React/TypeScript frontend — with a full auth flow and relational schema behind it.

## Repository Structure

```
alumniconnect/
├── Alumni_Project_Final/     # Backend — FastAPI + PostgreSQL
└── Alumni_Frontend/          # Frontend — React + TypeScript + Vite
```

## Key Features

- Role-based access control (Student / Alumni / Admin)
- JWT authentication with protected routes on the frontend
- Referral request workflow: create → submit → admin approve/reject
- 8-table relational schema with foreign-key constraints, cascade deletes, and indexed columns for query performance
- Typed REST API contract shared between backend and frontend
- Company directory and alumni verification flow

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, Uvicorn |
| Database | PostgreSQL, SQLAlchemy, Alembic (migrations) |
| Frontend | React 18, TypeScript, Vite |
| Frontend state/data | Zustand, React Query |
| Frontend forms | React Hook Form, Zod validation |
| Auth | JWT, role-based route guards (both layers) |
| Styling | TailwindCSS |

## Architecture

```
React + TypeScript (Vite)
  │  Axios client, typed REST calls, React Query cache
  ▼
FastAPI backend
  │  JWT auth, role-based route guards
  │  SQLAlchemy ORM
  ▼
PostgreSQL — 8-table schema, FK constraints, cascade deletes, indexed columns
```

## Getting Started

Run the backend and frontend in two separate terminals.

### 1. Backend

```bash
cd Alumni_Project_Final
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env            # set DATABASE_URL, JWT_SECRET

alembic upgrade head
uvicorn app.main:app --reload
```
API: `http://localhost:8000` · Docs: `http://localhost:8000/docs`

### 2. Frontend

```bash
cd Alumni_Frontend
npm install
cp .env.example .env            # set VITE_API_URL=http://localhost:8000/api/v1
npm run dev
```
App: `http://localhost:3000`

## Demo Credentials

For local development only — seed with `python scripts/seed_data.py` in the backend directory, then log in as:

| Role | Email | Password |
|---|---|---|
| Admin | admin@alumniconnect.com | Admin123 |
| Student | student@example.com | Student123 |
| Alumni | alumni@example.com | Alumni123 |

> These are dev-only seed accounts — not present in any deployed/production instance.

## API Overview

```http
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh

GET    /api/v1/referral-requests/
POST   /api/v1/referral-requests/
GET    /api/v1/referral-requests/{id}
POST   /api/v1/referral-requests/{id}/submit

GET    /api/v1/admin/pending-requests
POST   /api/v1/admin/requests/{id}/approve
POST   /api/v1/admin/requests/{id}/reject
```
Full interactive docs at `/docs` once the backend is running.

## Database Schema

8 tables covering users, student profiles, alumni profiles, referral requests, companies, roles/permissions, and status/audit tracking — with foreign-key constraints, cascade deletes, and indexes on frequently-queried columns (e.g. `user_id`, `status`).

## Testing

```bash
cd Alumni_Project_Final
pytest --cov=app --cov-report=html
```

## Individual Project Docs

- [Backend README](./Alumni_Project_Final/README.md)
- [Frontend README](./Alumni_Frontend/README.md)

## Roadmap

Ideas for future iterations — not yet built:
- Real-time notifications (WebSockets) for referral status changes
- Resume/file upload support
- Search and filtering for referral opportunities by company/role

## License

MIT

## Author

Sudarshan Jyotik — [GitHub](https://github.com/sudarshan-jyotik) · [LinkedIn](https://linkedin.com/in/sudarshan-jyotik)
