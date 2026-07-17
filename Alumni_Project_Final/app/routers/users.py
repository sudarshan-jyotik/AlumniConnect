"""Users endpoints."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.user import UserOut

router = APIRouter(prefix="/users")


@router.get("/me", response_model=ApiResponse[UserOut])
@limiter.limit("60/minute")
def get_current_user_info(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return ApiResponse(
        message="User info fetched",
        data=current_user,
    )
