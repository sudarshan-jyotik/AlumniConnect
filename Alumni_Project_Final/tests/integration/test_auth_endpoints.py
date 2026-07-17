"""Integration tests for authentication endpoints."""
import pytest


class TestAuthEndpoints:
    """Test cases for authentication API endpoints."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@test.com",
                "password": "TestPass123!",
                "full_name": "New User",
                "phone": "1234567890",
                "role": "student"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "newuser@test.com"
        assert data["data"]["role"] == "student"
        assert "password" not in data["data"]

    def test_register_duplicate_email(self, client, test_student):
        """Test registration with duplicate email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": test_student.email,
                "password": "TestPass123!",
                "full_name": "Duplicate User",
                "role": "student"
            }
        )
        
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False

    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "TestPass123!",
                "full_name": "Test User",
                "role": "student"
            }
        )
        
        assert response.status_code == 422  # Validation error

    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@test.com",
                "password": "weak",
                "full_name": "Test User",
                "role": "student"
            }
        )
        
        assert response.status_code == 422

    def test_register_alumni_role(self, client):
        """Test registration with alumni role."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "alumni@test.com",
                "password": "TestPass123!",
                "full_name": "Alumni User",
                "role": "alumni"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["role"] == "alumni"

    def test_login_success(self, client, test_student):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_student.email,
                "password": "TestPass123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_student):
        """Test login with wrong password."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_student.email,
                "password": "WrongPassword123"
            }
        )
        
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent@test.com",
                "password": "AnyPassword123"
            }
        )
        
        assert response.status_code == 403

    def test_verify_email_success(self, client, test_pending_user):
        """Test successful email verification."""
        response = client.get(
            f"/api/v1/auth/verify/{test_pending_user.verification_token}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_email_verified"] is True
        assert data["data"]["status"] == "active"

    def test_verify_email_invalid_token(self, client):
        """Test email verification with invalid token."""
        response = client.get(
            "/api/v1/auth/verify/invalid_token_xyz"
        )
        
        assert response.status_code == 404

    def test_refresh_token_success(self, client, test_student):
        """Test successful token refresh."""
        # First login
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_student.email,
                "password": "TestPass123"
            }
        )
        
        refresh_token = login_response.json()["data"]["refresh_token"]
        
        # Now refresh
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    def test_refresh_token_invalid(self, client):
        """Test token refresh with invalid token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        
        assert response.status_code == 403

    def test_logout_success(self, client, test_student):
        """Test successful logout."""
        # First login
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_student.email,
                "password": "TestPass123"
            }
        )
        
        refresh_token = login_response.json()["data"]["refresh_token"]
        
        # Now logout
        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_logout_with_invalid_token(self, client):
        """Test logout with invalid token doesn't fail."""
        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": "invalid_token"}
        )
        
        assert response.status_code == 200

    def test_register_missing_required_fields(self, client):
        """Test registration with missing required fields."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@test.com"
                # Missing password
            }
        )
        
        assert response.status_code == 422

    def test_login_missing_credentials(self, client):
        """Test login with missing credentials."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@test.com"
                # Missing password
            }
        )
        
        assert response.status_code == 422
