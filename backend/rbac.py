from typing import Callable
from fastapi import Depends, HTTPException, status
from .auth import CurrentUser

def require_role(allowed_roles: set[str]) -> Callable[[dict], dict]:
    """Dependency factory for checking RBAC roles."""
    def role_checker(user: CurrentUser) -> dict:
        if user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user
    return role_checker

# Pre-configured dependencies for common roles
RequireAdmin = Depends(require_role({"admin"}))
RequireAuthenticated = Depends(require_role({"admin", "authenticated"}))
