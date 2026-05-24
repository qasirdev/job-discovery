import asyncio
import sys

from temporalio.client import Client
from temporalio.worker import Worker
try:
    from temporalio.contrib.opentelemetry import TracingInterceptor
    OTEL_TEMPORAL_AVAILABLE = True
except ImportError:
    OTEL_TEMPORAL_AVAILABLE = False

from .orchestrator_agent import (
    ScrapeAndRankWorkflow,
    scrape_all_sources,
    security_check,
    rank_job,
    personalise_results,
    notify_user,
    route_to_dlq
)
from ...settings import get_settings
from ...logging_config import get_logger

logger = get_logger("temporal_worker")

async def main():
    settings = get_settings()
    url = settings.temporal_server_url or "localhost:7233"
    interceptors = [TracingInterceptor()] if OTEL_TEMPORAL_AVAILABLE else []
    
    if not settings.temporal_server_url:
        logger.warning("TEMPORAL_SERVER_URL not set. Falling back to localhost:7233 for development.")
    
    try:
        client = await Client.connect(url, interceptors=interceptors)
    except Exception as e:
        logger.error(f"Failed to connect to Temporal at {url}. Error: {e}")
        sys.exit(1)

    worker = Worker(
        client,
        task_queue="job-discovery-tasks",
        workflows=[ScrapeAndRankWorkflow],
        activities=[
            scrape_all_sources,
            security_check,
            rank_job,
            personalise_results,
            notify_user,
            route_to_dlq
        ],
        interceptors=interceptors,
    )
    
    logger.info("Starting Temporal Worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
