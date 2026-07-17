"""Referral Submission schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.referral_submission import SubmissionStatus

class ReferralSubmissionCreate(BaseModel):
    request_id: int
    notes: Optional[str] = None
    confidence_level: int = Field(default=3, ge=1, le=5)

class ReferralSubmissionUpdate(BaseModel):
    notes: Optional[str] = None
    internal_reference_id: Optional[str] = None

class ReferralSubmissionOut(BaseModel):
    id: int
    request_id: int
    alumni_id: int
    notes: Optional[str]
    status: SubmissionStatus
    confidence_level: int
    created_at: datetime
    
    class Config:
        from_attributes = True
