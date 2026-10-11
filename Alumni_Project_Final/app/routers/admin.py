"""Admin endpoints."""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel

from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.core.rate_limit import limiter
from app.dependencies.roles import require_admin
from app.models.alumni_profile import AlumniProfile
from app.models.company import Company
from app.models.referral_request import ReferralRequest, RequestStatus
from app.models.user import User, UserRole
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


class AdminStats(BaseModel):
    pending_requests_count: int
    approved_requests_count: int
    fulfilled_requests_count: int
    rejected_requests_count: int
    total_requests_count: int
    unverified_alumni_count: int
    total_companies_count: int
    total_users_count: int
    approval_rate_percentage: float


class AlumniVerificationOut(BaseModel):
    id: int
    user_id: int
    user_name: Optional[str] = None
    user_email: str
    current_company_id: Optional[int] = None
    current_company_name: Optional[str] = None
    current_position: Optional[str] = None
    graduation_year: Optional[int] = None
    degree: Optional[str] = None
    department: Optional[str] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    is_verified: bool
    verified_at: Optional[datetime] = None


@router.get("/stats", response_model=ApiResponse[AdminStats])
@limiter.limit("60/minute")
def get_admin_stats(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get real-time statistics for the administration dashboard."""
    pending_count = db.query(ReferralRequest).filter(
        ReferralRequest.status.in_([RequestStatus.PENDING, RequestStatus.PENDING.value])
    ).count()

    approved_count = db.query(ReferralRequest).filter(
        ReferralRequest.status.in_([RequestStatus.APPROVED, RequestStatus.APPROVED.value])
    ).count()

    fulfilled_count = db.query(ReferralRequest).filter(
        ReferralRequest.status.in_([RequestStatus.FULFILLED, RequestStatus.FULFILLED.value])
    ).count()

    rejected_count = db.query(ReferralRequest).filter(
        ReferralRequest.status.in_([RequestStatus.REJECTED, RequestStatus.REJECTED.value])
    ).count()

    total_requests = db.query(ReferralRequest).count()
    total_companies = db.query(Company).count()
    total_users = db.query(User).count()
    unverified_alumni = db.query(AlumniProfile).filter(AlumniProfile.is_verified == False).count()

    decided = approved_count + fulfilled_count + rejected_count
    approval_rate = round(((approved_count + fulfilled_count) / decided * 100), 1) if decided > 0 else 100.0

    return ApiResponse(
        message="Admin stats calculated",
        data=AdminStats(
            pending_requests_count=pending_count,
            approved_requests_count=approved_count,
            fulfilled_requests_count=fulfilled_count,
            rejected_requests_count=rejected_count,
            total_requests_count=total_requests,
            unverified_alumni_count=unverified_alumni,
            total_companies_count=total_companies,
            total_users_count=total_users,
            approval_rate_percentage=approval_rate,
        ),
    )


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


@router.get("/alumni-verifications", response_model=ApiResponse[List[AlumniVerificationOut]])
@limiter.limit("60/minute")
def get_alumni_verifications(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get alumni verification queue."""
    profiles = db.query(AlumniProfile).options(
        joinedload(AlumniProfile.user),
        joinedload(AlumniProfile.current_company),
    ).all()

    results = []
    for p in profiles:
        results.append(AlumniVerificationOut(
            id=p.id,
            user_id=p.user_id,
            user_name=p.user.full_name if p.user else "Alumni User",
            user_email=p.user.email if p.user else "unknown",
            current_company_id=p.current_company_id,
            current_company_name=p.current_company.name if p.current_company else (p.company if hasattr(p, 'company') else None),
            current_position=p.current_position or "Engineer",
            graduation_year=p.graduation_year,
            degree=p.degree,
            department=p.department,
            linkedin_url=str(p.linkedin_url) if p.linkedin_url else None,
            bio=p.bio,
            is_verified=bool(p.is_verified),
            verified_at=p.verified_at,
        ))

    return ApiResponse(
        message="Alumni verifications queue fetched",
        data=results,
    )


@router.post("/alumni/{user_id}/verify", response_model=ApiResponse[AlumniVerificationOut])
@limiter.limit("30/minute")
def verify_alumni(
    request: Request,
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Verify an alumni profile."""
    profile = db.query(AlumniProfile).filter(AlumniProfile.user_id == user_id).first()
    if not profile:
        profile = AlumniProfile(user_id=user_id)
        db.add(profile)

    profile.is_verified = True
    profile.verified_by_id = current_user.id
    profile.verified_at = datetime.now(timezone.utc)

    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.status = "active"

    db.commit()
    db.refresh(profile)

    return ApiResponse(
        message="Alumni identity successfully verified",
        data=AlumniVerificationOut(
            id=profile.id,
            user_id=profile.user_id,
            user_name=profile.user.full_name if profile.user else "Alumni",
            user_email=profile.user.email if profile.user else "",
            current_company_id=profile.current_company_id,
            current_company_name=profile.current_company.name if profile.current_company else None,
            current_position=profile.current_position,
            graduation_year=profile.graduation_year,
            degree=profile.degree,
            department=profile.department,
            linkedin_url=str(profile.linkedin_url) if profile.linkedin_url else None,
            bio=profile.bio,
            is_verified=True,
            verified_at=profile.verified_at,
        ),
    )


@router.post("/alumni/{user_id}/reject", response_model=ApiResponse[AlumniVerificationOut])
@limiter.limit("30/minute")
def reject_alumni_verification(
    request: Request,
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Reject / unverify an alumni profile."""
    profile = db.query(AlumniProfile).filter(AlumniProfile.user_id == user_id).first()
    if not profile:
        raise NotFoundException("Alumni profile not found")

    profile.is_verified = False
    profile.verified_by_id = None
    profile.verified_at = None

    db.commit()
    db.refresh(profile)

    return ApiResponse(
        message="Alumni verification rejected",
        data=AlumniVerificationOut(
            id=profile.id,
            user_id=profile.user_id,
            user_name=profile.user.full_name if profile.user else "Alumni",
            user_email=profile.user.email if profile.user else "",
            current_company_id=profile.current_company_id,
            current_company_name=profile.current_company.name if profile.current_company else None,
            current_position=profile.current_position,
            graduation_year=profile.graduation_year,
            degree=profile.degree,
            department=profile.department,
            linkedin_url=str(profile.linkedin_url) if profile.linkedin_url else None,
            bio=profile.bio,
            is_verified=False,
            verified_at=None,
        ),
    )
