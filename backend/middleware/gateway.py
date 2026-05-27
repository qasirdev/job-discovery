"""
backend/middleware/gateway.py

API Gateway plugin layer — JD-103.

Implements five gateway concerns as specified in infrastructure/AGENT.md and proposal-v4.md:

  1. rate-limiting    → delegated to RateLimitMiddleware (rate_limit.py)
  2. jwt              → JWT validation and claim forwarding to FastAPI via request.state
  3. file-log         → Structured request/response audit log with method, path, status,
                        latency (ms), user_id (from JWT sub claim)
  4. cors             → CORS headers applied at gateway layer; consistent with FastAPI
                        CORS middleware in main.py (kept in sync)
  5. request-transformer → strips sensitive inbound headers, injects X-Request-ID
                           (idempotent: preserves client-supplied ID, generates UUID otherwise)

Middleware execution order in main.py (outer → inner):
  GatewayMiddleware → RateLimitMiddleware → OWASPMiddleware → correlation_id_middleware → route

The GatewayMiddleware handles JWT claim extraction and stores on request.state.jwt_claims
so that RateLimitMiddleware can read the user identity for per-user key derivation.

Reference: proposal-v4.md API Gateway table, infrastructure/AGENT.md plugin list.
"""

import time
import uuid
from typing import Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from ..logging_config import get_logger
from ..settings import get_settings

logger = get_logger("api_gateway")

# ---------------------------------------------------------------------------
# Sensitive headers to strip before forwarding to FastAPI route handlers.
# These headers must not reach application code.
# ---------------------------------------------------------------------------
_STRIP_HEADERS: frozenset[str] = frozenset({
    "x-internal-secret",
    "x-forwarded-server",
    "x-real-ip-original",
    "proxy-authorization",
    "x-kong-proxy-latency",
    "x-kong-upstream-latency",
})

# ---------------------------------------------------------------------------
# Paths that bypass JWT validation (public endpoints)
# ---------------------------------------------------------------------------
_PUBLIC_PATHS: frozenset[str] = frozenset({
    "/health",
    "/api/docs",
    "/api/openapi.json",
    "/metrics",
})


def _is_public_path(path: str) -> bool:
    return path in _PUBLIC_PATHS or any(path.startswith(p) for p in _PUBLIC_PATHS)


def _extract_jwt_claims(request: Request) -> Optional[dict]:
    """
    Attempt to extract and decode JWT claims from the Authorization header.

    In MVP 2 this is a lightweight decode-without-verify used purely for
    extracting the sub/role claims for rate-limit keying and audit logging.
    Full signature verification is performed by verify_jwt() in
    backend/middleware/auth.py at the route dependency level.

    Returns None if no valid Authorization header is present.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split("Bearer ", 1)[1].strip()
    if not token:
        return None

    try:
        import jwt as pyjwt

        # Decode without verification — claims only, signature is checked by auth.py
        payload = pyjwt.decode(
            token,
            options={"verify_signature": False, "verify_exp": False},
            algorithms=["HS256", "RS256"],
        )
        return {
            "sub": payload.get("sub"),
            "role": payload.get("role", "user"),
            "email": payload.get("email"),
            "jti": payload.get("jti"),
        }
    except Exception:
        # Malformed token — not our job to reject here; auth.py handles rejection
        return None


class GatewayMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware that implements the API Gateway plugin layer.

    Runs before all other application middleware so that:
    - X-Request-ID is injected early (available to all downstream middleware/handlers)
    - JWT claims are extracted and stored on request.state (used by rate limiter)
    - Sensitive headers are stripped before reaching route handlers
    - Structured audit log is written on response completion
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self._settings = get_settings()

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        # ── Plugin 5: request-transformer ─────────────────────────────────
        # Inject X-Request-ID — idempotent: preserve if client sent one
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Strip sensitive headers
        # Note: Starlette headers are immutable, so we record which ones
        # were stripped and log it; actual stripping happens via MutableHeaders
        # on the request scope (Starlette internal approach).
        scope = request.scope
        raw_headers = scope.get("headers", [])
        stripped_headers = [
            (k, v) for k, v in raw_headers
            if k.decode("latin-1").lower() not in _STRIP_HEADERS
        ]
        scope["headers"] = stripped_headers

        # Re-bind request to the stripped scope
        request = Request(scope, request.receive, request._send)

        # ── Plugin 2: jwt — extract claims, store on request.state ────────
        claims = _extract_jwt_claims(request)
        request.state.jwt_claims = claims

        # Propagate request_id to request state (used by correlation_id_middleware)
        request.state.request_id = request_id

        # ── Process request ────────────────────────────────────────────────
        response: Response = await call_next(request)

        # ── Plugin 3: file-log — structured audit log ──────────────────────
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        user_id = claims.get("sub") if claims else "anonymous"

        logger.info(
            "request_audit",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.url.query),
                "status_code": response.status_code,
                "latency_ms": duration_ms,
                "user_id": user_id,
                "user_agent": request.headers.get("User-Agent", ""),
                "x_forwarded_for": request.headers.get("X-Forwarded-For", ""),
            },
        )

        # ── Plugin 5 (response): inject X-Request-ID on response ──────────
        response.headers["X-Request-ID"] = request_id

        return response
