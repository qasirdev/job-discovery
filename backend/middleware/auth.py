import jwt
from typing import Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..settings import get_settings

security = HTTPBearer()

async def verify_jwt(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Validates a Supabase JWT or Service Role JWT.
    Enforces RBAC via claims as documented in docs/SECURITY.md.
    """
    token = credentials.credentials
    settings = get_settings()

    # If it's the service role key, bypass standard user validation
    if settings.supabase_service_role_key and token == settings.supabase_service_role_key:
        return {"sub": str(settings.single_user_id), "role": "service", "email": "service@internal"}

    if not settings.supabase_anon_key:
        # Fallback for dev if no auth configured
        return {"sub": str(settings.single_user_id), "role": "admin", "email": "dev@local"}

    try:
        # Per docs/SECURITY.md: use SUPABASE_JWT_SECRET (separate from anon key).
        # Fallback to anon_key only for local dev environments where jwt_secret is unset.
        # Note: python-jose has known CVEs — pyjwt[crypto] is the only approved library.
        secret = settings.supabase_jwt_secret or settings.supabase_anon_key
        
        # We allow 30 seconds of clock skew for exp claim (JD-67 spec)
        payload = jwt.decode(token, secret, algorithms=["HS256"], leeway=30)
        
        # Verify issuer if necessary (depends on Supabase config, typically https://<project>.supabase.co/auth/v1)
        
        # Check Redis denylist
        jti = payload.get("jti")
        if jti and hasattr(request.app.state, "redis"):
            is_revoked = await request.app.state.redis.get(f"denylist:{jti}")
            if is_revoked:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"type": "about:blank", "title": "Unauthorized", "status": 401, "detail": "Token revoked"}
                )

        return {
            "sub": payload.get("sub"),
            "role": payload.get("role", "user"),
            "email": payload.get("email"),
            "jti": jti,
            "exp": payload.get("exp")
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"type": "about:blank", "title": "Unauthorized", "status": 401, "detail": "Token expired"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"type": "about:blank", "title": "Unauthorized", "status": 401, "detail": "Invalid token"}
        )

async def get_current_user(claims: Dict[str, Any] = Depends(verify_jwt)) -> Dict[str, Any]:
    """Dependency for user-scoped routes."""
    return claims

async def require_admin(claims: Dict[str, Any] = Depends(verify_jwt)) -> Dict[str, Any]:
    """Dependency for admin-only routes."""
    if claims.get("role") not in ["admin", "service"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"type": "about:blank", "title": "Forbidden", "status": 403, "detail": "Admin role required"}
        )
    return claims
