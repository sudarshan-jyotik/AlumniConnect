"""
Authentication service - FIXED VERSION with role in token.
"""

from datetime import datetime, timedelta, timezone
import secrets
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, NotFoundException
from app.core.security import hash_password, verify_password
from app.dependencies.auth import create_access_token, create_refresh_token
from app.models.refresh_token import RefreshToken
from app.models.user import User, UserStatus
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    """Authentication service for registration, login, and token management."""

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        db: Session,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.db = db

    def register(self, user_data: UserCreate) -> User:
        """Register a new user."""
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ForbiddenException("Email already registered")

        hashed_password = hash_password(user_data.password)
        
        # Generate verification token
        verification_token = secrets.token_urlsafe(32)

        new_user = User(
            email=user_data.email,
            password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role.value if hasattr(user_data.role, 'value') else str(user_data.role).lower(),
            verification_token=verification_token,
            status=UserStatus.PENDING.value,
        )

        self.user_repository.create(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        # TODO: Send verification email

        return new_user

    def authenticate(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens."""
        user = self.user_repository.get_by_email(email)

        if not user or not verify_password(password, user.password):
            raise ForbiddenException("Invalid credentials")

        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        # ✅ FIX: Include role in access token
        access_token = create_access_token({
            "user_id": user.id,
            "role": user.role.value  # Include role
        })

        refresh_token_value = create_refresh_token({"user_id": user.id})

        # Store refresh token
        refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token_value,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )

        self.refresh_token_repository.create(refresh_token)
        
        # Update last login
        user.last_login_at = datetime.now(timezone.utc)
        
        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_value,
            "token_type": "bearer",
        }

    def refresh_access_token(self, refresh_token_value: str) -> dict:
        """Refresh access token using refresh token rotation."""
        refresh_token = self.refresh_token_repository.get_by_token(refresh_token_value)

        if not refresh_token or refresh_token.revoked:
            raise ForbiddenException("Invalid refresh token")

        if refresh_token.is_expired():
            raise ForbiddenException("Refresh token expired")

        user = self.user_repository.get_by_id(refresh_token.user_id)
        if not user:
            raise NotFoundException("User not found")

        if not user.is_active:
            raise ForbiddenException("User account is inactive")

        # Revoke old token
        self.refresh_token_repository.revoke(refresh_token)

        # Create new tokens
        new_refresh_token_value = create_refresh_token({"user_id": user.id})
        new_refresh_token = RefreshToken(
            user_id=user.id,
            token=new_refresh_token_value,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        self.refresh_token_repository.create(new_refresh_token)

        # ✅ FIX: Include role in new access token
        access_token = create_access_token({
            "user_id": user.id,
            "role": user.role.value
        })

        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token_value,
            "token_type": "bearer",
        }

    def logout(self, refresh_token_value: str) -> None:
        """Logout by revoking refresh token."""
        refresh_token = self.refresh_token_repository.get_by_token(refresh_token_value)
        if refresh_token:
            self.refresh_token_repository.revoke(refresh_token)
            self.db.commit()

    def verify_email(self, token: str) -> User:
        """Verify user email with token."""
        user = self.user_repository.get_by_verification_token(token)
        if not user:
            raise NotFoundException("Invalid verification token")

        user.is_email_verified = True
        user.verified_at = datetime.now(timezone.utc)
        user.verification_token = None
        user.status = UserStatus.ACTIVE.value

        self.db.commit()
        self.db.refresh(user)

        return user
