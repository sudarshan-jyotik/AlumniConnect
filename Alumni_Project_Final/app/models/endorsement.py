"""
Endorsement model - Users endorse referral requests.
Transformed from: Vote (upvote/downvote)
To: Endorsement (support with optional comment)
"""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Endorsement(Base):
    """
    Endorsement Model
    
    Users can endorse referral requests to show support.
    Similar to LinkedIn endorsements - shows the request is worthy.
    
    Transformed from Vote model (upvote/downvote) to Endorsement (support only).
    """
    __tablename__ = "endorsements"
    
    # ===== Composite Primary Key =====
    # User can endorse each request only once
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    request_id = Column(
        Integer,
        ForeignKey("referral_requests.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    # ===== Endorsement Details =====
    # Optional comment explaining why endorsing
    comment = Column(Text)
    
    # Strength of endorsement (1-5)
    # 1 = "Good candidate"
    # 3 = "Strong candidate"
    # 5 = "Exceptional candidate"
    strength = Column(Integer, default=3)
    
    # Type of endorsement
    endorsement_type = Column(String(50), default="general")  # general, technical, cultural_fit
    
    # ===== Timestamp =====
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    
    # ===== Relationships =====
    # User who gave the endorsement
    user = relationship("User", back_populates="endorsements")
    
    # Request being endorsed
    request = relationship("ReferralRequest", back_populates="endorsements")
    
    def __repr__(self):
        return f"<Endorsement: User {self.user_id} → Request {self.request_id} (strength={self.strength})>"
