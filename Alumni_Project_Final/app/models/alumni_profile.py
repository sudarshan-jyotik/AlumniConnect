"""
AlumniProfile model - Alumni-specific profile information.
Linked one-to-one with User.
Admins can verify alumni accounts.
"""

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
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

    # ===== Alumni Professional Info =====
    company = Column(String(200))
    job_title = Column(String(200))
    linkedin_url = Column(String(500))

    graduation_year = Column(Integer)

    bio = Column(Text)

    # ===== Verification Workflow =====
    is_verified = Column(Boolean, default=False)

    verified_by_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    verified_at = Column(DateTime)

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

    # Alumni user account
    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="alumni_profile"
    )

    # Admin who verified this alumni
    verified_by = relationship(
        "User",
        foreign_keys=[verified_by_id],
        back_populates="verified_alumni_profiles"
    )

    def __repr__(self):
        return f"<AlumniProfile User={self.user_id}, Verified={self.is_verified}>"
