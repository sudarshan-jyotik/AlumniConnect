"""Seed the database with sample data (idempotent & ASCII-safe)."""
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole, UserStatus
from app.models.company import Company
from app.models.alumni_profile import AlumniProfile
from app.models.referral_request import ReferralRequest, RequestStatus


def seed_data():
    """Seed sample data."""
    db = SessionLocal()
    
    try:
        print("[SEED] Starting database seeding...")
        
        # 1. Create or get Admin user
        admin = db.query(User).filter(User.email == "admin@alumniconnect.com").first()
        if not admin:
            admin = User(
                email="admin@alumniconnect.com",
                password=hash_password("Admin123"),
                full_name="Admin User",
                role=UserRole.ADMIN,
                status=UserStatus.ACTIVE,
                is_email_verified=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("[SEED] Admin user created")
        else:
            print("[SEED] Admin user already exists")
        
        # 2. Create or get Student user
        student = db.query(User).filter(User.email == "student@example.com").first()
        if not student:
            student = User(
                email="student@example.com",
                password=hash_password("Student123"),
                full_name="John Student",
                role=UserRole.STUDENT,
                status=UserStatus.ACTIVE,
                is_email_verified=True,
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            print("[SEED] Student user created")
        else:
            print("[SEED] Student user already exists")
        
        # 3. Create or get Alumni user
        alumni = db.query(User).filter(User.email == "alumni@example.com").first()
        if not alumni:
            alumni = User(
                email="alumni@example.com",
                password=hash_password("Alumni123"),
                full_name="Jane Alumni",
                role=UserRole.ALUMNI,
                status=UserStatus.ACTIVE,
                is_email_verified=True,
            )
            db.add(alumni)
            db.commit()
            db.refresh(alumni)
            print("[SEED] Alumni user created")
        else:
            print("[SEED] Alumni user already exists")
        
        # 4. Create companies
        companies_data = [
            {"name": "Google", "industry": "Technology", "website": "https://google.com"},
            {"name": "Microsoft", "industry": "Technology", "website": "https://microsoft.com"},
            {"name": "Amazon", "industry": "E-commerce", "website": "https://amazon.com"},
            {"name": "Netflix", "industry": "Entertainment", "website": "https://netflix.com"},
            {"name": "Meta", "industry": "Social Media", "website": "https://meta.com"},
            {"name": "Apple", "industry": "Technology", "website": "https://apple.com"},
        ]
        
        created_companies = []
        for company_data in companies_data:
            existing = db.query(Company).filter(Company.name == company_data["name"]).first()
            if not existing:
                company = Company(**company_data, is_verified=True)
                db.add(company)
                db.commit()
                db.refresh(company)
                created_companies.append(company)
            else:
                created_companies.append(existing)
        
        print(f"[SEED] Companies verified: {[c.name for c in created_companies]}")

        # 5. Create or get AlumniProfile
        profile = db.query(AlumniProfile).filter(AlumniProfile.user_id == alumni.id).first()
        if not profile:
            profile = AlumniProfile(
                user_id=alumni.id,
                current_company_id=created_companies[0].id if created_companies else None,
                current_position="Senior Software Engineer",
                graduation_year=2020,
                degree="B.Tech",
                department="Computer Science",
                linkedin_url="https://linkedin.com/in/jane-alumni",
                bio="Alumni working at Google, happy to refer qualified candidates.",
                is_verified=True,
                verified_by_id=admin.id,
                verified_at=datetime.now(timezone.utc),
                is_available=True,
            )
            db.add(profile)
            db.commit()
            print("[SEED] Alumni profile created")
        else:
            print("[SEED] Alumni profile already exists")
        
        # 6. Create sample referral request if none exists
        existing_req = db.query(ReferralRequest).first()
        if not existing_req and created_companies:
            sample_request = ReferralRequest(
                student_id=student.id,
                company_id=created_companies[0].id,
                position_title="Software Engineer (L3)",
                motivation="Passionate about large scale distributed systems and backend engineering.",
                skills_match="FastAPI, Python, React, PostgreSQL",
                status=RequestStatus.APPROVED.value,
                priority="medium",
                location="Remote",
            )
            db.add(sample_request)
            db.commit()
            print("[SEED] Sample approved referral request created")
        
        print("\n[SEED] Database seeding complete!")
        print("\nDemo Credentials:")
        print("   Admin:   admin@alumniconnect.com / Admin123")
        print("   Student: student@example.com / Student123")
        print("   Alumni:  alumni@example.com / Alumni123")
        
    except Exception as e:
        print(f"[ERROR] Seeding error: {e}")
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
