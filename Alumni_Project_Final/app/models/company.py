"""
Company model - Companies where students seek referrals.
"""

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Company(Base):
    """
    Company Model
    
    Represents companies where students can request referrals.
    Can be added by admin or students (pending approval).
    """
    __tablename__ = "companies"
    
    # ===== Basic Information =====
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), unique=True, nullable=False, index=True)
    
    # ===== Details =====
    industry = Column(String(100))  # e.g., "Technology", "Finance"
    website = Column(String(500))
    careers_page = Column(String(500))  # Link to careers/jobs page
    logo_url = Column(String(500))
    description = Column(Text)
    
    # ===== Location =====
    headquarters = Column(String(200))  # e.g., "San Francisco, CA"
    
    # ===== Size & Type =====
    company_size = Column(String(50))  # e.g., "1000-5000", "5000+"
    company_type = Column(String(50))  # e.g., "Public", "Private", "Startup"
    
    # ===== Status =====
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Admin verified
    
    # ===== Stats =====
    request_count = Column(Integer, default=0)  # Number of requests for this company
    
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
    # Referral requests for this company
    referral_requests = relationship(
        "ReferralRequest",
        back_populates="company",
        cascade="all, delete-orphan"
    )
    
    # Alumni working at this company (via AlumniProfile)
    # This will be set up when we create AlumniProfile model
    
    def __repr__(self):
        return f"<Company: {self.name}>"
    
    def increment_request_count(self):
        """Increment the request count."""
        self.request_count += 1
