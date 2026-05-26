import asyncio
import sys

from temporalio.client import Client
from temporalio.worker import Worker
try:
    from temporalio.contrib.opentelemetry import TracingInterceptor
    OTEL_TEMPORAL_AVAILABLE = True
except ImportError:
    OTEL_TEMPORAL_AVAILABLE = False

from .interview_agent import generate_interview_prep_activity, InterviewPrepWorkflow
from ...settings import get_settings
from ...logging_config import get_logger

logger = get_logger("interview_temporal_worker")

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
        task_queue="interview-tasks",
        workflows=[InterviewPrepWorkflow],
        activities=[generate_interview_prep_activity],
        interceptors=interceptors,
    )
    
    logger.info("Starting Interview Prep Temporal Worker on 'interview-tasks' queue...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
