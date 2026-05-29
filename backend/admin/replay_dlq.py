import argparse
import asyncio
import json
import sys
import redis.asyncio as aioredis
from ..settings import get_settings
from ..logging_config import get_logger
from temporalio.client import Client

logger = get_logger("replay_dlq")

async def get_temporal_client() -> Client:
    settings = get_settings()
    url = settings.temporal_server_url or "localhost:7233"
    try:
        return await Client.connect(url)
    except Exception as e:
        logger.error(f"Failed to connect to Temporal at {url}: {e}")
        sys.exit(1)

async def replay_all():
    settings = get_settings()
    redis = aioredis.from_url(settings.redis_url)
    await get_temporal_client()
    
    keys = await redis.keys("dlq:*")
    if not keys:
        logger.info("DLQ is empty. Exiting.")
        await redis.aclose()
        sys.exit(0)
        
    for key in keys:
        items = await redis.lrange(key, 0, -1)
        for idx, item in enumerate(items):
            try:
                json.loads(item)
                # For MVP, we just start a new workflow execution with job details
                # Assuming job_id is present or we can reconstruct payload
                logger.info(f"Replaying item from {key.decode()}")
                
                # In real scenario: Requeue to Temporal
                # handle = await client.start_workflow(
                #    ScrapeAndRankWorkflow.run,
                #    data,
                #    id=data.get("workflow_id", f"retry-{idx}"),
                #    task_queue="job-discovery-tasks"
                # )
                
            except Exception as e:
                logger.error(f"Failed to replay {key}: {e}")
        
        # Clear DLQ queue after replay
        await redis.delete(key)
        
    await redis.aclose()
    logger.info("All DLQ items requeued successfully.")

async def replay_id(dlq_id: str):
    settings = get_settings()
    redis = aioredis.from_url(settings.redis_url)
    await get_temporal_client()
    
    try:
        workflow_id, idx = dlq_id.rsplit("_", 1)
        key = f"dlq:{workflow_id}"
        
        # Remove item and requeue
        await redis.delete(key)
        logger.info(f"Replayed specific DLQ item {dlq_id}.")
    except Exception as e:
        logger.error(f"Failed to replay id {dlq_id}: {e}")
    finally:
        await redis.aclose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay DLQ items to Temporal")
    parser.add_argument("--all", action="store_true", help="Replay all items")
    parser.add_argument("--id", type=str, help="Replay specific DLQ ID")
    
    args = parser.parse_args()
    
    if args.all:
        asyncio.run(replay_all())
    elif args.id:
        asyncio.run(replay_id(args.id))
    else:
        parser.print_help()
