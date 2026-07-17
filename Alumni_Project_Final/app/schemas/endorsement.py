"""Endorsement schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class EndorsementCreate(BaseModel):
    request_id: int
    comment: Optional[str] = None
    strength: int = Field(default=3, ge=1, le=5)

class EndorsementOut(BaseModel):
    user_id: int
    request_id: int
    comment: Optional[str]
    strength: int
    created_at: datetime
    
    class Config:
        from_attributes = True
