"""
AlumniProfile model - Alumni-specific profile information.
Linked one-to-one with User.
Matches the database schema and Alembic migration.
"""

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class AlumniProfile(Base):
    """
    Alumni Profile Model

    Stores extra information for alumni users only.
    Each alumni has exactly one profile.
    Admins verify alumni before they can submit referrals.
    """

    __tablename__ = "alumni_profiles"

    # ===== Primary Key =====
    id = Column(Integer, primary_key=True, nullable=False)

    # ===== One-to-One Link with User =====
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    # ===== Professional & Academic Info =====
    current_company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True
    )
    current_position = Column(String(200), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    graduation_year = Column(Integer, nullable=False, default=2024)
    degree = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    college_email = Column(String, nullable=True)
    linkedin_url = Column(String(500), nullable=True)

    # ===== Verification Workflow =====
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    verified_by_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    verification_notes = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    expertise_areas = Column(Text, nullable=True)

    # ===== Activity & Availability =====
    is_available = Column(Boolean, default=True)
    max_requests_per_month = Column(Integer, default=5)
    current_month_count = Column(Integer, default=0)
    referrals_given = Column(Integer, default=0)
    referrals_successful = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)

    # ===== Timestamps =====
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # ===== Relationships =====
    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="alumni_profile"
    )
    current_company = relationship(
        "Company",
        foreign_keys=[current_company_id]
    )
    verified_by = relationship(
        "User",
        foreign_keys=[verified_by_id],
        back_populates="verified_alumni_profiles"
    )

    # Compatibility properties
    @property
    def company(self):
        return self.current_company.name if self.current_company else None

    @property
    def job_title(self):
        return self.current_position

    def __repr__(self):
        return f"<AlumniProfile User={self.user_id}, Verified={self.is_verified}>"
