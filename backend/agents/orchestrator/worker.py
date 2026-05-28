import asyncio
import signal
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
            personalise_results,
            notify_user,
            route_to_dlq
        ],
        interceptors=interceptors,
    )

    # JD-72: Graceful SIGTERM handler — drains in-progress activities before Docker SIGKILL at 30s.
    # All cleanup must complete within 25 seconds (5s buffer before supervisor stopwaitsecs=30).
    loop = asyncio.get_event_loop()

    def shutdown_handler(sig, frame):
        logger.warning(f"Received signal {sig}. Initiating graceful Temporal worker shutdown...")
        loop.create_task(worker.shutdown())

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    logger.info("Starting Temporal Worker (orchestrator) on 'job-discovery-tasks' queue...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

