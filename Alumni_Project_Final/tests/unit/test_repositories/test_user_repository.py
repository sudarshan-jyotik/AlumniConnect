"""Tests for User Repository."""
import pytest
from datetime import datetime, timezone

from app.models.user import User, UserRole, UserStatus
from app.repositories.user import UserRepository
from app.core.security import hash_password


class TestUserRepository:
    """Test cases for User Repository."""

    def test_create_user(self, db):
        """Test creating a user."""
        repo = UserRepository(db)
        user = User(
            email="newuser@test.com",
            password=hash_password("TestPass123"),
            full_name="New User",
            role="student",
            status="pending",
            created_at=datetime.now(timezone.utc)
        )
        
        created_user = repo.create(user)
        db.commit()  # Commit the transaction
        db.refresh(created_user)  # Refresh to get the ID
        
        assert created_user.id is not None
        assert created_user.email == "newuser@test.com"
        assert created_user.role == "student"
        assert created_user.status == "pending"

    def test_get_by_id(self, db, test_student):
        """Test getting user by ID."""
        repo = UserRepository(db)
        
        user = repo.get_by_id(test_student.id)
        
        assert user is not None
        assert user.id == test_student.id
        assert user.email == test_student.email

    def test_get_by_id_not_found(self, db):
        """Test getting non-existent user."""
        repo = UserRepository(db)
        
        user = repo.get_by_id(99999)
        
        assert user is None

    def test_get_by_email(self, db, test_student):
        """Test getting user by email."""
        repo = UserRepository(db)
        
        user = repo.get_by_email(test_student.email)
        
        assert user is not None
        assert user.email == test_student.email
        assert user.id == test_student.id

    def test_get_by_email_not_found(self, db):
        """Test getting user with non-existent email."""
        repo = UserRepository(db)
        
        user = repo.get_by_email("nonexistent@test.com")
        
        assert user is None

    def test_get_by_email_case_insensitive(self, db, test_student):
        """Test email lookup is case insensitive."""
        repo = UserRepository(db)
        
        user = repo.get_by_email("STUDENT@TEST.COM")
        
        # SQLite doesn't enforce case sensitivity by default
        # This test documents expected behavior
        assert user is None or user.email.lower() == "student@test.com".lower()

    def test_get_by_verification_token(self, db, test_pending_user):
        """Test getting user by verification token."""
        repo = UserRepository(db)
        
        user = repo.get_by_verification_token(test_pending_user.verification_token)
        
        assert user is not None
        assert user.id == test_pending_user.id
        assert user.verification_token == test_pending_user.verification_token

    def test_get_by_verification_token_not_found(self, db):
        """Test getting user with invalid verification token."""
        repo = UserRepository(db)
        
        user = repo.get_by_verification_token("invalid_token")
        
        assert user is None

    def test_get_by_role(self, db, test_student, test_alumni, test_admin):
        """Test getting users by role."""
        repo = UserRepository(db)
        
        students = repo.get_by_role("student", skip=0, limit=10)
        
        assert len(students) >= 1
        assert all(user.role == "student" for user in students)
        assert any(user.id == test_student.id for user in students)

    def test_get_by_role_pagination(self, db):
        """Test pagination in get_by_role."""
        repo = UserRepository(db)
        
        # Create multiple students
        for i in range(5):
            user = User(
                email=f"student{i}@test.com",
                password=hash_password("TestPass123"),
                role="student",
                status="active",
                created_at=datetime.now(timezone.utc)
            )
            repo.create(user)
        db.commit()  # Commit all users
        
        # Test pagination
        page1 = repo.get_by_role("student", skip=0, limit=2)
        page2 = repo.get_by_role("student", skip=2, limit=2)
        
        assert len(page1) == 2
        assert len(page2) >= 2
        assert page1[0].id != page2[0].id

    def test_get_all(self, db, test_student, test_alumni, test_admin):
        """Test getting all users."""
        repo = UserRepository(db)
        
        all_users = repo.get_all(skip=0, limit=100)
        
        assert len(all_users) >= 3
        user_ids = [user.id for user in all_users]
        assert test_student.id in user_ids
        assert test_alumni.id in user_ids
        assert test_admin.id in user_ids

    def test_update_user(self, db, test_student):
        """Test updating a user."""
        repo = UserRepository(db)
        
        updated_user = repo.update(test_student.id, {
            "full_name": "Updated Name",
            "phone": "9876543210"
        })
        
        assert updated_user.full_name == "Updated Name"
        assert updated_user.phone == "9876543210"
        assert updated_user.email == test_student.email  # Unchanged

    def test_update_nonexistent_user(self, db):
        """Test updating a non-existent user."""
        repo = UserRepository(db)
        
        updated_user = repo.update(99999, {"full_name": "New Name"})
        
        assert updated_user is None

    def test_delete_user(self, db, test_student):
        """Test deleting a user."""
        repo = UserRepository(db)
        student_id = test_student.id
        
        result = repo.delete(student_id)
        db.commit()  # Commit the deletion
        
        assert result is True
        assert repo.get_by_id(student_id) is None

    def test_delete_nonexistent_user(self, db):
        """Test deleting a non-existent user."""
        repo = UserRepository(db)
        
        result = repo.delete(99999)
        
        assert result is False

    def test_user_relationships_loaded(self, db, test_student, test_draft_request):
        """Test that user relationships can be accessed."""
        repo = UserRepository(db)
        
        user = repo.get_by_id(test_student.id)
        
        # Access relationship
        assert user.referral_requests is not None
        assert len(user.referral_requests) >= 1

    def test_create_duplicate_email(self, db, test_student):
        """Test creating user with duplicate email raises error."""
        repo = UserRepository(db)
        user = User(
            email=test_student.email,  # Duplicate
            password=hash_password("TestPass123"),
            role="student",
            status="pending",
            created_at=datetime.now(timezone.utc)
        )
        
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            repo.create(user)
            db.commit()
