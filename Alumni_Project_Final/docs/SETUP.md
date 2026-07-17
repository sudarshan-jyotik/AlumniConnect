# Setup Guide

## Local Development Setup

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Git
- Virtual environment tool

### 2. Database Setup

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo service postgresql start

# Create database
sudo -u postgres createdb alumniconnect

# Create user (optional)
sudo -u postgres psql
CREATE USER alumniconnect WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE alumniconnect TO alumniconnect;
\q
```

### 3. Application Setup

```bash
# Clone repo
git clone <your-repo-url>
cd alumniconnect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 4. Environment Configuration

Edit `.env`:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=alumniconnect
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password

SECRET_KEY=generate-with-openssl-rand-hex-32
```

Generate SECRET_KEY:
```bash
openssl rand -hex 32
```

### 5. Database Migrations

```bash
# Run migrations
alembic upgrade head

# Create new migration (after model changes)
alembic revision --autogenerate -m "description"
```

### 6. Seed Data

```bash
python scripts/seed_data.py
```

### 7. Run Application

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker Setup

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f app

# Run migrations in container
docker-compose exec app alembic upgrade head

# Seed data in container
docker-compose exec app python scripts/seed_data.py
```

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check connection
psql -h localhost -U postgres -d alumniconnect
```

### Migration Error

```bash
# Reset database
alembic downgrade base
alembic upgrade head
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

## Testing Setup

```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app
```
