"""Referral submissions endpoints."""
from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import ForbiddenException, NotFoundException, ValidationException
from app.core.rate_limit import limiter
from app.dependencies.auth import get_current_user
from app.models.referral_request import ReferralRequest, RequestStatus
from app.models.referral_submission import ReferralSubmission, SubmissionStatus
from app.models.user import User, UserRole
from app.schemas.referral_submission import (
    ReferralSubmissionCreate,
    ReferralSubmissionOut,
)
from app.schemas.response import ApiResponse

router = APIRouter(prefix="/referral-submissions")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[ReferralSubmissionOut])
@limiter.limit("20/minute")
def create_submission(
    request: Request,
    submission_data: ReferralSubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Alumni submits a referral for an approved request."""
    user_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if user_role not in [UserRole.ALUMNI.value, UserRole.ADMIN.value, "alumni", "admin"]:
        raise ForbiddenException("Only alumni can submit referrals")

    referral_request = db.query(ReferralRequest).filter(ReferralRequest.id == submission_data.request_id).first()
    if not referral_request:
        raise NotFoundException("Referral request not found")

    new_submission = ReferralSubmission(
        request_id=submission_data.request_id,
        alumni_id=current_user.id,
        notes=submission_data.notes,
        confidence_level=submission_data.confidence_level,
        status=SubmissionStatus.APPROVED.value,
    )
    db.add(new_submission)

    # Mark the request as fulfilled
    referral_request.status = RequestStatus.FULFILLED.value

    db.commit()
    db.refresh(new_submission)

    return ApiResponse(
        message="Referral submitted successfully",
        data=new_submission,
    )


@router.get("/", response_model=ApiResponse[List[ReferralSubmissionOut]])
@limiter.limit("60/minute")
def get_submissions(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get referral submissions based on role."""
    user_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if user_role in [UserRole.ALUMNI.value, "alumni"]:
        submissions = db.query(ReferralSubmission).filter(
            ReferralSubmission.alumni_id == current_user.id
        ).offset(skip).limit(limit).all()
    elif user_role in [UserRole.STUDENT.value, "student"]:
        submissions = db.query(ReferralSubmission).join(ReferralRequest).filter(
            ReferralRequest.student_id == current_user.id
        ).offset(skip).limit(limit).all()
    else:
        submissions = db.query(ReferralSubmission).offset(skip).limit(limit).all()

    return ApiResponse(
        message="Submissions fetched successfully",
        data=submissions,
    )


@router.get("/{submission_id}", response_model=ApiResponse[ReferralSubmissionOut])
@limiter.limit("60/minute")
def get_submission(
    request: Request,
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific submission by ID."""
    submission = db.query(ReferralSubmission).filter(ReferralSubmission.id == submission_id).first()
    if not submission:
        raise NotFoundException("Submission not found")
    return ApiResponse(
        message="Submission fetched successfully",
        data=submission,
    )
