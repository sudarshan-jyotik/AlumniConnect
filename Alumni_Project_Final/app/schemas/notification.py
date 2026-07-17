"""Notification schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.notification import NotificationType

class NotificationOut(BaseModel):
    id: int
    type: NotificationType
    title: str
    message: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
