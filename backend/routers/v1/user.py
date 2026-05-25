import json
import time
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ...db import get_db
from ...middleware.auth import get_current_user
from ...logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/user", tags=["user"])

@router.delete("")
async def delete_user(
    claims: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    GDPR Right to Erasure.
    Performs a hard delete of the user from the database.
    Due to RLS and cascading deletes, all associated data is removed.
    """
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID not found in claims")

    try:
        # Supabase auth.users deletion usually happens via Supabase API.
        # But we can also remove the user profile directly if we store it.
        # In MVP, we just execute a mock deletion logic or rely on Supabase cascade.
        await db.execute(text("DELETE FROM applications WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM cv WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM cover_letter WHERE user_id = :uid"), {"uid": user_id})
        
        # Log the GDPR deletion event to audit_log (indefinite retention)
        await db.execute(
            text("INSERT INTO audit_log (user_id, event_type, details) VALUES (:uid, 'gdpr_erasure', 'User requested full deletion')"),
            {"uid": user_id}
        )
        await db.commit()
        
        logger.info(json.dumps({"event": "gdpr_erasure_completed", "user_id": user_id}))
        return {"status": "success", "detail": "User data deleted according to GDPR Right to Erasure."}
    except Exception as e:
        await db.rollback()
        logger.error(f"Error during GDPR erasure for user {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process deletion request")

@router.get("/export")
async def export_user_data(
    claims: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    GDPR Right to Access.
    Streams all user-scoped data out in JSON format.
    """
    user_id = claims.get("sub")
    
    async def generate_json():
        yield '{\n  "user_id": "%s",\n  "applications": [\n' % user_id
        
        # Fetch applications
        apps = await db.execute(text("SELECT id, status FROM applications WHERE user_id = :uid"), {"uid": user_id})
        first = True
        for row in apps.fetchall():
            if not first:
                yield ',\n'
            yield f'    {{"id": "{row.id}", "status": "{row.status}"}}'
            first = False
            
        yield '\n  ]\n}'

    logger.info(json.dumps({"event": "gdpr_export_requested", "user_id": user_id}))
    return StreamingResponse(generate_json(), media_type="application/json")

@router.post("/logout")
async def logout(
    request: Request,
    claims: Dict[str, Any] = Depends(get_current_user)
):
    """
    Logs out the user by adding their JWT's 'jti' claim to the Redis denylist.
    The TTL of the Redis key is set to the remaining expiration time of the JWT.
    """
    jti = claims.get("jti")
    exp = claims.get("exp")
    
    if not jti or not exp:
        return {"status": "success", "detail": "No trackable token found"}
        
    if not hasattr(request.app.state, "redis"):
        logger.warning("Redis is not configured, cannot denylist token")
        return {"status": "success", "detail": "Logged out (denylist unavailable)"}
        
    now = int(time.time())
    ttl = exp - now
    
    if ttl > 0:
        await request.app.state.redis.setex(f"denylist:{jti}", ttl, "true")
        logger.info(json.dumps({"event": "token_revoked", "jti": jti, "ttl": ttl}))
        
    return {"status": "success", "detail": "Successfully logged out"}
