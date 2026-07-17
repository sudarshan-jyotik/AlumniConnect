"""
RefreshToken model for JWT token rotation.
"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class RefreshToken(Base):
    """Refresh token model for token rotation."""
    
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=7)
    )
    revoked = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    def __repr__(self):
        return f"<RefreshToken {self.id} for User {self.user_id}>"
    
    def is_expired(self) -> bool:
        """Check if token is expired."""
        now = datetime.now(timezone.utc)
        expires_at = self.expires_at
        
        # Handle timezone-naive datetime from SQLite
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        return now > expires_at
    
    def is_valid(self) -> bool:
        """Check if token is valid (not revoked and not expired)."""
        return not self.revoked and not self.is_expired()
