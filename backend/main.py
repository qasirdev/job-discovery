from contextlib import asynccontextmanager
from typing import AsyncGenerator
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis

from .settings import get_settings
from .logging_config import get_logger, request_id_ctx

# Import registry and agents for auto-registration
from .agents import registry
from .agents.linkedin import linkedin_agent
from .agents.jobserve import jobserve_agent
from .agents.observability.observability_agent import ObservabilityAgent
from .agents.security.security_agent import OWASPMiddleware

from .api.v1 import scrape, jobs, profile, cv, feature_flags, admin, observability

try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from prometheus_fastapi_instrumentator import Instrumentator
    OBSERVABILITY_DEPS_LOADED = True
except ImportError:
    OBSERVABILITY_DEPS_LOADED = False

logger = get_logger(__name__)

if OBSERVABILITY_DEPS_LOADED:
    settings = get_settings()
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=0.1,
            environment=settings.environment,
            release=settings.app_version,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration()
            ]
        )

def custom_operation_id(route: APIRoute) -> str:
    """Generate unique operation ID for SDK generation."""
    tag = route.tags[0].lower().replace(" ", "_") if route.tags else "api"
    name = route.name.replace("_", "-")
    return f"{tag}:{name}"

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    logger.info("Starting up FastAPI application. App ready.")
    settings = get_settings()
    app.state.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    app.state.obs_task = obs_agent.start_background_task()
    yield
    app.state.obs_task.cancel()
    await app.state.redis.aclose()
    logger.info("Shutting down FastAPI application")

app = FastAPI(
    title="Job Discovery API",
    description="AI-Powered Job Discovery Platform",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
    generate_unique_id_function=custom_operation_id,
)

if OBSERVABILITY_DEPS_LOADED:
    Instrumentator().instrument(app).expose(app)

# Enable CORS for local Next.js development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

obs_agent = ObservabilityAgent()
obs_agent.instrument_fastapi_app(app)

app.add_middleware(OWASPMiddleware)

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
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
    return {"status": "ok", "version": "1.0.0"}

# Mount versioned API routes
app.include_router(scrape.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")
app.include_router(cv.router, prefix="/api/v1")
app.include_router(feature_flags.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(observability.router, prefix="/api/v1")
