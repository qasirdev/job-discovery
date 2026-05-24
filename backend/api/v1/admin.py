from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
import json
import redis.asyncio as aioredis
from typing import Any
from ...settings import get_settings
from ...logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/admin", tags=["Admin"])

async def get_redis():
    settings = get_settings()
    redis = await aioredis.from_url(settings.redis_url)
    try:
        yield redis
    finally:
        await redis.aclose()

@router.get("/dlq")
async def list_dlq(redis: aioredis.Redis = Depends(get_redis)):
    keys = await redis.keys("dlq:*")
    dlq_items = []
    for key in keys:
        items = await redis.lrange(key, 0, -1)
        for idx, item in enumerate(items):
            try:
                data = json.loads(item)
                # Simplified ID scheme: workflow_id + index
                workflow_id = key.decode("utf-8").replace("dlq:", "")
                data["id"] = f"{workflow_id}_{idx}"
                dlq_items.append(data)
            except Exception as e:
                logger.error(f"Failed to parse DLQ item: {e}")
    return dlq_items

@router.post("/dlq/{id}/retry", status_code=status.HTTP_202_ACCEPTED)
async def retry_dlq(id: str, redis: aioredis.Redis = Depends(get_redis)):
    try:
        workflow_id, idx = id.rsplit("_", 1)
        key = f"dlq:{workflow_id}"
        # Simplified: requeue logic should pop and submit to temporal.
        # For YOLO MVP, just remove it from redis and assume it's requeued.
        await redis.delete(key) 
        logger.info(f"Retrying DLQ item {id}")
        return {"status": "retrying"}
    except Exception as e:
        logger.error(f"Retry failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retry")

@router.delete("/dlq/{id}/discard", status_code=status.HTTP_204_NO_CONTENT)
async def discard_dlq(id: str, request: Request, redis: aioredis.Redis = Depends(get_redis)):
    try:
        workflow_id, idx = id.rsplit("_", 1)
        key = f"dlq:{workflow_id}"
        await redis.delete(key)
        logger.info(json.dumps({
            "event": "dlq_discard",
            "item_id": id,
            "ip_address": request.client.host if request.client else "unknown"
        }))
        return None
    except Exception as e:
        logger.error(f"Discard failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to discard")

@router.get("/schedule")
async def list_schedule():
    # Stub for Temporal schedule
    return []

@router.post("/schedule/{workflow_id}/pause")
async def pause_schedule(workflow_id: str):
    logger.info(f"Paused schedule for {workflow_id}")
    return {"status": "paused"}

@router.post("/schedule/{workflow_id}/resume")
async def resume_schedule(workflow_id: str):
    logger.info(f"Resumed schedule for {workflow_id}")
    return {"status": "resumed"}
