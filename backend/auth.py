from fastapi import Request
from .logging_config import get_logger

logger = get_logger(__name__)

async def verify_jwt(request: Request):
    """Middleware dependency to verify Supabase JWT token."""
    # Stub for MVP 3
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        # logger.warning("Missing or invalid Authorization header.")
        # raise HTTPException(status_code=401, detail="Unauthorized")
        pass # Allow all for now
    
    logger.info("JWT Verification passed (Mocked).")
    return True
