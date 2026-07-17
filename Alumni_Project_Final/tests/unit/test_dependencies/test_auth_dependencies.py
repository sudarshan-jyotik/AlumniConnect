"""Tests for authentication dependencies."""
import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.dependencies.auth import (
    create_access_token,
    create_refresh_token,
    verify_access_token
)
from app.core.config import settings
from app.schemas.token import TokenData
from fastapi import HTTPException


class TestAuthDependencies:
    """Test cases for authentication dependency functions."""

    def test_create_access_token(self):
        """Test creating an access token."""
        data = {
            "user_id": 123,
            "role": "student"
        }
        
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50

    def test_access_token_contains_correct_claims(self):
        """Test that access token contains correct claims."""
        data = {
            "user_id": 456,
            "role": "alumni"
        }
        
        token = create_access_token(data)
        
        # Decode token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        assert payload["sub"] == "456"
        assert payload["role"] == "alumni"
        assert "exp" in payload
        assert "iat" in payload

    def test_access_token_expiration(self):
        """Test that access token has correct expiration."""
        data = {
            "user_id": 789,
            "role": "admin"
        }
        
        token = create_access_token(data)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        iat = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)
        
        # Check expiration is approximately correct
        expected_duration = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        actual_duration = exp - iat
        
        assert abs(actual_duration - expected_duration) < timedelta(seconds=5)

    def test_create_refresh_token(self):
        """Test creating a refresh token."""
        data = {"user_id": 123}
        
        token = create_refresh_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50

    def test_refresh_tokens_are_unique(self):
        """Test that refresh tokens are unique each time."""
        data = {"user_id": 123}
        
        token1 = create_refresh_token(data)
        token2 = create_refresh_token(data)
        
        assert token1 != token2

    def test_verify_access_token_success(self):
        """Test verifying a valid access token."""
        data = {
            "user_id": 123,
            "role": "student"
        }
        
        token = create_access_token(data)
        credentials_exception = HTTPException(status_code=401, detail="Could not validate")
        
        token_data = verify_access_token(token, credentials_exception)
        
        assert token_data.id == 123
        assert token_data.role == "student"

    def test_verify_access_token_invalid(self):
        """Test verifying an invalid token."""
        credentials_exception = HTTPException(status_code=401, detail="Could not validate")
        
        with pytest.raises(HTTPException):
            verify_access_token("invalid_token", credentials_exception)

    def test_verify_access_token_expired(self):
        """Test verifying an expired token."""
        # Create token that expired 1 hour ago
        data = {
            "user_id": 123,
            "role": "student",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            "iat": datetime.now(timezone.utc) - timedelta(hours=2),
            "sub": "123"
        }
        
        expired_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        credentials_exception = HTTPException(status_code=401, detail="Could not validate")
        
        with pytest.raises(HTTPException):
            verify_access_token(expired_token, credentials_exception)

    def test_verify_access_token_missing_sub(self):
        """Test verifying token without 'sub' claim."""
        # Create token without 'sub' claim
        data = {
            "role": "student",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            "iat": datetime.now(timezone.utc)
        }
        
        invalid_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        credentials_exception = HTTPException(status_code=401, detail="Could not validate")
        
        with pytest.raises(HTTPException):
            verify_access_token(invalid_token, credentials_exception)

    def test_create_access_token_default_role(self):
        """Test that access token has default role if not provided."""
        data = {
            "user_id": 999
            # No role provided
        }
        
        token = create_access_token(data)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        assert payload["role"] == "student"  # Default role

    def test_verify_token_data_type(self):
        """Test that verify_access_token returns TokenData type."""
        data = {
            "user_id": 123,
            "role": "alumni"
        }
        
        token = create_access_token(data)
        credentials_exception = HTTPException(status_code=401, detail="Could not validate")
        
        token_data = verify_access_token(token, credentials_exception)
        
        assert isinstance(token_data, TokenData)
        assert hasattr(token_data, 'id')
        assert hasattr(token_data, 'role')
