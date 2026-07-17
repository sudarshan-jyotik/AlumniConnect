"""Admin endpoints."""
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.dependencies.roles import require_admin
from app.models.user import User
from app.repositories.company import CompanyRepository
from app.repositories.referral_request import ReferralRequestRepository
from app.schemas.referral_request import ReferralRequestOut, ReferralRequestReject
from app.schemas.response import ApiResponse
from app.services.referral_request import ReferralRequestService

router = APIRouter(prefix="/admin")


def get_service(db: Session = Depends(get_db)) -> ReferralRequestService:
    """Get service."""
    repository = ReferralRequestRepository(db)
    company_repository = CompanyRepository(db)
    return ReferralRequestService(repository, company_repository, db)


@router.get("/pending-requests", response_model=ApiResponse[list[ReferralRequestOut]])
@limiter.limit("60/minute")
def get_pending_requests(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    service: ReferralRequestService = Depends(get_service),
):
    """Get all pending requests for admin approval."""
    from app.models.referral_request import RequestStatus
    requests = service.repository.get_by_status(RequestStatus.PENDING, skip, limit)
    return ApiResponse(
        message="Pending requests fetched",
        data=requests,
    )


@router.post("/requests/{request_id}/approve", response_model=ApiResponse[ReferralRequestOut])
@limiter.limit("30/minute")
def approve_request(
    request: Request,
    request_id: int,
    current_user: User = Depends(require_admin),
    service: ReferralRequestService = Depends(get_service),
):
    """Approve a referral request."""
    approved_request = service.approve_request(request_id, current_user.id)
    return ApiResponse(
        message="Request approved successfully",
        data=approved_request,
    )


@router.post("/requests/{request_id}/reject", response_model=ApiResponse[ReferralRequestOut])
@limiter.limit("30/minute")
def reject_request(
    request: Request,
    request_id: int,
    rejection_data: ReferralRequestReject,
    current_user: User = Depends(require_admin),
    service: ReferralRequestService = Depends(get_service),
):
    """Reject a referral request."""
    rejected_request = service.reject_request(request_id, current_user.id, rejection_data.reason)
    return ApiResponse(
        message="Request rejected",
        data=rejected_request,
    )
