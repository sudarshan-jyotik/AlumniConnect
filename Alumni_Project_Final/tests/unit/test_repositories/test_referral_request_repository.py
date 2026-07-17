"""Tests for Referral Request Repository."""
import pytest
from datetime import datetime, timezone

from app.models.referral_request import ReferralRequest, RequestStatus, RequestPriority
from app.repositories.referral_request import ReferralRequestRepository


class TestReferralRequestRepository:
    """Test cases for Referral Request Repository."""

    def test_create_request(self, db, test_student, test_company):
        """Test creating a referral request."""
        repo = ReferralRequestRepository(db)
        request = ReferralRequest(
            student_id=test_student.id,
            company_id=test_company.id,
            position_title="Backend Engineer",
            motivation="Very interested",
            status="draft",
            priority="medium",
            created_at=datetime.now(timezone.utc)
        )
        
        created_request = repo.create(request)
        db.commit()  # Commit the transaction
        db.refresh(created_request)  # Refresh to get the ID
        
        assert created_request.id is not None
        assert created_request.position_title == "Backend Engineer"
        assert created_request.status == "draft"

    def test_get_by_id(self, db, test_draft_request):
        """Test getting request by ID."""
        repo = ReferralRequestRepository(db)
        
        request = repo.get_by_id(test_draft_request.id)
        
        assert request is not None
        assert request.id == test_draft_request.id

    def test_get_by_student(self, db, test_student, test_draft_request, test_pending_request):
        """Test getting requests by student."""
        repo = ReferralRequestRepository(db)
        
        requests = repo.get_by_student(test_student.id, skip=0, limit=10)
        
        assert len(requests) >= 2
        assert all(r.student_id == test_student.id for r in requests)

    def test_get_by_student_pagination(self, db, test_student, test_company):
        """Test pagination in get_by_student."""
        repo = ReferralRequestRepository(db)
        
        # Create multiple requests
        for i in range(5):
            request = ReferralRequest(
                student_id=test_student.id,
                company_id=test_company.id,
                position_title=f"Position {i}",
                motivation="Motivated",
                status="draft",
                created_at=datetime.now(timezone.utc)
            )
            repo.create(request)
        db.commit()  # Commit all requests
        
        # Test pagination
        page1 = repo.get_by_student(test_student.id, skip=0, limit=2)
        page2 = repo.get_by_student(test_student.id, skip=2, limit=2)
        
        assert len(page1) == 2
        assert len(page2) >= 2

    def test_get_by_status(self, db, test_draft_request, test_pending_request, test_approved_request):
        """Test getting requests by status."""
        repo = ReferralRequestRepository(db)
        
        pending_requests = repo.get_by_status("pending", skip=0, limit=10)
        
        assert len(pending_requests) >= 1
        assert all(r.status == "pending" for r in pending_requests)

    def test_get_by_status_draft(self, db, test_draft_request):
        """Test getting draft requests."""
        repo = ReferralRequestRepository(db)
        
        draft_requests = repo.get_by_status("draft", skip=0, limit=10)
        
        assert len(draft_requests) >= 1
        assert all(r.status == "draft" for r in draft_requests)

    def test_get_by_status_approved(self, db, test_approved_request):
        """Test getting approved requests."""
        repo = ReferralRequestRepository(db)
        
        approved_requests = repo.get_by_status("approved", skip=0, limit=10)
        
        assert len(approved_requests) >= 1
        assert all(r.status == "approved" for r in approved_requests)

    def test_get_approved(self, db, test_approved_request):
        """Test getting approved requests specifically."""
        repo = ReferralRequestRepository(db)
        
        approved_requests = repo.get_approved(skip=0, limit=10)
        
        assert len(approved_requests) >= 1
        assert all(r.status == "approved" for r in approved_requests)

    def test_get_with_details(self, db, test_draft_request):
        """Test getting request with relationships loaded."""
        repo = ReferralRequestRepository(db)
        
        request = repo.get_with_details(test_draft_request.id)
        
        assert request is not None
        assert request.student is not None
        assert request.company is not None
        assert request.student.email is not None
        assert request.company.name is not None

    def test_get_with_details_not_found(self, db):
        """Test getting non-existent request with details."""
        repo = ReferralRequestRepository(db)
        
        request = repo.get_with_details(99999)
        
        assert request is None

    def test_update_request(self, db, test_draft_request):
        """Test updating a request."""
        repo = ReferralRequestRepository(db)
        
        updated_request = repo.update(test_draft_request.id, {
            "position_title": "Senior Engineer",
            "priority": "high"
        })
        
        assert updated_request.position_title == "Senior Engineer"
        assert updated_request.priority == "high"

    def test_update_request_status(self, db, test_draft_request):
        """Test updating request status."""
        repo = ReferralRequestRepository(db)
        
        updated_request = repo.update(test_draft_request.id, {
            "status": "pending",
            "submitted_at": datetime.now(timezone.utc)
        })
        
        assert updated_request.status == "pending"
        assert updated_request.submitted_at is not None

    def test_delete_request(self, db, test_draft_request):
        """Test deleting a request."""
        repo = ReferralRequestRepository(db)
        request_id = test_draft_request.id
        
        result = repo.delete(request_id)
        db.commit()  # Commit the deletion
        
        assert result is True
        assert repo.get_by_id(request_id) is None

    def test_get_all(self, db, test_draft_request, test_pending_request):
        """Test getting all requests."""
        repo = ReferralRequestRepository(db)
        
        all_requests = repo.get_all(skip=0, limit=100)
        
        assert len(all_requests) >= 2

    def test_request_with_submissions(self, db, test_approved_request, test_submission):
        """Test request with submissions relationship."""
        repo = ReferralRequestRepository(db)
        
        request = repo.get_by_id(test_approved_request.id)
        
        assert request.submissions is not None
        assert len(request.submissions) >= 1

    def test_get_by_company(self, db, test_company, test_draft_request, test_pending_request):
        """Test getting requests by company."""
        repo = ReferralRequestRepository(db)
        
        # Get all requests and filter by company
        all_requests = repo.get_all()
        company_requests = [r for r in all_requests if r.company_id == test_company.id]
        
        assert len(company_requests) >= 2

    def test_priority_filtering(self, db, test_approved_request):
        """Test that we can filter by priority."""
        repo = ReferralRequestRepository(db)
        
        # Get all requests and check priorities exist
        all_requests = repo.get_all()
        
        assert any(r.priority == "urgent" for r in all_requests)
