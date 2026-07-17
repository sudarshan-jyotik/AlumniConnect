"""Tests for Auth Service."""
import pytest
from datetime import datetime, timedelta, timezone

from app.core.exceptions import ForbiddenException, NotFoundException
from app.core.security import verify_password
from app.models.user import User, UserStatus
from app.repositories.user import UserRepository
from app.repositories.refresh_token import RefreshTokenRepository
from app.schemas.user import UserCreate
from app.services.auth import AuthService


class TestAuthService:
    """Test cases for Auth Service."""

    @pytest.fixture
    def auth_service(self, db):
        """Create auth service instance."""
        user_repo = UserRepository(db)
        refresh_token_repo = RefreshTokenRepository(db)
        return AuthService(user_repo, refresh_token_repo, db)

    def test_register_new_user(self, db, auth_service):
        """Test registering a new user."""
        user_data = UserCreate(
            email="newuser@test.com",
            password="TestPass123!",
            full_name="New User",
            phone="1234567890",
            role="student"
        )
        
        created_user = auth_service.register(user_data)
        
        assert created_user.id is not None
        assert created_user.email == "newuser@test.com"
        assert created_user.full_name == "New User"
        assert created_user.role == "student"
        assert created_user.status == "pending"
        assert created_user.verification_token is not None
        assert created_user.is_email_verified is False

    def test_register_duplicate_email(self, db, auth_service, test_student):
        """Test registering with duplicate email raises error."""
        user_data = UserCreate(
            email=test_student.email,
            password="TestPass123!",
            full_name="Duplicate User",
            role="student"
        )
        
        with pytest.raises(ForbiddenException) as exc_info:
            auth_service.register(user_data)
        
        assert "already registered" in str(exc_info.value).lower()

    def test_register_password_is_hashed(self, db, auth_service):
        """Test that password is properly hashed."""
        user_data = UserCreate(
            email="hashtest@test.com",
            password="PlainPassword123",
            full_name="Hash Test",
            role="student"
        )
        
        created_user = auth_service.register(user_data)
        
        # Password should be hashed
        assert created_user.password != "PlainPassword123"
        assert created_user.password.startswith("$2b$")
        
        # But should verify correctly
        assert verify_password("PlainPassword123", created_user.password)

    def test_authenticate_success(self, db, auth_service, test_student):
        """Test successful authentication."""
        # test_student has password "TestPass123"
        result = auth_service.authenticate(
            email=test_student.email,
            password="TestPass123"
        )
        
        assert "access_token" in result
        assert "refresh_token" in result
        assert "token_type" in result
        assert result["token_type"] == "bearer"

    def test_authenticate_wrong_password(self, db, auth_service, test_student):
        """Test authentication with wrong password."""
        with pytest.raises(ForbiddenException) as exc_info:
            auth_service.authenticate(
                email=test_student.email,
                password="WrongPassword123"
            )
        
        assert "invalid credentials" in str(exc_info.value).lower()

    def test_authenticate_nonexistent_user(self, db, auth_service):
        """Test authentication with non-existent user."""
        with pytest.raises(ForbiddenException) as exc_info:
            auth_service.authenticate(
                email="nonexistent@test.com",
                password="AnyPassword123"
            )
        
        assert "invalid credentials" in str(exc_info.value).lower()

    def test_authenticate_inactive_user(self, db, auth_service, test_student):
        """Test authentication with inactive user."""
        # Make user inactive
        test_student.is_active = False
        db.commit()
        
        with pytest.raises(ForbiddenException) as exc_info:
            auth_service.authenticate(
                email=test_student.email,
                password="TestPass123"
            )
        
        assert "inactive" in str(exc_info.value).lower()

    def test_authenticate_updates_last_login(self, db, auth_service, test_student):
        """Test that authentication updates last_login_at."""
        initial_last_login = test_student.last_login_at
        
        auth_service.authenticate(
            email=test_student.email,
            password="TestPass123"
        )
        
        db.refresh(test_student)
        assert test_student.last_login_at != initial_last_login
        assert test_student.last_login_at is not None

    def test_authenticate_creates_refresh_token(self, db, auth_service, test_student):
        """Test that authentication creates refresh token in database."""
        result = auth_service.authenticate(
            email=test_student.email,
            password="TestPass123"
        )
        
        refresh_token_repo = RefreshTokenRepository(db)
        token = refresh_token_repo.get_by_token(result["refresh_token"])
        
        assert token is not None
        assert token.user_id == test_student.id
        assert not token.revoked

    def test_verify_email_success(self, db, auth_service, test_pending_user):
        """Test successful email verification."""
        verified_user = auth_service.verify_email(test_pending_user.verification_token)
        
        assert verified_user.is_email_verified is True
        assert verified_user.verified_at is not None
        assert verified_user.verification_token is None
        assert verified_user.status == "active"

    def test_verify_email_invalid_token(self, db, auth_service):
        """Test email verification with invalid token."""
        with pytest.raises(NotFoundException) as exc_info:
            auth_service.verify_email("invalid_token_xyz")
        
        assert "invalid" in str(exc_info.value).lower()

    def test_refresh_access_token_success(self, db, auth_service, test_student):
        """Test successful token refresh."""
        # First authenticate to get refresh token
        auth_result = auth_service.authenticate(
            email=test_student.email,
            password="TestPass123"
        )
        
        old_refresh_token = auth_result["refresh_token"]
        
        # Now refresh
        new_tokens = auth_service.refresh_access_token(old_refresh_token)
        
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens
        assert new_tokens["refresh_token"] != old_refresh_token

    def test_refresh_access_token_invalid(self, db, auth_service):
        """Test token refresh with invalid token."""
        with pytest.raises(ForbiddenException) as exc_info:
            auth_service.refresh_access_token("invalid_token")
        
        assert "invalid" in str(exc_info.value).lower()

    def test_refresh_access_token_revoked(self, db, auth_service, test_student):
        """Test token refresh with revoked token."""
        # Authenticate and get refresh token
        auth_result = auth_service.authenticate(
            email=test_student.email,
            password="TestPass123"
        )
        
        refresh_token_value = auth_result["refresh_token"]
        
        # Revoke the token
        refresh_token_repo = RefreshTokenRepository(db)
        token = refresh_token_repo.get_by_token(refresh_token_value)
        refresh_token_repo.revoke(token)
        db.commit()
        
        # Try to refresh with revoked token
        with pytest.raises(ForbiddenException):
            auth_service.refresh_access_token(refresh_token_value)

    def test_refresh_access_token_inactive_user(self, db, auth_service, test_student):
        """Test token refresh with inactive user."""
        # Authenticate first
        auth_result = auth_service.authenticate(
            email=test_student.email,
            password="TestPass123"
        )
        
        # Make user inactive
        test_student.is_active = False
        db.commit()
        
        # Try to refresh
        with pytest.raises(ForbiddenException) as exc_info:
            auth_service.refresh_access_token(auth_result["refresh_token"])
        
        assert "inactive" in str(exc_info.value).lower()

    def test_logout_success(self, db, auth_service, test_student):
        """Test successful logout."""
        # Authenticate to get refresh token
        auth_result = auth_service.authenticate(
            email=test_student.email,
            password="TestPass123"
        )
        
        refresh_token_value = auth_result["refresh_token"]
        
        # Logout
        auth_service.logout(refresh_token_value)
        
        # Token should be revoked
        refresh_token_repo = RefreshTokenRepository(db)
        token = refresh_token_repo.get_by_token(refresh_token_value)
        assert token.revoked is True

    def test_logout_nonexistent_token(self, db, auth_service):
        """Test logout with non-existent token doesn't raise error."""
        # Should not raise error
        auth_service.logout("nonexistent_token")

    def test_register_alumni_role(self, db, auth_service):
        """Test registering user with alumni role."""
        user_data = UserCreate(
            email="alumni@test.com",
            password="TestPass123!",
            full_name="Alumni User",
            role="alumni"
        )
        
        created_user = auth_service.register(user_data)
        
        assert created_user.role == "alumni"

    def test_register_admin_role(self, db, auth_service):
        """Test registering user with admin role."""
        user_data = UserCreate(
            email="admin@test.com",
            password="TestPass123!",
            full_name="Admin User",
            role="admin"
        )
        
        created_user = auth_service.register(user_data)
        
        assert created_user.role == "admin"
