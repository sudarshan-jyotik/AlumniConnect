"""Tests for enum normalization utilities."""
import pytest
from app.utils.normalize_enums import (
    normalize_user_enums,
    normalize_request_enums,
    normalize_submission_enums,
    normalize_notification_enums,
    normalize_enum_value,
    normalize_all_enums
)
from app.models.user import UserRole, UserStatus
from app.models.referral_request import RequestStatus, RequestPriority


class TestEnumNormalization:
    """Test cases for enum normalization utilities."""

    def test_normalize_user_enums_lowercase(self):
        """Test normalizing user enums that are already lowercase."""
        data = {
            "role": "student",
            "status": "active"
        }
        
        result = normalize_user_enums(data)
        
        assert result["role"] == "student"
        assert result["status"] == "active"

    def test_normalize_user_enums_uppercase(self):
        """Test normalizing uppercase user enums."""
        data = {
            "role": "STUDENT",
            "status": "ACTIVE"
        }
        
        result = normalize_user_enums(data)
        
        assert result["role"] == "student"
        assert result["status"] == "active"

    def test_normalize_user_enums_mixed_case(self):
        """Test normalizing mixed case user enums."""
        data = {
            "role": "Student",
            "status": "Active"
        }
        
        result = normalize_user_enums(data)
        
        assert result["role"] == "student"
        assert result["status"] == "active"

    def test_normalize_user_enums_from_enum_object(self):
        """Test normalizing enum objects."""
        data = {
            "role": UserRole.STUDENT,
            "status": UserStatus.ACTIVE
        }
        
        result = normalize_user_enums(data)
        
        assert result["role"] == "student"
        assert result["status"] == "active"

    def test_normalize_user_enums_with_none(self):
        """Test normalizing with None values."""
        data = {
            "role": None,
            "status": None
        }
        
        result = normalize_user_enums(data)
        
        # Should not crash, None values are skipped
        assert "role" in result
        assert "status" in result

    def test_normalize_user_enums_boolean_field(self):
        """Test normalizing boolean field."""
        data = {
            "is_email_verified": 1
        }
        
        result = normalize_user_enums(data)
        
        assert result["is_email_verified"] is True

    def test_normalize_request_enums(self):
        """Test normalizing request enums."""
        data = {
            "status": "PENDING",
            "priority": "HIGH"
        }
        
        result = normalize_request_enums(data)
        
        assert result["status"] == "pending"
        assert result["priority"] == "high"

    def test_normalize_request_enums_from_objects(self):
        """Test normalizing request enum objects."""
        data = {
            "status": RequestStatus.PENDING,
            "priority": RequestPriority.HIGH
        }
        
        result = normalize_request_enums(data)
        
        assert result["status"] == "pending"
        assert result["priority"] == "high"

    def test_normalize_submission_enums(self):
        """Test normalizing submission enums."""
        data = {
            "status": "APPROVED"
        }
        
        result = normalize_submission_enums(data)
        
        assert result["status"] == "approved"

    def test_normalize_notification_enums(self):
        """Test normalizing notification enums."""
        data = {
            "type": "REQUEST_APPROVED"
        }
        
        result = normalize_notification_enums(data)
        
        assert result["type"] == "request_approved"

    def test_normalize_enum_value_string(self):
        """Test normalizing single enum value as string."""
        result = normalize_enum_value("STUDENT")
        
        assert result == "student"

    def test_normalize_enum_value_enum_object(self):
        """Test normalizing single enum value as enum object."""
        result = normalize_enum_value(UserRole.STUDENT)
        
        assert result == "student"

    def test_normalize_enum_value_none(self):
        """Test normalizing None value."""
        result = normalize_enum_value(None)
        
        assert result is None

    def test_normalize_all_enums(self):
        """Test generic enum normalization function."""
        data = {
            "role": "STUDENT",
            "status": "ACTIVE",
            "name": "Test User"
        }
        
        result = normalize_all_enums(data, ["role", "status"])
        
        assert result["role"] == "student"
        assert result["status"] == "active"
        assert result["name"] == "Test User"  # Unchanged

    def test_normalize_all_enums_with_missing_fields(self):
        """Test normalizing when some enum fields are missing."""
        data = {
            "role": "STUDENT"
            # Missing status field
        }
        
        result = normalize_all_enums(data, ["role", "status"])
        
        assert result["role"] == "student"
        assert "status" not in result

    def test_normalize_preserves_other_fields(self):
        """Test that normalization preserves non-enum fields."""
        data = {
            "role": "STUDENT",
            "email": "test@test.com",
            "full_name": "Test User",
            "age": 25
        }
        
        result = normalize_user_enums(data)
        
        assert result["role"] == "student"
        assert result["email"] == "test@test.com"
        assert result["full_name"] == "Test User"
        assert result["age"] == 25

    def test_underscore_enums(self):
        """Test enums with underscores."""
        data = {
            "status": "SUBMITTED_TO_COMPANY"
        }
        
        result = normalize_submission_enums(data)
        
        assert result["status"] == "submitted_to_company"
