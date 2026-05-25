"""
backend/middleware/rate_limit.py

Redis-backed sliding window rate limiter — JD-102.

Per-endpoint rate limits enforced at the FastAPI middleware layer (API Gateway level):
  - GET  /api/v1/jobs            → 300 req/min
  - POST /api/v1/cover-letter/*  → 20 req/min
  - POST /api/v1/question-answer/* → 30 req/min
  - POST /api/v1/interview-prep/* → 10 req/min
  - POST /api/v1/scrape          → 1 concurrent globally (handled by asyncio.Lock / Redis lock)
  - ANY  *                       → 600 req/min (general usage cap)

The /health endpoint is always bypassed.

Implementation: sliding window log via Redis ZADD + ZREMRANGEBYSCORE.
Keys: rate:<endpoint_tag>:<user_key>  — uses SINGLE_USER_ID when JWT sub is present,
falling back to client IP for unauthenticated requests.

Reference: proposal-v4-structure.md RATE LIMITING STRATEGY table.
"""

import time
import math
import re
from typing import Optional

import redis.asyncio as aioredis
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from ..logging_config import get_logger

logger = get_logger("rate_limiter")

# ---------------------------------------------------------------------------
# Endpoint → (window_seconds, max_requests) map
# Ordered from most specific to most general — first match wins.
# ---------------------------------------------------------------------------
_ENDPOINT_RULES: list[tuple[str, str, int, int]] = [
    # (method_pattern, path_pattern, window_seconds, max_requests)
    ("GET",  r"^/api/v1/jobs(?:/|$)", 60, 300),
    ("POST", r"^/api/v1/cover-letter/", 60, 20),
    ("POST", r"^/api/v1/question-answer/", 60, 30),
    ("POST", r"^/api/v1/interview-prep/", 60, 10),
    # Scrape is limited to 1 concurrent globally via asyncio.Lock / Redis lock in scrape.py
    # No sliding window rate limit added here for scrape — the lock is the gate.
    ("ANY",  r"^/api/", 60, 600),  # General API cap — any method
]

# Endpoints that are never rate-limited
_BYPASS_PATHS: set[str] = {"/health", "/api/docs", "/api/openapi.json", "/metrics"}

_COMPILED_RULES: list[tuple[str, re.Pattern, int, int]] = [
    (method, re.compile(pattern), window, limit)
    for method, pattern, window, limit in _ENDPOINT_RULES
]


def _match_rule(method: str, path: str) -> Optional[tuple[str, int, int]]:
    """Return (tag, window_seconds, max_requests) for the first matching rule, or None."""
    for rule_method, pattern, window, limit in _COMPILED_RULES:
        if rule_method != "ANY" and rule_method != method.upper():
            continue
        if pattern.search(path):
            tag = pattern.pattern.rstrip("/.*").lstrip("^/").replace("/", "_").replace(".", "")
            return tag, window, limit
    return None


def _user_key(request: Request) -> str:
    """
    Derive a low-cardinality rate-limit key for the request.

    Priority:
    1. JWT sub claim injected by OWASPMiddleware / auth middleware (stored in request.state)
    2. X-Forwarded-For header (first IP)
    3. Direct client host
    """
    # Auth middleware may inject claims into request.state
    claims = getattr(request.state, "jwt_claims", None)
    if claims and claims.get("sub"):
        return f"user:{claims['sub']}"

    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
        return f"ip:{ip}"

    host = request.client.host if request.client else "unknown"
    return f"ip:{host}"


async def _sliding_window_check(
    redis: aioredis.Redis,
    key: str,
    window_seconds: int,
    max_requests: int,
) -> tuple[bool, int, int]:
    """
    Sliding window log algorithm using a Redis sorted set.

    Returns:
        (allowed: bool, remaining: int, retry_after_seconds: int)
    """
    now = time.time()
    window_start = now - window_seconds

    pipe = redis.pipeline()
    # Remove timestamps outside the window
    pipe.zremrangebyscore(key, "-inf", window_start)
    # Count remaining in window
    pipe.zcard(key)
    # Add current timestamp
    pipe.zadd(key, {str(now): now})
    # Set TTL to window_seconds + 1 (auto-cleanup)
    pipe.expire(key, window_seconds + 1)
    results = await pipe.execute()

    request_count: int = results[1]  # count BEFORE adding current request

    if request_count >= max_requests:
        # Find oldest entry to calculate Retry-After
        oldest = await redis.zrange(key, 0, 0, withscores=True)
        retry_after = 1
        if oldest:
            oldest_ts = oldest[0][1]
            retry_after = max(1, math.ceil(oldest_ts + window_seconds - now))
        remaining = 0
        return False, remaining, retry_after

    remaining = max(0, max_requests - request_count - 1)
    return True, remaining, 0


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI/Starlette middleware that enforces per-endpoint sliding window rate limits
    using Redis as a distributed counter store.

    Plugs into the same Redis connection pool stored on app.state.redis by the
    lifespan context manager in main.py.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        method = request.method

        # Always bypass certain paths
        if path in _BYPASS_PATHS or any(path.startswith(p) for p in _BYPASS_PATHS):
            return await call_next(request)

        redis: aioredis.Redis | None = getattr(request.app.state, "redis", None)
        if redis is None:
            # No Redis available — degrade gracefully (allow request through, log warning)
            logger.warning(
                "rate_limiter_degraded",
                extra={"reason": "Redis not available on app.state", "path": path},
            )
            return await call_next(request)

        rule = _match_rule(method, path)
        if rule is None:
            return await call_next(request)

        tag, window_seconds, max_requests = rule
        user_key = _user_key(request)
        redis_key = f"rate:{tag}:{user_key}"

        try:
            allowed, remaining, retry_after = await _sliding_window_check(
                redis, redis_key, window_seconds, max_requests
            )
        except Exception as exc:
            # Redis failure → fail open (allow request, log error)
            logger.error(
                "rate_limiter_redis_error",
                extra={"error": str(exc), "path": path},
            )
            return await call_next(request)

        if not allowed:
            logger.warning(
                "rate_limit_exceeded",
                extra={
                    "path": path,
                    "method": method,
                    "user_key": user_key,
                    "limit": max_requests,
                    "window_seconds": window_seconds,
                    "retry_after": retry_after,
                },
            )
            return JSONResponse(
                status_code=429,
                content={
                    "type": "about:blank",
                    "title": "Too Many Requests",
                    "status": 429,
                    "detail": (
                        f"Rate limit exceeded: {max_requests} requests per "
                        f"{window_seconds}s for this endpoint. "
                        f"Retry after {retry_after}s."
                    ),
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + retry_after),
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"] = str(window_seconds)
        return response
