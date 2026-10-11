"""Endorsements endpoints."""
from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.core.rate_limit import limiter
from app.dependencies.auth import get_current_user
from app.models.endorsement import Endorsement
from app.models.referral_request import ReferralRequest
from app.models.user import User
from app.schemas.endorsement import EndorsementCreate, EndorsementOut
from app.schemas.response import ApiResponse

router = APIRouter(prefix="/endorsements")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[EndorsementOut])
@limiter.limit("30/minute")
def create_endorsement(
    request: Request,
    data: EndorsementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Endorse a referral request."""
    referral_request = db.query(ReferralRequest).filter(ReferralRequest.id == data.request_id).first()
    if not referral_request:
        raise NotFoundException("Referral request not found")

    existing = db.query(Endorsement).filter(
        Endorsement.user_id == current_user.id,
        Endorsement.request_id == data.request_id
    ).first()

    if existing:
        existing.comment = data.comment
        existing.strength = data.strength
        db.commit()
        db.refresh(existing)
        return ApiResponse(
            message="Endorsement updated",
            data=existing,
        )

    endorsement = Endorsement(
        user_id=current_user.id,
        request_id=data.request_id,
        comment=data.comment,
        strength=data.strength,
    )
    db.add(endorsement)
    referral_request.endorsement_count = (referral_request.endorsement_count or 0) + 1
    db.commit()
    db.refresh(endorsement)

    return ApiResponse(
        message="Endorsement created successfully",
        data=endorsement,
    )


@router.get("/request/{request_id}", response_model=ApiResponse[List[EndorsementOut]])
@limiter.limit("60/minute")
def get_request_endorsements(
    request: Request,
    request_id: int,
    db: Session = Depends(get_db),
):
    """Get all endorsements for a request."""
    endorsements = db.query(Endorsement).filter(Endorsement.request_id == request_id).all()
    return ApiResponse(
        message="Endorsements fetched successfully",
        data=endorsements,
    )
