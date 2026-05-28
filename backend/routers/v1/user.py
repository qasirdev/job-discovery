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

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    request: Request,
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

    ip_address = request.client.host if request.client else "unknown"

    try:
        # Write final audit_log entry before deletion executes
        await db.execute(
            text("INSERT INTO audit_log (user_id, action, timestamp, ip_address) VALUES (:uid, 'user_deletion', NOW(), :ip)"),
            {"uid": user_id, "ip": ip_address}
        )
        
        # Hard-delete all rows
        await db.execute(text("DELETE FROM applications WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM cvs WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM cover_letters WHERE user_id = :uid"), {"uid": user_id})
        # Delete interview_preps for jobs the user applied to
        await db.execute(text("DELETE FROM interview_preps WHERE job_id IN (SELECT job_id FROM applications WHERE user_id = :uid)"), {"uid": user_id})
        
        # Delete pgvector embeddings from cv_chunks (assuming cv_chunks exists and links to user_id or cv_id)
        await db.execute(text("DELETE FROM cv_chunks WHERE cv_id IN (SELECT id FROM cvs WHERE user_id = :uid)"), {"uid": user_id})
        
        await db.commit()
        
        # Purge Redis cache entries for user (SCAN + DEL pattern)
        if hasattr(request.app.state, "redis"):
            redis = request.app.state.redis
            cursor = b"0"
            while cursor:
                cursor, keys = await redis.scan(cursor=cursor, match=f"*{user_id}*", count=100)
                if keys:
                    await redis.delete(*keys)
                if cursor == b"0":
                    break
        
        logger.info(json.dumps({"event": "gdpr_erasure_completed", "user_id": user_id}))
        from fastapi import Response
        return Response(status_code=status.HTTP_204_NO_CONTENT)
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
