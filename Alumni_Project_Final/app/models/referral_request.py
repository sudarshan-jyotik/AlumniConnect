"""
ReferralRequest model - Students request job referrals from alumni.
"""

from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class RequestStatus(str, PyEnum):
    """Status of referral request through approval workflow."""
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FULFILLED = "fulfilled"
    CLOSED = "closed"


class RequestPriority(str, PyEnum):
    """Priority level of referral request."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ReferralRequest(Base):
    """
    Referral Request Model

    Students create requests for job referrals at specific companies.
    Flow: Draft → Pending → Approved → Fulfilled → Closed
    """

    __tablename__ = "referral_requests"

    # ===== Basic Information =====
    id = Column(Integer, primary_key=True, nullable=False)

    # Student who created the request
    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Company for which referral is requested
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ===== Job Details =====
    position_title = Column(String(200), nullable=False)
    job_description = Column(Text)
    job_url = Column(String(500))
    location = Column(String(200))

    # ===== Student Pitch =====
    motivation = Column(Text, nullable=False)
    skills_match = Column(Text)
    resume_url = Column(String(500))

    # ===== Status & Priority =====
    status = Column(
        Enum(RequestStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=RequestStatus.DRAFT.value,
        index=True,
    )

    priority = Column(
        Enum(RequestPriority, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=RequestPriority.MEDIUM.value,
    )

    # ===== Workflow Tracking =====
    submitted_at = Column(DateTime)

    # Admin approval
    approved_at = Column(DateTime)

    approved_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    # Admin rejection
    rejection_reason = Column(Text)
    rejected_at = Column(DateTime)

    # ===== Deadlines =====
    application_deadline = Column(DateTime)
    expires_at = Column(DateTime)

    # ===== Metrics =====
    view_count = Column(Integer, default=0)
    endorsement_count = Column(Integer, default=0)

    # ===== Flags =====
    is_urgent = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)

    # ===== Timestamps =====
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ======================================================
    # ✅ Relationships (FIXED)
    # ======================================================

    # Student who created the request
    student = relationship(
        "User",
        foreign_keys=[student_id],
        back_populates="referral_requests",
    )

    # Admin who approved the request
    approved_by = relationship(
        "User",
        foreign_keys=[approved_by_id],
        back_populates="approved_referral_requests",
    )

    # Company relationship
    company = relationship(
        "Company",
        back_populates="referral_requests",
    )

    # Submissions from alumni
    submissions = relationship(
        "ReferralSubmission",
        back_populates="request",
        cascade="all, delete-orphan",
    )

    # Endorsements
    endorsements = relationship(
        "Endorsement",
        back_populates="request",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<ReferralRequest #{self.id}: {self.position_title} ({self.status})>"
