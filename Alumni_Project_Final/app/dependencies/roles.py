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
        user_role_str = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
        allowed_str = [r.value if hasattr(r, 'value') else str(r) for r in allowed_roles]
        if user_role_str not in allowed_str:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_str}"
            )
        return current_user
    
    return role_checker


def require_student(current_user: User = Depends(get_current_user)) -> User:
    """Require student role."""
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val != UserRole.STUDENT.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Students only."
        )
    return current_user


def require_alumni(current_user: User = Depends(get_current_user)) -> User:
    """Require alumni role."""
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val != UserRole.ALUMNI.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Alumni only."
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role."""
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )
    return current_user
