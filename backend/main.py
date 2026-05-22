from contextlib import asynccontextmanager
from typing import AsyncGenerator
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from .logging_config import get_logger, request_id_ctx
from .routers import scrape, jobs
from .agents.observability.observability_agent import ObservabilityAgent

logger = get_logger(__name__)

def custom_operation_id(route: APIRoute) -> str:
    """Generate unique operation ID for SDK generation."""
    tag = route.tags[0].lower().replace(" ", "_") if route.tags else "api"
    name = route.name.replace("_", "-")
    return f"{tag}:{name}"


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
    generate_unique_id_function=custom_operation_id,
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
async def correlation_id_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
    """Inject correlation ID and log incoming requests."""
    rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request_id_ctx.set(rid)
    
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    
    response.headers["X-Request-ID"] = rid
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

