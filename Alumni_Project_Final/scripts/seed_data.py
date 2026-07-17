"""Seed the database with sample data."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole, UserStatus
from app.models.company import Company
from app.models.referral_request import ReferralRequest, RequestStatus


def seed_data():
    """Seed sample data."""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding data...")
        
        # Create admin user
        admin = User(
            email="admin@alumniconnect.com",
            password=hash_password("Admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            is_email_verified=True,
        )
        db.add(admin)
        
        # Create student
        student = User(
            email="student@example.com",
            password=hash_password("Student123"),
            full_name="John Student",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE,
            is_email_verified=True,
        )
        db.add(student)
        
        # Create alumni
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
        print("✅ Users created")
        
        # Create companies
        companies_data = [
            {"name": "Google", "industry": "Technology", "website": "https://google.com"},
            {"name": "Microsoft", "industry": "Technology", "website": "https://microsoft.com"},
            {"name": "Amazon", "industry": "E-commerce", "website": "https://amazon.com"},
            {"name": "Apple", "industry": "Technology", "website": "https://apple.com"},
            {"name": "Meta", "industry": "Social Media", "website": "https://meta.com"},
        ]
        
        companies = []
        for company_data in companies_data:
            company = Company(**company_data, is_verified=True)
            db.add(company)
            companies.append(company)
        
        db.commit()
        print("✅ Companies created")
        
        # Create sample referral request
        request = ReferralRequest(
            student_id=student.id,
            company_id=companies[0].id,
            position_title="Software Engineer",
            motivation="I am passionate about software development...",
            skills_match="Python, FastAPI, React",
            status=RequestStatus.APPROVED,
        )
        db.add(request)
        
        db.commit()
        print("✅ Sample referral request created")
        
        print("\n✨ Seeding complete!")
        print("\n📝 Demo Credentials:")
        print("   Admin:   admin@alumniconnect.com / Admin123")
        print("   Student: student@example.com / Student123")
        print("   Alumni:  alumni@example.com / Alumni123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
