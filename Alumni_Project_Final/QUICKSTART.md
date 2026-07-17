# 🚀 AlumniConnect - Quick Start

## ⚡ Start in 30 Seconds

```bash
cd alumniconnect-corrected
docker-compose up --build
```

**That's it!** 

- API running at: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: PostgreSQL on port 5433

---

## ✅ What Happens Automatically

When you run `docker-compose up --build`:

1. ✓ PostgreSQL database starts
2. ✓ Database migrations run automatically
3. ✓ All 8 tables are created
4. ✓ Application starts on port 8000

---

## 🔐 Default Test User

After starting, register a user via API or use the `/docs` interface:

**Register Student:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "Test@123",
    "role": "student",
    "full_name": "Test Student"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student@test.com&password=Test@123"
```

---

## 📊 Verify Everything is Working

### 1. Check Application Health
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### 2. Check Database Tables
```bash
docker-compose exec db psql -U postgres -d alumniconnect -c "\dt"
```

**Expected Output:**
```
 Schema |         Name          | Type  |  Owner   
--------+-----------------------+-------+----------
 public | alumni_profiles       | table | postgres
 public | companies             | table | postgres
 public | endorsements          | table | postgres
 public | notifications         | table | postgres
 public | referral_requests     | table | postgres
 public | referral_submissions  | table | postgres
 public | refresh_tokens        | table | postgres
 public | users                 | table | postgres
```

### 3. Check Migration Status
```bash
docker-compose exec app alembic current
```

**Expected Output:**
```
001_initial_schema (head)
```

---

## 🛠️ Common Commands

### View Logs
```bash
# All logs
docker-compose logs -f

# Just application logs
docker-compose logs -f app

# Just database logs
docker-compose logs -f db
```

### Stop Application
```bash
docker-compose down
```

### Restart Fresh (Clear Database)
```bash
docker-compose down -v
docker-compose up --build
```

### Access Database
```bash
docker-compose exec db psql -U postgres -d alumniconnect
```

---

## 📱 Using the API

### Interactive Documentation
Open in browser: http://localhost:8000/docs

This provides:
- ✓ Interactive API testing
- ✓ Request/response examples
- ✓ Try endpoints directly
- ✓ Authentication testing

### Alternative Documentation
Open in browser: http://localhost:8000/redoc

---

## 🧪 Testing Endpoints

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123",
    "role": "student",
    "full_name": "Test User"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=SecurePass123"
```

**Save the access_token from the response!**

### 3. Get Current User (Authenticated)
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🐛 Troubleshooting

### Application Won't Start

**Check if port is in use:**
```bash
lsof -i :8000
lsof -i :5433
```

**Change ports in docker-compose.yml if needed:**
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Database Connection Issues

**Verify database is running:**
```bash
docker-compose ps
```

**Check database logs:**
```bash
docker-compose logs db
```

### Migration Errors

**Check migration status:**
```bash
docker-compose exec app alembic current
```

**Manual migration:**
```bash
docker-compose exec app alembic upgrade head
```

### Clean Restart

If something is wrong, start fresh:
```bash
# Stop everything
docker-compose down -v

# Remove old images
docker-compose rm -f

# Rebuild and restart
docker-compose up --build
```

---

## 📚 Project Structure

```
alumniconnect-corrected/
├── app/
│   ├── models/          # 8 database models
│   ├── routers/         # API endpoints
│   ├── core/            # Configuration
│   └── ...
├── alembic/
│   └── versions/
│       └── 001_initial_schema.py  # Migration
├── docker-compose.yml   # Docker setup
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## 🎯 What's Included

- ✅ 8 Database Models
- ✅ 30+ API Endpoints
- ✅ JWT Authentication
- ✅ Role-Based Access (Student/Alumni/Admin)
- ✅ Complete Migration Script
- ✅ Docker Setup
- ✅ PostgreSQL Database
- ✅ Interactive API Docs

---

## 📖 Additional Resources

- **FIXES_APPLIED.md** - Details of all fixes made
- **README.md** - Full project documentation
- **API Docs** - http://localhost:8000/docs (when running)

---

## ✅ Success Checklist

When everything is working, you should see:

- [x] `docker-compose up --build` completes without errors
- [x] Logs show "Application Ready"
- [x] http://localhost:8000/health returns success
- [x] http://localhost:8000/docs shows Swagger UI
- [x] Can register and login successfully
- [x] Database has all 8 tables

---

**Need help?** Check `FIXES_APPLIED.md` for details on what was fixed!

🎉 **You're ready to start developing!**
