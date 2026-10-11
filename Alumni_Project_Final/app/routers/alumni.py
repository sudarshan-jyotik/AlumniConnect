"""Alumni endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.core.rate_limit import limiter
from app.dependencies.auth import get_current_user
from app.models.alumni_profile import AlumniProfile
from app.models.user import User
from app.schemas.alumni_profile import AlumniProfileOut, AlumniProfileUpdate
from app.schemas.response import ApiResponse

router = APIRouter(prefix="/alumni")


@router.get("/profiles", response_model=ApiResponse[List[AlumniProfileOut]])
@limiter.limit("60/minute")
def get_alumni_profiles(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all verified alumni profiles."""
    profiles = db.query(AlumniProfile).offset(skip).limit(limit).all()
    return ApiResponse(
        message="Alumni profiles fetched successfully",
        data=profiles,
    )


@router.get("/profiles/{user_id}", response_model=ApiResponse[AlumniProfileOut])
@limiter.limit("60/minute")
def get_alumni_profile_by_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get alumni profile by user ID."""
    profile = db.query(AlumniProfile).filter(AlumniProfile.user_id == user_id).first()
    if not profile:
        raise NotFoundException("Alumni profile not found")
    return ApiResponse(
        message="Alumni profile fetched successfully",
        data=profile,
    )


@router.put("/profile", response_model=ApiResponse[AlumniProfileOut])
@limiter.limit("20/minute")
def update_my_alumni_profile(
    request: Request,
    profile_data: AlumniProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's alumni profile."""
    profile = db.query(AlumniProfile).filter(AlumniProfile.user_id == current_user.id).first()
    if not profile:
        profile = AlumniProfile(user_id=current_user.id)
        db.add(profile)

    update_dict = profile_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if hasattr(profile, key) and value is not None:
            setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return ApiResponse(
        message="Alumni profile updated successfully",
        data=profile,
    )
