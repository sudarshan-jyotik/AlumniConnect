"""
User Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.STUDENT
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain a digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserOut(BaseModel):
    """Schema for user response."""
    id: int
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]
    role: UserRole
    status: UserStatus
    is_email_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    """Schema for password change."""
    old_password: str
    new_password: str = Field(min_length=8)
