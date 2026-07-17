"""
ReferralSubmission model - Alumni submit referrals for student requests.
Admins approve submissions before they are officially sent.
"""

from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class SubmissionStatus(str, PyEnum):
    """Status of referral submission."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    SUBMITTED_TO_COMPANY = "submitted_to_company"

    INTERVIEW_SCHEDULED = "interview_scheduled"
    OFFER_RECEIVED = "offer_received"

    REJECTED_BY_COMPANY = "rejected_by_company"
    WITHDRAWN = "withdrawn"


class ReferralSubmission(Base):
    """
    Referral Submission Model

    Alumni submit referrals for approved student referral requests.
    Requires admin approval before submission is finalized.
    """

    __tablename__ = "referral_submissions"

    # ===== Primary Key =====
    id = Column(Integer, primary_key=True, nullable=False)

    # ===== Foreign Keys =====

    request_id = Column(
        Integer,
        ForeignKey("referral_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    alumni_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ===== Submission Content =====

    notes = Column(Text)

    internal_reference_id = Column(String(100))

    confidence_level = Column(Integer, default=3)

    # ===== Status =====

    status = Column(
        Enum(SubmissionStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=SubmissionStatus.PENDING.value,
        index=True
    )

    # ===== Admin Approval Workflow =====

    approved_at = Column(DateTime)

    approved_by_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    rejection_reason = Column(Text)
    rejected_at = Column(DateTime)

    # ===== Outcome Tracking =====

    submitted_to_company_at = Column(DateTime)

    interview_date = Column(DateTime)
    interview_feedback = Column(Text)

    outcome_notes = Column(Text)
    outcome_updated_at = Column(DateTime)

    # ===== Timestamps =====

    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # ===== Relationships =====

    # Referral Request this submission belongs to
    request = relationship(
        "ReferralRequest",
        back_populates="submissions"
    )

    # Alumni User who submitted
    alumni = relationship(
        "User",
        foreign_keys=[alumni_id],
        back_populates="referral_submissions"
    )

    # Admin who approved
    approved_by = relationship(
        "User",
        foreign_keys=[approved_by_id],
        back_populates="approved_referral_submissions"
    )

    def __repr__(self):
        return f"<ReferralSubmission #{self.id} Request={self.request_id} Alumni={self.alumni_id}>"

    def is_successful(self) -> bool:
        return self.status == SubmissionStatus.OFFER_RECEIVED
