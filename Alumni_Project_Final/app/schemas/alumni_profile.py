"""Alumni Profile schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class AlumniProfileBase(BaseModel):
    current_company_id: Optional[int] = None
    current_position: Optional[str] = Field(None, max_length=200)
    years_of_experience: Optional[int] = Field(None, ge=0)
    graduation_year: int = Field(ge=1950, le=2030)
    degree: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    linkedin_url: Optional[HttpUrl] = None
    bio: Optional[str] = None
    is_available: bool = True

class AlumniProfileCreate(AlumniProfileBase):
    pass

class AlumniProfileUpdate(BaseModel):
    current_company_id: Optional[int] = None
    current_position: Optional[str] = None
    bio: Optional[str] = None
    is_available: Optional[bool] = None

class AlumniProfileOut(AlumniProfileBase):
    id: int
    user_id: int
    is_verified: bool
    referrals_given: int
    success_rate: float
    created_at: datetime
    
    class Config:
        from_attributes = True
