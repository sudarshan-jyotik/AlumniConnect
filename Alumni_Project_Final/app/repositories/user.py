"""User repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_verification_token(self, token: str) -> Optional[User]:
        """Get user by verification token."""
        return self.db.query(User).filter(User.verification_token == token).first()

    def get_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role."""
        return self.db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
