"""
Generic API response schemas.
"""

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    success: bool = Field(default=True)
    message: str = Field(min_length=1, max_length=500)
    data: Optional[T] = Field(default=None)
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    success: bool = False
    message: str = Field(min_length=1, max_length=500)
    detail: Optional[str] = None
    errors: Optional[list[dict]] = None
