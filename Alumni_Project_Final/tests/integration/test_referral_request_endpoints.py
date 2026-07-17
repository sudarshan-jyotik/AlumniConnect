"""Integration tests for referral request endpoints."""
import pytest


class TestReferralRequestEndpoints:
    """Test cases for referral request API endpoints."""

    def test_create_request_as_student(self, client, test_student, test_company, auth_headers_student):
        """Test creating a referral request as student."""
        response = client.post(
            "/api/v1/referral-requests/",
            headers=auth_headers_student,
            json={
                "company_id": test_company.id,
                "position_title": "Software Engineer",
                "job_description": "Great opportunity",
                "location": "San Francisco",
                "motivation": "Very interested in this role and company culture",
                "priority": "medium"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["position_title"] == "Software Engineer"
        assert data["data"]["status"] == "draft"

    def test_create_request_unauthorized(self, client, test_company):
        """Test creating request without authentication."""
        response = client.post(
            "/api/v1/referral-requests/",
            json={
                "company_id": test_company.id,
                "position_title": "Engineer",
                "motivation": "Interested",
                "priority": "medium"
            }
        )
        
        assert response.status_code == 401

    def test_get_my_requests_as_student(self, client, test_student, test_draft_request, auth_headers_student):
        """Test getting own requests as student."""
        response = client.get(
            "/api/v1/referral-requests/",
            headers=auth_headers_student
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) >= 1

    def test_get_approved_requests_as_alumni(self, client, test_alumni, test_approved_request, auth_headers_alumni):
        """Test alumni sees approved requests."""
        response = client.get(
            "/api/v1/referral-requests/",
            headers=auth_headers_alumni
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert all(req["status"] == "approved" for req in data["data"])

    def test_get_pending_requests_as_admin(self, client, test_admin, test_pending_request, auth_headers_admin):
        """Test admin sees pending requests."""
        response = client.get(
            "/api/v1/referral-requests/",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_single_request(self, client, test_draft_request, auth_headers_student):
        """Test getting a single request."""
        response = client.get(
            f"/api/v1/referral-requests/{test_draft_request.id}",
            headers=auth_headers_student
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == test_draft_request.id

    def test_update_draft_request(self, client, test_student, test_draft_request, auth_headers_student):
        """Test updating a draft request."""
        response = client.put(
            f"/api/v1/referral-requests/{test_draft_request.id}",
            headers=auth_headers_student,
            json={
                "position_title": "Senior Engineer",
                "priority": "high"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["position_title"] == "Senior Engineer"
        assert data["data"]["priority"] == "high"

    def test_update_request_unauthorized(self, client, test_draft_request, auth_headers_alumni):
        """Test updating request by non-owner."""
        response = client.put(
            f"/api/v1/referral-requests/{test_draft_request.id}",
            headers=auth_headers_alumni,
            json={"position_title": "New Title"}
        )
        
        assert response.status_code == 403

    def test_submit_request_for_approval(self, client, test_student, test_draft_request, auth_headers_student):
        """Test submitting request for approval."""
        response = client.post(
            f"/api/v1/referral-requests/{test_draft_request.id}/submit",
            headers=auth_headers_student
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "pending"

    def test_delete_draft_request(self, client, test_student, test_draft_request, auth_headers_student):
        """Test deleting a draft request."""
        response = client.delete(
            f"/api/v1/referral-requests/{test_draft_request.id}",
            headers=auth_headers_student
        )
        
        assert response.status_code == 204

    def test_create_request_invalid_company(self, client, auth_headers_student):
        """Test creating request with invalid company."""
        response = client.post(
            "/api/v1/referral-requests/",
            headers=auth_headers_student,
            json={
                "company_id": 99999,
                "position_title": "Engineer",
                "motivation": "Interested",
                "priority": "medium"
            }
        )
        
        assert response.status_code == 404

    def test_pagination(self, client, test_student, test_company, auth_headers_student, db):
        """Test pagination of requests."""
        # Create multiple requests
        from app.models.referral_request import ReferralRequest
        from datetime import datetime, timezone
        
        for i in range(5):
            req = ReferralRequest(
                student_id=test_student.id,
                company_id=test_company.id,
                position_title=f"Position {i}",
                motivation="Interested",
                status="draft",
                created_at=datetime.now(timezone.utc)
            )
            db.add(req)
        db.commit()
        
        # Test pagination
        response = client.get(
            "/api/v1/referral-requests/?skip=0&limit=3",
            headers=auth_headers_student
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 3


class TestAdminReferralEndpoints:
    """Test admin-specific referral request endpoints."""

    def test_get_pending_requests(self, client, test_admin, test_pending_request, auth_headers_admin):
        """Test getting pending requests as admin."""
        response = client.get(
            "/api/v1/admin/pending-requests",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_pending_requests_unauthorized(self, client, auth_headers_student):
        """Test non-admin cannot access pending requests."""
        response = client.get(
            "/api/v1/admin/pending-requests",
            headers=auth_headers_student
        )
        
        assert response.status_code == 403

    def test_approve_request(self, client, test_admin, test_pending_request, auth_headers_admin):
        """Test approving a request."""
        response = client.post(
            f"/api/v1/admin/requests/{test_pending_request.id}/approve",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "approved"

    def test_reject_request(self, client, test_admin, test_pending_request, auth_headers_admin):
        """Test rejecting a request."""
        response = client.post(
            f"/api/v1/admin/requests/{test_pending_request.id}/reject",
            headers=auth_headers_admin,
            json={"reason": "Insufficient information"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "rejected"

    def test_approve_request_as_non_admin(self, client, test_pending_request, auth_headers_student):
        """Test that non-admin cannot approve requests."""
        response = client.post(
            f"/api/v1/admin/requests/{test_pending_request.id}/approve",
            headers=auth_headers_student
        )
        
        assert response.status_code == 403
