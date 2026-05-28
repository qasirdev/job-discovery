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

from .application_agent import execute_assistant_activity, ApplicationAssistantWorkflow
from ...settings import get_settings
from ...logging_config import get_logger

logger = get_logger("application_temporal_worker")

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
        task_queue="application-tasks",
        workflows=[ApplicationAssistantWorkflow],
        activities=[execute_assistant_activity],
        interceptors=interceptors,
    )

    # JD-72: Graceful SIGTERM handler — drains in-progress application assistant activities before Docker SIGKILL.
    loop = asyncio.get_event_loop()

    def shutdown_handler(sig, frame):
        logger.warning(f"Received signal {sig}. Initiating graceful application assistant worker shutdown...")
        loop.create_task(worker.shutdown())

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    logger.info("Starting Application Assistant Temporal Worker on 'application-tasks' queue...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
