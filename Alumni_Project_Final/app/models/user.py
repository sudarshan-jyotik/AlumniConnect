"""
User model with role-based system and verification workflow.
Fully corrected to avoid AmbiguousForeignKeysError.
"""

from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


# =====================================================
# ENUMS
# =====================================================

class UserRole(str, PyEnum):
    """User roles in the system."""
    STUDENT = "student"
    ALUMNI = "alumni"
    ADMIN = "admin"


class UserStatus(str, PyEnum):
    """User account status."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


# =====================================================
# USER MODEL
# =====================================================

class User(Base):
    """
    User model with comprehensive role + verification workflow.

    Roles:
    - STUDENT: Creates referral requests
    - ALUMNI: Submits referrals + endorsements
    - ADMIN: Approves requests/submissions + verifies alumni
    """

    __tablename__ = "users"

    # =====================================================
    # BASIC INFO
    # =====================================================

    id = Column(Integer, primary_key=True, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    full_name = Column(String(200))
    phone = Column(String(20))

    # =====================================================
    # ROLE + STATUS
    # =====================================================

    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), nullable=False, default=UserRole.STUDENT.value)
    status = Column(Enum(UserStatus, values_callable=lambda x: [e.value for e in x]), nullable=False, default=UserStatus.PENDING.value)

    # =====================================================
    # EMAIL VERIFICATION
    # =====================================================

    is_email_verified = Column(Boolean, default=False)

    verification_token = Column(String, unique=True, index=True)
    verification_sent_at = Column(DateTime)
    verified_at = Column(DateTime)

    # =====================================================
    # ACCOUNT MANAGEMENT
    # =====================================================

    is_active = Column(Boolean, nullable=False, default=True)
    last_login_at = Column(DateTime)

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # =====================================================
    # RELATIONSHIPS (ALL FIXED)
    # =====================================================

    # -------------------------------------------------
    # Alumni Profile (One-to-One)
    # -------------------------------------------------

    alumni_profile = relationship(
        "AlumniProfile",
        foreign_keys="AlumniProfile.user_id",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Admin verifying alumni profiles
    verified_alumni_profiles = relationship(
        "AlumniProfile",
        foreign_keys="AlumniProfile.verified_by_id",
        back_populates="verified_by",
    )

    # -------------------------------------------------
    # Referral Requests (Student creates)
    # ReferralRequest has:
    #   student_id → users.id
    #   approved_by_id → users.id
    # -------------------------------------------------

    referral_requests = relationship(
        "ReferralRequest",
        foreign_keys="ReferralRequest.student_id",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    # Requests approved by admin
    approved_referral_requests = relationship(
        "ReferralRequest",
        foreign_keys="ReferralRequest.approved_by_id",
        back_populates="approved_by",
    )

    # -------------------------------------------------
    # Referral Submissions (Alumni submits)
    # ReferralSubmission has:
    #   alumni_id → users.id
    #   approved_by_id → users.id
    # -------------------------------------------------

    referral_submissions = relationship(
        "ReferralSubmission",
        foreign_keys="ReferralSubmission.alumni_id",
        back_populates="alumni",
        cascade="all, delete-orphan",
    )

    # Submissions approved by admin
    approved_referral_submissions = relationship(
        "ReferralSubmission",
        foreign_keys="ReferralSubmission.approved_by_id",
        back_populates="approved_by",
    )

    # -------------------------------------------------
    # Endorsements (User endorses request)
    # Endorsement has:
    #   user_id → users.id
    # -------------------------------------------------

    endorsements = relationship(
        "Endorsement",
        foreign_keys="Endorsement.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # -------------------------------------------------
    # Notifications
    # Notification has:
    #   user_id → users.id
    # -------------------------------------------------

    notifications = relationship(
        "Notification",
        foreign_keys="Notification.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # =====================================================
    # HELPERS
    # =====================================================

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"

    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT

    def is_alumni(self) -> bool:
        return self.role == UserRole.ALUMNI

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def can_create_requests(self) -> bool:
        return self.role in [UserRole.STUDENT, UserRole.ALUMNI]

    def can_submit_referrals(self) -> bool:
        return self.role == UserRole.ALUMNI and self.status == UserStatus.ACTIVE

    def can_approve_requests(self) -> bool:
        return self.role == UserRole.ADMIN
