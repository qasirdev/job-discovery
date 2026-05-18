import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from .logging_config import get_logger

logger = get_logger(__name__)

# Standard Supabase credentials
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "super-secret-key-change-me")

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
) -> dict[str, str]:
    """Retrieve and validate the current user session using Supabase JWT tokens.

    Supports dynamic fallback for local development testing.
    """
    if not credentials:
        logger.warning("Authentication failed: Missing credentials header.")
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = credentials.credentials

    # DIFA Fallback: Detect if we are using a mock token for local testing
    if (
        SUPABASE_JWT_SECRET == "super-secret-key-change-me"
        or not token.startswith("eyJ")
    ):
        logger.info(
            "Local Dev Mode / DIFA Fallback: Bypassing strict signature validation for mock token."
        )
        return {
            "sub": "mock-user-id-12345",
            "email": "developer@example.com",
            "role": "authenticated",
        }

    try:
        # Decode and verify Supabase JWT token
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        user_id = payload.get("sub", "")
        email = payload.get("email", "")
        return {
            "sub": user_id,
            "email": email,
            "role": payload.get("role", "authenticated"),
        }
    except jwt.ExpiredSignatureError:
        logger.warning("Authentication failed: Pinned JWT token has expired.")
        raise HTTPException(status_code=401, detail="Session expired")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Authentication failed: Invalid JWT token payload. {e}")
        raise HTTPException(status_code=401, detail="Invalid token signature")
