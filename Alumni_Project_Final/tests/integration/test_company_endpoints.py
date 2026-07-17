"""Integration tests for company endpoints."""
import pytest


class TestCompanyEndpoints:
    """Test cases for company API endpoints."""

    def test_get_all_companies(self, client, test_company, test_company_2):
        """Test getting all companies (public endpoint)."""
        response = client.get("/api/v1/companies/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) >= 2

    def test_get_single_company(self, client, test_company):
        """Test getting a single company."""
        response = client.get(f"/api/v1/companies/{test_company.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == test_company.id
        assert data["data"]["name"] == test_company.name

    def test_get_nonexistent_company(self, client):
        """Test getting non-existent company."""
        response = client.get("/api/v1/companies/99999")
        
        assert response.status_code == 404

    def test_search_companies(self, client, test_company):
        """Test searching companies."""
        response = client.get(f"/api/v1/companies/?search={test_company.name}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_create_company_as_admin(self, client, auth_headers_admin):
        """Test creating a company as admin."""
        response = client.post(
            "/api/v1/companies/",
            headers=auth_headers_admin,
            json={
                "name": "New Company Inc",
                "industry": "Technology",
                "website": "https://newcompany.com",
                "description": "A new company"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "New Company Inc"

    def test_create_company_as_non_admin(self, client, auth_headers_student):
        """Test that non-admin cannot create company."""
        response = client.post(
            "/api/v1/companies/",
            headers=auth_headers_student,
            json={
                "name": "New Company",
                "industry": "Tech"
            }
        )
        
        assert response.status_code == 403

    def test_update_company_as_admin(self, client, test_company, auth_headers_admin):
        """Test updating a company as admin."""
        response = client.put(
            f"/api/v1/companies/{test_company.id}",
            headers=auth_headers_admin,
            json={
                "industry": "Software",
                "description": "Updated description"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["industry"] == "Software"

    def test_delete_company_as_admin(self, client, test_company_2, auth_headers_admin):
        """Test deleting a company as admin."""
        response = client.delete(
            f"/api/v1/companies/{test_company_2.id}",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 204

    def test_pagination(self, client, db):
        """Test pagination of companies."""
        from app.models.company import Company
        from datetime import datetime, timezone
        
        # Create multiple companies
        for i in range(10):
            company = Company(
                name=f"Test Company {i}",
                industry="Test",
                is_active=True,
                created_at=datetime.now(timezone.utc)
            )
            db.add(company)
        db.commit()
        
        # Test pagination
        response = client.get("/api/v1/companies/?skip=0&limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 5
