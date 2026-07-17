"""
ReferralRequest Pydantic schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

from app.models.referral_request import RequestStatus, RequestPriority
from app.schemas.user import UserOut
from app.schemas.company import CompanyOut


class ReferralRequestBase(BaseModel):
    """Base referral request schema."""
    company_id: int
    position_title: str = Field(min_length=1, max_length=200)
    job_description: Optional[str] = None
    job_url: Optional[HttpUrl] = None
    location: Optional[str] = Field(None, max_length=200)
    motivation: str = Field(min_length=10)
    skills_match: Optional[str] = None
    priority: RequestPriority = RequestPriority.MEDIUM


class ReferralRequestCreate(ReferralRequestBase):
    """Schema for creating a referral request."""
    pass


class ReferralRequestUpdate(BaseModel):
    """Schema for updating a referral request."""
    position_title: Optional[str] = None
    job_description: Optional[str] = None
    job_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    motivation: Optional[str] = None
    skills_match: Optional[str] = None
    priority: Optional[RequestPriority] = None


class ReferralRequestOut(ReferralRequestBase):
    """Schema for referral request response."""
    id: int
    student_id: int
    status: RequestStatus
    submitted_at: Optional[datetime]
    approved_at: Optional[datetime]
    view_count: int
    endorsement_count: int
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    student: UserOut
    company: CompanyOut
    
    class Config:
        from_attributes = True


class ReferralRequestSubmit(BaseModel):
    """Schema for submitting request for approval."""
    pass


class ReferralRequestApprove(BaseModel):
    """Schema for approving a request."""
    pass


class ReferralRequestReject(BaseModel):
    """Schema for rejecting a request."""
    reason: str = Field(min_length=10)
