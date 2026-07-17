"""Tests for security utilities."""
import pytest
from app.core.security import hash_password, verify_password


class TestSecurityFunctions:
    """Test cases for security utility functions."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert hashed.startswith("$2b$")
        assert len(hashed) > 50

    def test_hash_password_different_each_time(self):
        """Test that hashing same password produces different hashes."""
        password = "SamePassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2  # Different due to salt

    def test_verify_password_correct(self):
        """Test verifying correct password."""
        password = "CorrectPassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        password = "CorrectPassword123"
        wrong_password = "WrongPassword123"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive."""
        password = "Password123"
        hashed = hash_password(password)
        
        assert verify_password("password123", hashed) is False
        assert verify_password("PASSWORD123", hashed) is False

    def test_hash_empty_password(self):
        """Test hashing empty password."""
        password = ""
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0

    def test_hash_unicode_password(self):
        """Test hashing password with unicode characters."""
        password = "Test密码123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_hash_long_password(self):
        """Test hashing very long password."""
        password = "A" * 100
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_with_special_chars(self):
        """Test verifying password with special characters."""
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_with_spaces(self):
        """Test verifying password with spaces."""
        password = "Pass Word 123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("PassWord123", hashed) is False
