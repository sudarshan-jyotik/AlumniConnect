from typing import Optional
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.response import ApiResponse
from app.schemas.token import Token, LogoutRequest, RefreshTokenRequest
from app.schemas.user import UserCreate, UserOut
from app.services.auth import AuthService

router = APIRouter(prefix="/auth")


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Get auth service dependency."""
    user_repo = UserRepository(db)
    refresh_token_repo = RefreshTokenRepository(db)
    return AuthService(user_repo, refresh_token_repo, db)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[UserOut])
@limiter.limit("3/minute")
def register(
    request: Request,
    user: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    """Register a new user."""
    created_user = service.register(user)
    return ApiResponse(
        message="User registered successfully. Please check your email to verify your account.",
        data=created_user,
    )


@router.post("/login", response_model=ApiResponse[Token])
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    """Login and get access + refresh tokens."""
    tokens = service.authenticate(
        email=form_data.username,
        password=form_data.password,
    )
    return ApiResponse(
        message="Login successful",
        data=tokens,
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def logout(
    request: Request,
    data: LogoutRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Logout by revoking refresh token."""
    service.logout(data.refresh_token)
    return ApiResponse(message="Logged out successfully")


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=ApiResponse[Token])
@limiter.limit("10/minute")
def refresh_token(
    request: Request,
    data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Refresh access token using refresh token."""
    tokens = service.refresh_access_token(data.refresh_token)
    return ApiResponse(
        message="Access token refreshed",
        data=tokens,
    )


@router.get("/verify/{token}", response_model=ApiResponse[UserOut])
def verify_email(
    token: str,
    service: AuthService = Depends(get_auth_service),
):
    """Verify user email with verification token."""
    user = service.verify_email(token)
    return ApiResponse(
        message="Email verified successfully",
        data=user,
    )


class GoogleAuthRequest(BaseModel):
    credential: str
    role: Optional[str] = "student"


@router.post("/google", response_model=ApiResponse[Token])
@limiter.limit("15/minute")
def login_google(
    request: Request,
    data: GoogleAuthRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Authenticate or register via Google OAuth credential."""
    tokens = service.authenticate_google(data.credential, data.role or "student")
    return ApiResponse(
        message="Google login successful",
        data=tokens,
    )
