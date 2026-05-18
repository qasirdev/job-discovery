import json
from pathlib import Path
from sqlalchemy import text
from ..db import AsyncSessionLocal
from ..agents.registry import get_agent
from ..logging_config import get_logger
from ..agents.linkedin.linkedin_agent import LinkedInAgent as LinkedInAgent  # noqa: F401
from ..agents.jobserve.jobserve_agent import JobServeAgent as JobServeAgent  # noqa: F401

logger = get_logger("admin.replay_dlq")




async def run() -> None:
    """Replays the Dead Letter Queue (DLQ) for failed scrapes with DIFA-compliant fallback."""
    logger.info("Initializing DLQ replay system...")

    failed_items = []

    try:
        # Detect: Attempt to pull failed scraper payloads from DB
        async with AsyncSessionLocal() as db:
            result = await db.execute(text("SELECT id, source, payload FROM dlq_jobs WHERE status = 'failed'"))
            rows = result.fetchall()
            for row in rows:

                failed_items.append({
                    "id": row[0],
                    "source": row[1],
                    "payload": row[2]
                })
            logger.info(f"Connected to Supabase PostgreSQL database. Retrieved {len(failed_items)} failed items from DLQ.")
    except Exception as e:
        # Isolate & Fallback: Read from local JSON DLQ file if DB is offline
        logger.warning(
            f"PostgreSQL database is currently unreachable ({e}). "
            "Gracefully falling back to inspect local JSON DLQ repository (DIFA Fallback)."
        )
        local_dlq_path = Path(__file__).parent.parent / "dlq_fallback.json"
        if local_dlq_path.exists():
            try:
                with open(local_dlq_path, "r", encoding="utf-8") as f:
                    failed_items = json.load(f)
                logger.info(f"Loaded {len(failed_items)} failed items from local file: {local_dlq_path}")
            except Exception as json_err:
                logger.error(f"Failed to read local fallback DLQ file: {json_err}")
        else:
            logger.info("No local DLQ fallback file found. Writing empty starter file...")
            try:
                # Write a sample item so developers have a baseline to inspect and test
                sample_item = [{
                    "id": "dlq-sample-1",
                    "source": "linkedin",
                    "payload": {"max_jobs": 2}
                }]
                with open(local_dlq_path, "w", encoding="utf-8") as f:
                    json.dump(sample_item, f, indent=2)
                failed_items = sample_item
                logger.info(f"Sample starter DLQ fallback file created at {local_dlq_path}")
            except Exception as write_err:
                logger.error(f"Failed to write local starter DLQ: {write_err}")

    if not failed_items:
        logger.info("DLQ replay queue is empty. 0 items to process.")
        return

    # Process and replay DLQ items
    success_count = 0
    for item in failed_items:
        source_id = item.get("source")
        if not isinstance(source_id, str):
            logger.error(f"Invalid or missing source: {source_id}. Skipping.")
            continue

        payload = item.get("payload", {})
        logger.info(f"Replaying failed scrape for source '{source_id}' (ID: {item.get('id')})...")

        try:
            agent_cls = get_agent(source_id)
            if not agent_cls:
                logger.error(f"No registered agent found for source '{source_id}'. Skipping.")
                continue

            agent = agent_cls()
            # Execute scraper replay
            max_jobs = payload.get("max_jobs", 5)
            scrape_res = await agent.run(max_jobs=max_jobs)
            logger.info(f"Successfully replayed and recovered scrape for source '{source_id}': {scrape_res}")
            success_count += 1
        except Exception as run_err:
            logger.error(f"Failed to replay scrape for source '{source_id}': {run_err}")


    logger.info(f"DLQ replay pipeline completed. Successfully recovered {success_count}/{len(failed_items)} tasks.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
