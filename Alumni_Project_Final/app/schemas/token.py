"""
Token Pydantic schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""
    id: Optional[int] = None
    role: str


class LogoutRequest(BaseModel):
    """Schema for logout request."""
    refresh_token: str = Field(min_length=1)


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str = Field(min_length=1)
