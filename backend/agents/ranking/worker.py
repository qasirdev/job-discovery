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

from ..orchestrator.orchestrator_agent import rank_job
from ...settings import get_settings
from ...logging_config import get_logger

logger = get_logger("ranking_temporal_worker")

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
        task_queue="ranking-tasks",
        activities=[rank_job],
        interceptors=interceptors,
    )

    # JD-72: Graceful SIGTERM handler — drains in-progress ranking activities before Docker SIGKILL.
    loop = asyncio.get_event_loop()

    def shutdown_handler(sig, frame):
        logger.warning(f"Received signal {sig}. Initiating graceful ranking worker shutdown...")
        loop.create_task(worker.shutdown())

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    logger.info("Starting Ranking Temporal Worker on 'ranking-tasks' queue...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

