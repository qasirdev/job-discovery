from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, Dict, List
from fastapi import FastAPI, Request
import time
from .logging_config import get_logger
from .routers import scrape, jobs

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    print("Starting up")
    yield
    print("Shutting down")


app = FastAPI(
    title="Job Discovery Platform API",
    description="AI-Powered Job Discovery Platform",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# In-memory DB for MVP 1
# This will be replaced by asyncpg / Supabase in MVP 2
fake_db: Dict[str, List[Any]] = {"jobs": []}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming HTTP requests."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    # We log JSON naturally via our configured logger.
    # For now, we inject into a standard string message.
    # In a fully integrated OpenTelemetry setup, we would inject span attributes.
    logger.info(
        f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {duration:.4f}s"
    )
    return response


@app.get("/health")
async def health_check():
    """Return healthy status for readiness probe."""
    return {"status": "healthy"}

# Mount versioned API routes
app.include_router(scrape.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
