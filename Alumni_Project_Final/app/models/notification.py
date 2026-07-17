"""
Notification model - In-app and email notifications for users.
"""

from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class NotificationType(str, PyEnum):
    """Types of notifications in the system."""
    # Request related
    REQUEST_APPROVED = "request_approved"
    REQUEST_REJECTED = "request_rejected"
    REQUEST_EXPIRED = "request_expired"
    
    # Submission related
    NEW_SUBMISSION = "new_submission"
    SUBMISSION_APPROVED = "submission_approved"
    SUBMISSION_REJECTED = "submission_rejected"
    
    # Endorsement related
    NEW_ENDORSEMENT = "new_endorsement"
    
    # Interview/Outcome related
    INTERVIEW_SCHEDULED = "interview_scheduled"
    OFFER_RECEIVED = "offer_received"
    
    # Account related
    ACCOUNT_VERIFIED = "account_verified"
    WELCOME = "welcome"


class Notification(Base):
    """
    Notification Model
    
    In-app notifications for users. Can optionally send email as well.
    """
    __tablename__ = "notifications"
    
    # ===== Basic Information =====
    id = Column(Integer, primary_key=True, nullable=False)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # ===== Notification Content =====
    type = Column(Enum(NotificationType, values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Optional action URL (e.g., link to the request)
    action_url = Column(String(500))
    action_text = Column(String(100))  # e.g., "View Request"
    
    # ===== Related Entity =====
    # What entity this notification is about
    entity_type = Column(String(50))  # e.g., "referral_request", "submission"
    entity_id = Column(Integer)
    
    # ===== Status =====
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime)
    
    # ===== Email Delivery =====
    send_email = Column(Boolean, default=True)  # Whether to send email
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime)
    email_error = Column(Text)  # Error message if email failed
    
    # ===== Timestamps =====
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    
    # ===== Relationships =====
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification: {self.type} for User {self.user_id}>"
    
    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.now(timezone.utc)
    
    def mark_email_sent(self):
        """Mark email as sent."""
        self.email_sent = True
        self.email_sent_at = datetime.now(timezone.utc)
