"""
Role-based access control dependencies.
"""

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import User, UserRole


def require_role(*allowed_roles: UserRole):
    """
    Dependency to require specific user roles.
    
    Args:
        *allowed_roles: Roles that are allowed
        
    Returns:
        Dependency function
        
    Example:
        @app.get("/admin", dependencies=[Depends(require_role(UserRole.ADMIN))])
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    
    return role_checker


def require_student(current_user: User = Depends(get_current_user)) -> User:
    """Require student role."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Students only."
        )
    return current_user


def require_alumni(current_user: User = Depends(get_current_user)) -> User:
    """Require alumni role."""
    if current_user.role != UserRole.ALUMNI:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Alumni only."
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )
    return current_user
