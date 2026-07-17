"""Test configuration and fixtures."""
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.dependencies.auth import create_access_token
from app.main import app
from app.models.user import User, UserRole, UserStatus
from app.models.company import Company
from app.models.alumni_profile import AlumniProfile
from app.models.referral_request import ReferralRequest, RequestStatus, RequestPriority
from app.models.referral_submission import ReferralSubmission, SubmissionStatus
from app.models.endorsement import Endorsement

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# ==================== USER FIXTURES ====================

@pytest.fixture
def test_student(db):
    """Create a test student user."""
    user = User(
        email="student@test.com",
        password=hash_password("TestPass123"),
        full_name="Test Student",
        phone="1234567890",
        role="student",
        status="active",
        is_email_verified=True,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_alumni(db):
    """Create a test alumni user."""
    user = User(
        email="alumni@test.com",
        password=hash_password("TestPass123"),
        full_name="Test Alumni",
        phone="1234567890",
        role="alumni",
        status="active",
        is_email_verified=True,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_admin(db):
    """Create a test admin user."""
    user = User(
        email="admin@test.com",
        password=hash_password("TestPass123"),
        full_name="Test Admin",
        phone="1234567890",
        role="admin",
        status="active",
        is_email_verified=True,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_pending_user(db):
    """Create a test pending user."""
    user = User(
        email="pending@test.com",
        password=hash_password("TestPass123"),
        full_name="Pending User",
        role="student",
        status="pending",
        is_email_verified=False,
        is_active=True,
        verification_token="test_token_123",
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ==================== TOKEN FIXTURES ====================

@pytest.fixture
def student_token(test_student):
    """Create access token for student."""
    return create_access_token({
        "user_id": test_student.id,
        "role": test_student.role
    })


@pytest.fixture
def alumni_token(test_alumni):
    """Create access token for alumni."""
    return create_access_token({
        "user_id": test_alumni.id,
        "role": test_alumni.role
    })


@pytest.fixture
def admin_token(test_admin):
    """Create access token for admin."""
    return create_access_token({
        "user_id": test_admin.id,
        "role": test_admin.role
    })


@pytest.fixture
def auth_headers_student(student_token):
    """Create authorization headers for student."""
    return {"Authorization": f"Bearer {student_token}"}


@pytest.fixture
def auth_headers_alumni(alumni_token):
    """Create authorization headers for alumni."""
    return {"Authorization": f"Bearer {alumni_token}"}


@pytest.fixture
def auth_headers_admin(admin_token):
    """Create authorization headers for admin."""
    return {"Authorization": f"Bearer {admin_token}"}


# ==================== COMPANY FIXTURES ====================

@pytest.fixture
def test_company(db):
    """Create a test company."""
    company = Company(
        name="Test Company Inc",
        industry="Technology",
        website="https://testcompany.com",
        description="A test company",
        is_active=True,
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@pytest.fixture
def test_company_2(db):
    """Create a second test company."""
    company = Company(
        name="Another Company Ltd",
        industry="Finance",
        website="https://anothercompany.com",
        description="Another test company",
        is_active=True,
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


# ==================== ALUMNI PROFILE FIXTURES ====================

@pytest.fixture
def test_alumni_profile(db, test_alumni, test_company):
    """Create a test alumni profile."""
    profile = AlumniProfile(
        user_id=test_alumni.id,
        current_company_id=test_company.id,
        current_position="Software Engineer",
        years_of_experience=5,
        graduation_year=2018,
        degree="Bachelor of Science",
        department="Computer Science",
        is_verified=True,
        is_available=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


# ==================== REFERRAL REQUEST FIXTURES ====================

@pytest.fixture
def test_draft_request(db, test_student, test_company):
    """Create a draft referral request."""
    request = ReferralRequest(
        student_id=test_student.id,
        company_id=test_company.id,
        position_title="Software Engineer",
        job_description="Test job description",
        location="San Francisco, CA",
        motivation="I am very motivated",
        status="draft",
        priority="medium",
        created_at=datetime.now(timezone.utc)
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@pytest.fixture
def test_pending_request(db, test_student, test_company):
    """Create a pending referral request."""
    request = ReferralRequest(
        student_id=test_student.id,
        company_id=test_company.id,
        position_title="Data Scientist",
        job_description="Data science role",
        location="New York, NY",
        motivation="Passionate about data",
        status="pending",
        priority="high",
        submitted_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc)
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@pytest.fixture
def test_approved_request(db, test_student, test_company, test_admin):
    """Create an approved referral request."""
    request = ReferralRequest(
        student_id=test_student.id,
        company_id=test_company.id,
        position_title="Product Manager",
        job_description="PM role",
        location="Seattle, WA",
        motivation="Great product experience",
        status="approved",
        priority="urgent",
        submitted_at=datetime.now(timezone.utc),
        approved_at=datetime.now(timezone.utc),
        approved_by_id=test_admin.id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


# ==================== REFERRAL SUBMISSION FIXTURES ====================

@pytest.fixture
def test_submission(db, test_approved_request, test_alumni):
    """Create a test referral submission."""
    submission = ReferralSubmission(
        request_id=test_approved_request.id,
        alumni_id=test_alumni.id,
        notes="Happy to refer",
        confidence_level=4,
        status="pending",
        created_at=datetime.now(timezone.utc)
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@pytest.fixture
def test_approved_submission(db, test_approved_request, test_alumni, test_admin):
    """Create an approved referral submission."""
    submission = ReferralSubmission(
        request_id=test_approved_request.id,
        alumni_id=test_alumni.id,
        notes="Excellent candidate",
        confidence_level=5,
        status="approved",
        approved_at=datetime.now(timezone.utc),
        approved_by_id=test_admin.id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


# ==================== ENDORSEMENT FIXTURES ====================

@pytest.fixture
def test_endorsement(db, test_approved_request, test_alumni):
    """Create a test endorsement."""
    endorsement = Endorsement(
        user_id=test_alumni.id,
        request_id=test_approved_request.id,
        comment="Great candidate!",
        strength=5,
        endorsement_type="technical",
        created_at=datetime.now(timezone.utc)
    )
    db.add(endorsement)
    db.commit()
    db.refresh(endorsement)
    return endorsement
