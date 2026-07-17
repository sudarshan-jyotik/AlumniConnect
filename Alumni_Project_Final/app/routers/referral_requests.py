"""Referral requests endpoints."""
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.referral_request import RequestStatus
from app.repositories.company import CompanyRepository
from app.repositories.referral_request import ReferralRequestRepository
from app.schemas.referral_request import (
    ReferralRequestCreate,
    ReferralRequestOut,
    ReferralRequestUpdate,
)
from app.schemas.response import ApiResponse
from app.services.referral_request import ReferralRequestService

router = APIRouter(prefix="/referral-requests")


def get_service(db: Session = Depends(get_db)) -> ReferralRequestService:
    """Get referral request service."""
    repository = ReferralRequestRepository(db)
    company_repository = CompanyRepository(db)
    return ReferralRequestService(repository, company_repository, db)


@router.get("/", response_model=ApiResponse[list[ReferralRequestOut]])
@limiter.limit("60/minute")
def get_requests(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: ReferralRequestService = Depends(get_service),
):
    """Get referral requests based on user role."""
    if current_user.is_student():
        # Students see their own requests
        requests = service.get_my_requests(current_user.id, skip, limit)
    elif current_user.is_alumni():
        # Alumni see approved requests
        requests = service.get_approved_requests(skip, limit)
    else:
        # Admins see all pending
        requests = service.repository.get_by_status(RequestStatus.PENDING, skip, limit)
    
    return ApiResponse(
        message="Requests fetched successfully",
        data=requests,
    )


@router.get("/{request_id}", response_model=ApiResponse[ReferralRequestOut])
@limiter.limit("60/minute")
def get_request(
    request: Request,
    request_id: int,
    current_user: User = Depends(get_current_user),
    service: ReferralRequestService = Depends(get_service),
):
    """Get a specific request."""
    req = service.get_request(request_id)
    return ApiResponse(
        message="Request fetched successfully",
        data=req,
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[ReferralRequestOut])
@limiter.limit("10/minute")
def create_request(
    request: Request,
    request_data: ReferralRequestCreate,
    current_user: User = Depends(get_current_user),
    service: ReferralRequestService = Depends(get_service),
):
    """Create a new referral request."""
    created_request = service.create_request(request_data, current_user.id)
    return ApiResponse(
        message="Request created successfully",
        data=created_request,
    )


@router.put("/{request_id}", response_model=ApiResponse[ReferralRequestOut])
@limiter.limit("10/minute")
def update_request(
    request: Request,
    request_id: int,
    request_data: ReferralRequestUpdate,
    current_user: User = Depends(get_current_user),
    service: ReferralRequestService = Depends(get_service),
):
    """Update a referral request."""
    updated_request = service.update_request(request_id, request_data, current_user.id)
    return ApiResponse(
        message="Request updated successfully",
        data=updated_request,
    )


@router.post("/{request_id}/submit", response_model=ApiResponse[ReferralRequestOut])
@limiter.limit("10/minute")
def submit_request(
    request: Request,
    request_id: int,
    current_user: User = Depends(get_current_user),
    service: ReferralRequestService = Depends(get_service),
):
    """Submit request for approval."""
    submitted_request = service.submit_for_approval(request_id, current_user.id)
    return ApiResponse(
        message="Request submitted for approval",
        data=submitted_request,
    )


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
def delete_request(
    request: Request,
    request_id: int,
    current_user: User = Depends(get_current_user),
    service: ReferralRequestService = Depends(get_service),
):
    """Delete a request."""
    service.delete_request(request_id, current_user)
