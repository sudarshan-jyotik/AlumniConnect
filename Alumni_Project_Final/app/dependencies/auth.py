"""
Authentication dependencies - FIXED VERSION.
Fixed bugs:
1. Token verification now reads 'sub' claim correctly
2. Role is included in access token
3. Uses timezone-aware datetime
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a new JWT access token.
    
    Args:
        data: Dictionary with user_id and role
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "sub": str(data["user_id"]),  # Store as 'sub' (standard JWT claim)
        "role": data.get("role", "student"),  # ✅ FIX: Include role
    })
    
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a new refresh token.
    
    Args:
        data: User data
        
    Returns:
        Secure random token
    """
    return secrets.token_urlsafe(64)


def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """
    Verify and decode JWT access token.
    
    Args:
        token: JWT token string
        credentials_exception: Exception to raise on failure
        
    Returns:
        TokenData with user_id and role
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # ✅ FIX: Read from 'sub' claim (not 'user_id')
        user_id_str: str = payload.get("sub")
        role: str = payload.get("role", "student")
        
        if user_id_str is None:
            raise credentials_exception
        
        user_id = int(user_id_str)
        token_data = TokenData(id=user_id, role=role)
        
    except (JWTError, ValueError, TypeError):
        raise credentials_exception
    
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.id).first()

    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    
    Args:
        current_user: User from get_current_user
        
    Returns:
        User if active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
