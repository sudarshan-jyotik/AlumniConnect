"""Tests for Referral Request Service."""
import pytest
from datetime import datetime, timezone

from app.core.exceptions import ForbiddenException, NotFoundException, ValidationException
from app.models.referral_request import RequestStatus
from app.models.user import UserRole
from app.repositories.referral_request import ReferralRequestRepository
from app.repositories.company import CompanyRepository
from app.schemas.referral_request import ReferralRequestCreate, ReferralRequestUpdate
from app.services.referral_request import ReferralRequestService


class TestReferralRequestService:
    """Test cases for Referral Request Service."""

    @pytest.fixture
    def request_service(self, db):
        """Create referral request service instance."""
        request_repo = ReferralRequestRepository(db)
        company_repo = CompanyRepository(db)
        return ReferralRequestService(request_repo, company_repo, db)

    def test_create_request(self, db, request_service, test_student, test_company):
        """Test creating a referral request."""
        request_data = ReferralRequestCreate(
            company_id=test_company.id,
            position_title="Software Engineer",
            job_description="Great opportunity",
            location="San Francisco",
            motivation="Very interested in this role",
            priority="medium"
        )
        
        created_request = request_service.create_request(request_data, test_student.id)
        
        assert created_request.id is not None
        assert created_request.student_id == test_student.id
        assert created_request.company_id == test_company.id
        assert created_request.position_title == "Software Engineer"
        assert created_request.status == "draft"

    def test_create_request_invalid_company(self, db, request_service, test_student):
        """Test creating request with invalid company."""
        request_data = ReferralRequestCreate(
            company_id=99999,  # Non-existent
            position_title="Software Engineer",
            motivation="Very interested",
            priority="medium"
        )
        
        with pytest.raises(NotFoundException) as exc_info:
            request_service.create_request(request_data, test_student.id)
        
        assert "company not found" in str(exc_info.value).lower()

    def test_get_request(self, db, request_service, test_draft_request):
        """Test getting a request by ID."""
        request = request_service.get_request(test_draft_request.id)
        
        assert request is not None
        assert request.id == test_draft_request.id
        assert request.student is not None
        assert request.company is not None

    def test_get_request_not_found(self, db, request_service):
        """Test getting non-existent request."""
        with pytest.raises(NotFoundException):
            request_service.get_request(99999)

    def test_get_my_requests(self, db, request_service, test_student, test_draft_request, test_pending_request):
        """Test getting user's own requests."""
        requests = request_service.get_my_requests(test_student.id)
        
        assert len(requests) >= 2
        assert all(r.student_id == test_student.id for r in requests)

    def test_get_approved_requests(self, db, request_service, test_approved_request):
        """Test getting approved requests."""
        requests = request_service.get_approved_requests()
        
        assert len(requests) >= 1
        assert all(r.status == "approved" for r in requests)

    def test_update_request_success(self, db, request_service, test_student, test_draft_request):
        """Test updating a draft request."""
        update_data = ReferralRequestUpdate(
            position_title="Senior Software Engineer",
            priority="high"
        )
        
        updated_request = request_service.update_request(
            test_draft_request.id,
            update_data,
            test_student.id
        )
        
        assert updated_request.position_title == "Senior Software Engineer"
        assert updated_request.priority == "high"

    def test_update_request_unauthorized(self, db, request_service, test_draft_request, test_alumni):
        """Test updating request by non-owner."""
        update_data = ReferralRequestUpdate(
            position_title="New Title"
        )
        
        with pytest.raises(ForbiddenException) as exc_info:
            request_service.update_request(
                test_draft_request.id,
                update_data,
                test_alumni.id  # Different user
            )
        
        assert "not authorized" in str(exc_info.value).lower()

    def test_update_request_non_draft(self, db, request_service, test_student, test_pending_request):
        """Test updating non-draft request fails."""
        update_data = ReferralRequestUpdate(
            position_title="New Title"
        )
        
        with pytest.raises(ValidationException) as exc_info:
            request_service.update_request(
                test_pending_request.id,
                update_data,
                test_student.id
            )
        
        assert "draft" in str(exc_info.value).lower()

    def test_submit_for_approval(self, db, request_service, test_student, test_draft_request):
        """Test submitting request for approval."""
        submitted_request = request_service.submit_for_approval(
            test_draft_request.id,
            test_student.id
        )
        
        assert submitted_request.status == "pending"
        assert submitted_request.submitted_at is not None

    def test_submit_for_approval_unauthorized(self, db, request_service, test_draft_request, test_alumni):
        """Test submitting request by non-owner."""
        with pytest.raises(ForbiddenException):
            request_service.submit_for_approval(
                test_draft_request.id,
                test_alumni.id
            )

    def test_submit_already_submitted(self, db, request_service, test_student, test_pending_request):
        """Test submitting already submitted request."""
        with pytest.raises(ValidationException) as exc_info:
            request_service.submit_for_approval(
                test_pending_request.id,
                test_student.id
            )
        
        assert "already submitted" in str(exc_info.value).lower()

    def test_approve_request(self, db, request_service, test_admin, test_pending_request):
        """Test approving a pending request."""
        approved_request = request_service.approve_request(
            test_pending_request.id,
            test_admin.id
        )
        
        assert approved_request.status == "approved"
        assert approved_request.approved_at is not None
        assert approved_request.approved_by_id == test_admin.id

    def test_approve_non_pending_request(self, db, request_service, test_admin, test_draft_request):
        """Test approving non-pending request fails."""
        with pytest.raises(ValidationException) as exc_info:
            request_service.approve_request(
                test_draft_request.id,
                test_admin.id
            )
        
        assert "pending" in str(exc_info.value).lower()

    def test_reject_request(self, db, request_service, test_admin, test_pending_request):
        """Test rejecting a pending request."""
        rejected_request = request_service.reject_request(
            test_pending_request.id,
            test_admin.id,
            "Not enough information provided"
        )
        
        assert rejected_request.status == "rejected"
        assert rejected_request.rejection_reason == "Not enough information provided"
        assert rejected_request.rejected_at is not None

    def test_reject_non_pending_request(self, db, request_service, test_admin, test_approved_request):
        """Test rejecting non-pending request fails."""
        with pytest.raises(ValidationException):
            request_service.reject_request(
                test_approved_request.id,
                test_admin.id,
                "Some reason"
            )

    def test_delete_request_by_student(self, db, request_service, test_student, test_draft_request):
        """Test student deleting their own draft request."""
        result = request_service.delete_request(
            test_draft_request.id,
            test_student
        )
        
        assert result is True

    def test_delete_request_by_admin(self, db, request_service, test_admin, test_pending_request):
        """Test admin deleting any request."""
        result = request_service.delete_request(
            test_pending_request.id,
            test_admin
        )
        
        assert result is True

    def test_delete_request_unauthorized_student(self, db, request_service, test_student, test_pending_request):
        """Test student cannot delete non-draft request."""
        with pytest.raises(ForbiddenException):
            request_service.delete_request(
                test_pending_request.id,
                test_student
            )

    def test_delete_request_unauthorized_alumni(self, db, request_service, test_alumni, test_draft_request):
        """Test alumni cannot delete student's request."""
        with pytest.raises(ForbiddenException):
            request_service.delete_request(
                test_draft_request.id,
                test_alumni
            )

    def test_create_request_with_url(self, db, request_service, test_student, test_company):
        """Test creating request with job URL."""
        request_data = ReferralRequestCreate(
            company_id=test_company.id,
            position_title="DevOps Engineer",
            job_url="https://example.com/jobs/123",
            motivation="Great fit for my skills",
            priority="medium"
        )
        
        created_request = request_service.create_request(request_data, test_student.id)
        
        assert created_request.job_url is not None
        assert "https://example.com" in created_request.job_url

    def test_create_request_with_high_priority(self, db, request_service, test_student, test_company):
        """Test creating high priority request."""
        request_data = ReferralRequestCreate(
            company_id=test_company.id,
            position_title="Urgent Position",
            motivation="Need to apply soon",
            priority="urgent"
        )
        
        created_request = request_service.create_request(request_data, test_student.id)
        
        assert created_request.priority == "urgent"

    def test_update_partial_fields(self, db, request_service, test_student, test_draft_request):
        """Test partial update of request."""
        original_title = test_draft_request.position_title
        
        update_data = ReferralRequestUpdate(
            location="Remote"  # Only update location
        )
        
        updated_request = request_service.update_request(
            test_draft_request.id,
            update_data,
            test_student.id
        )
        
        assert updated_request.location == "Remote"
        assert updated_request.position_title == original_title  # Unchanged
