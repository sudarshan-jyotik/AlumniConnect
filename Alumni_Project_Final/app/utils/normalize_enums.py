"""
Enum normalization utilities to ensure case-insensitive enum handling.

PostgreSQL ENUM types are case-sensitive. This module provides utilities
to normalize enum values to match the database schema (all lowercase).
"""
from typing import Any, Dict
from enum import Enum


def normalize_user_enums(data: dict) -> dict:
    """
    Ensures all ENUM fields for the `users` table are lowercase.
    Handles: role, status
    """
    if "role" in data and data["role"]:
        value = data["role"]
        if isinstance(value, Enum):
            data["role"] = value.value.lower()
        else:
            data["role"] = str(value).lower()
    if "status" in data and data["status"]:
        value = data["status"]
        if isinstance(value, Enum):
            data["status"] = value.value.lower()
        else:
            data["status"] = str(value).lower()
    if "is_email_verified" in data:
        data["is_email_verified"] = bool(data["is_email_verified"])
    return data


def normalize_request_enums(data: dict) -> dict:
    """
    Ensures all ENUM fields for the `referral_requests` table are lowercase.
    Handles: status, priority
    """
    if "status" in data and data["status"]:
        value = data["status"]
        if isinstance(value, Enum):
            data["status"] = value.value.lower()
        else:
            data["status"] = str(value).lower()
    if "priority" in data and data["priority"]:
        value = data["priority"]
        if isinstance(value, Enum):
            data["priority"] = value.value.lower()
        else:
            data["priority"] = str(value).lower()
    return data


def normalize_submission_enums(data: dict) -> dict:
    """
    Ensures all ENUM fields for the `referral_submissions` table are lowercase.
    Handles: status
    """
    if "status" in data and data["status"]:
        value = data["status"]
        if isinstance(value, Enum):
            data["status"] = value.value.lower()
        else:
            data["status"] = str(value).lower()
    return data


def normalize_notification_enums(data: dict) -> dict:
    """
    Ensures all ENUM fields for the `notifications` table are lowercase.
    Handles: type
    """
    if "type" in data and data["type"]:
        value = data["type"]
        if isinstance(value, Enum):
            data["type"] = value.value.lower()
        else:
            data["type"] = str(value).lower()
    return data


def normalize_enum_value(value: Any) -> str:
    """
    Normalize any enum value to lowercase string.
    Handles both string values and enum objects.
    """
    if value is None:
        return None
    if isinstance(value, Enum):
        return value.value.lower()
    return str(value).lower()


def normalize_all_enums(data: Dict[str, Any], enum_fields: list) -> Dict[str, Any]:
    """
    Generic function to normalize all specified enum fields in a data dictionary.
    
    Args:
        data: Dictionary containing the data
        enum_fields: List of field names that contain enum values
        
    Returns:
        Dictionary with normalized enum values
    """
    for field in enum_fields:
        if field in data and data[field] is not None:
            data[field] = normalize_enum_value(data[field])
    return data
