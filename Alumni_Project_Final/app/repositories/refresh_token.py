"""Refresh Token repository."""
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get refresh token by token string."""
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def create(self, refresh_token: RefreshToken) -> RefreshToken:
        """Create a new refresh token."""
        self.db.add(refresh_token)
        return refresh_token

    def revoke(self, refresh_token: RefreshToken) -> None:
        """Revoke a refresh token."""
        refresh_token.revoked = True

    def delete_expired(self) -> int:
        """Delete all expired refresh tokens."""
        count = self.db.query(RefreshToken).filter(
            RefreshToken.expires_at < datetime.now(timezone.utc)
        ).delete()
        return count
