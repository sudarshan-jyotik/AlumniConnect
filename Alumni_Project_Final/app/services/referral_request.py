"""
Referral Request service.
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, NotFoundException, ValidationException
from app.models.referral_request import ReferralRequest, RequestStatus
from app.models.user import User, UserRole
from app.repositories.referral_request import ReferralRequestRepository
from app.repositories.company import CompanyRepository
from app.schemas.referral_request import ReferralRequestCreate, ReferralRequestUpdate


class ReferralRequestService:
    """Service for managing referral requests."""

    def __init__(
        self,
        repository: ReferralRequestRepository,
        company_repository: CompanyRepository,
        db: Session
    ):
        self.repository = repository
        self.company_repository = company_repository
        self.db = db

    def create_request(self, request_data: ReferralRequestCreate, student_id: int) -> ReferralRequest:
        """Create a new referral request."""
        # Verify company exists
        company = self.company_repository.get_by_id(request_data.company_id)
        if not company:
            raise NotFoundException("Company not found")

        new_request = ReferralRequest(
            student_id=student_id,
            company_id=request_data.company_id,
            position_title=request_data.position_title,
            job_description=request_data.job_description,
            job_url=str(request_data.job_url) if request_data.job_url else None,
            location=request_data.location,
            motivation=request_data.motivation,
            skills_match=request_data.skills_match,
            priority=request_data.priority.value if hasattr(request_data.priority, 'value') else str(request_data.priority).lower(),
            status=RequestStatus.PENDING.value,
            submitted_at=datetime.now(timezone.utc),
        )

        self.repository.create(new_request)
        self.db.commit()
        self.db.refresh(new_request)

        return new_request

    def get_request(self, request_id: int) -> ReferralRequest:
        """Get request by ID."""
        request = self.repository.get_with_details(request_id)
        if not request:
            raise NotFoundException(f"Request {request_id} not found")
        return request

    def get_my_requests(self, user_id: int, skip: int = 0, limit: int = 100) -> list[ReferralRequest]:
        """Get user's own requests."""
        return self.repository.get_by_student(user_id, skip, limit)

    def get_approved_requests(self, skip: int = 0, limit: int = 100) -> list[ReferralRequest]:
        """Get all approved requests (for alumni to view)."""
        return self.repository.get_approved(skip, limit)

    def update_request(
        self, 
        request_id: int, 
        request_data: ReferralRequestUpdate, 
        user_id: int
    ) -> ReferralRequest:
        """Update a referral request."""
        request = self.get_request(request_id)

        # Only student who created can update
        if request.student_id != user_id:
            raise ForbiddenException("Not authorized to update this request")

        # Can only update if in draft (compare with both enum and string value)
        if request.status != RequestStatus.DRAFT.value and request.status != RequestStatus.DRAFT:
            raise ValidationException("Can only update draft requests")

        update_data = request_data.model_dump(exclude_unset=True)
        updated_request = self.repository.update(request_id, update_data)

        self.db.commit()
        self.db.refresh(updated_request)

        return updated_request

    def submit_for_approval(self, request_id: int, user_id: int) -> ReferralRequest:
        """Submit request for admin approval."""
        request = self.get_request(request_id)

        if request.student_id != user_id:
            raise ForbiddenException("Not authorized")

        if request.status != RequestStatus.DRAFT.value and request.status != RequestStatus.DRAFT:
            raise ValidationException("Request already submitted")

        request.status = RequestStatus.PENDING.value
        request.submitted_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(request)

        # TODO: Notify admins

        return request

    def approve_request(self, request_id: int, admin_id: int) -> ReferralRequest:
        """Approve a request (admin only)."""
        request = self.get_request(request_id)

        if request.status != RequestStatus.PENDING.value and request.status != RequestStatus.PENDING:
            raise ValidationException("Can only approve pending requests")

        request.status = RequestStatus.APPROVED.value
        request.approved_at = datetime.now(timezone.utc)
        request.approved_by_id = admin_id

        self.db.commit()
        self.db.refresh(request)

        # TODO: Notify student

        return request

    def reject_request(self, request_id: int, admin_id: int, reason: str) -> ReferralRequest:
        """Reject a request (admin only)."""
        request = self.get_request(request_id)

        if request.status != RequestStatus.PENDING.value and request.status != RequestStatus.PENDING:
            raise ValidationException("Can only reject pending requests")

        request.status = RequestStatus.REJECTED.value
        request.rejection_reason = reason
        request.rejected_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(request)

        # TODO: Notify student

        return request

    def delete_request(self, request_id: int, user: User) -> bool:
        """Delete a request."""
        request = self.get_request(request_id)

        # Admin can delete any, student can delete their own drafts
        # Compare role with both enum and string value for compatibility
        if (user.role == UserRole.ADMIN.value or user.role == UserRole.ADMIN):
            pass  # Allowed
        elif (request.student_id == user.id and 
              (request.status == RequestStatus.DRAFT.value or request.status == RequestStatus.DRAFT)):
            pass  # Allowed
        else:
            raise ForbiddenException("Not authorized to delete this request")

        self.repository.delete(request_id)
        self.db.commit()

        return True

    def endorse_request(self, request_id: int, user_id: int) -> ReferralRequest:
        """Endorse a referral request."""
        from app.models.endorsement import Endorsement
        request = self.get_request(request_id)

        # Check if already endorsed
        existing = self.db.query(Endorsement).filter(
            Endorsement.user_id == user_id,
            Endorsement.request_id == request_id
        ).first()

        if not existing:
            endorsement = Endorsement(
                user_id=user_id,
                request_id=request_id,
                strength=5,
                endorsement_type="technical"
            )
            self.db.add(endorsement)
            request.endorsement_count = (request.endorsement_count or 0) + 1
            self.db.commit()
            self.db.refresh(request)

        return request
