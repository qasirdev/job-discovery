from contextlib import asynccontextmanager
from typing import AsyncGenerator

import time

from fastapi import FastAPI, Request

from .logging_config import get_logger
from .routers import scrape, jobs

from fastapi.middleware.cors import CORSMiddleware
from .agents.observability.observability_agent import ObservabilityAgent

logger = get_logger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    print("Starting up")
    yield
    print("Shutting down")

# from functools import lru_cache
# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     """Settings class docstring."""
#     app_name: str = "Users API"
#     app_version: str = "1.0.0"
#     debug: bool = False
#     allowed_origins: list[str] = ["http://localhost:3000"]

#     model_config = {"env_file": ".env"}

# # Least Recently Used cache
# @lru_cache
# def get_settings() -> Settings:
#     """get_settings function docstring."""
#     return Settings()

    # docs_url="/docs" if settings.debug else None,
    # redoc_url="/redoc" if settings.debug else None,
    # openapi_url="/openapi.json" if settings.debug else None,
app = FastAPI(
    title="Job Discovery Platform API",
    description="AI-Powered Job Discovery Platform",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Enable CORS for local Next.js development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

obs_agent = ObservabilityAgent()
obs_agent.instrument_fastapi_app(app)





@app.middleware("http")
async def log_requests(request: Request, call_next):  # type: ignore[no-untyped-def]
    """Log all incoming HTTP requests with method, path, status code, and duration."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.4f}s"
    )
    return response


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return healthy status for readiness probe."""
    return {"status": "healthy"}


# Mount versioned API routes
app.include_router(scrape.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")

