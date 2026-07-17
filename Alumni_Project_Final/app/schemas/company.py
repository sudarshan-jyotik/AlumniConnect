"""
Company Pydantic schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class CompanyBase(BaseModel):
    """Base company schema."""
    name: str = Field(min_length=1, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    website: Optional[HttpUrl] = None
    careers_page: Optional[HttpUrl] = None
    description: Optional[str] = None
    headquarters: Optional[str] = Field(None, max_length=200)
    company_size: Optional[str] = Field(None, max_length=50)
    company_type: Optional[str] = Field(None, max_length=50)


class CompanyCreate(CompanyBase):
    """Schema for creating a company."""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating a company."""
    name: Optional[str] = Field(None, max_length=200)
    industry: Optional[str] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None


class CompanyOut(CompanyBase):
    """Schema for company response."""
    id: int
    is_active: bool
    is_verified: bool
    request_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
