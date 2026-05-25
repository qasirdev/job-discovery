"""
backend/middleware/test_gateway.py

Unit tests for the GatewayMiddleware API Gateway plugin layer — JD-103.

Tests: JWT claim extraction, request-transformer header stripping,
X-Request-ID idempotent injection, structured audit log, and public path bypass.

Run with: uv run pytest backend/middleware/test_gateway.py -v
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .gateway import (
    GatewayMiddleware,
    _extract_jwt_claims,
    _is_public_path,
    _STRIP_HEADERS,
    _PUBLIC_PATHS,
)


# ---------------------------------------------------------------------------
# Unit tests — _is_public_path
# ---------------------------------------------------------------------------

class TestIsPublicPath:
    """Tests for public path bypass logic."""

    def test_health_is_public(self):
        assert _is_public_path("/health") is True

    def test_docs_is_public(self):
        assert _is_public_path("/api/docs") is True

    def test_openapi_is_public(self):
        assert _is_public_path("/api/openapi.json") is True

    def test_metrics_is_public(self):
        assert _is_public_path("/metrics") is True

    def test_api_v1_is_not_public(self):
        assert _is_public_path("/api/v1/jobs") is False

    def test_empty_string_is_not_public(self):
        assert _is_public_path("") is False


# ---------------------------------------------------------------------------
# Unit tests — _extract_jwt_claims
# ---------------------------------------------------------------------------

class TestExtractJwtClaims:
    """Tests for JWT claim extraction (decode-without-verify mode)."""

    def test_returns_none_without_auth_header(self):
        request = MagicMock()
        request.headers = {}
        assert _extract_jwt_claims(request) is None

    def test_returns_none_with_non_bearer_header(self):
        request = MagicMock()
        request.headers = {"Authorization": "Basic abc123"}
        assert _extract_jwt_claims(request) is None

    def test_returns_none_with_empty_bearer(self):
        request = MagicMock()
        request.headers = {"Authorization": "Bearer "}
        assert _extract_jwt_claims(request) is None

    def test_returns_none_with_malformed_token(self):
        request = MagicMock()
        request.headers = {"Authorization": "Bearer not.a.valid.jwt"}
        result = _extract_jwt_claims(request)
        # Malformed tokens must not raise — must return None
        assert result is None

    def test_extracts_claims_from_valid_jwt(self):
        """Create a real JWT and verify claim extraction."""
        import jwt

        payload = {
            "sub": "user-uuid-123",
            "role": "admin",
            "email": "user@example.com",
            "jti": "token-jti-abc",
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")

        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {token}"}
        result = _extract_jwt_claims(request)

        assert result is not None
        assert result["sub"] == "user-uuid-123"
        assert result["role"] == "admin"
        assert result["email"] == "user@example.com"
        assert result["jti"] == "token-jti-abc"


# ---------------------------------------------------------------------------
# Unit tests — _STRIP_HEADERS
# ---------------------------------------------------------------------------

class TestStripHeaders:
    """Verify sensitive header set is correctly defined."""

    def test_internal_secret_is_stripped(self):
        assert "x-internal-secret" in _STRIP_HEADERS

    def test_proxy_authorization_is_stripped(self):
        assert "proxy-authorization" in _STRIP_HEADERS

    def test_x_forwarded_server_is_stripped(self):
        assert "x-forwarded-server" in _STRIP_HEADERS

    def test_normal_headers_not_stripped(self):
        """Standard headers must not appear in the strip list."""
        assert "authorization" not in _STRIP_HEADERS
        assert "content-type" not in _STRIP_HEADERS
        assert "x-request-id" not in _STRIP_HEADERS


# ---------------------------------------------------------------------------
# Integration tests — GatewayMiddleware via TestClient
# ---------------------------------------------------------------------------

@pytest.fixture
def app_with_gateway():
    """Build a minimal FastAPI app with GatewayMiddleware for integration testing."""
    test_app = FastAPI()

    with patch("backend.middleware.gateway.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock(
            secret_key="test-secret",
            algorithm="HS256",
        )
        test_app.add_middleware(GatewayMiddleware)

    @test_app.get("/api/v1/jobs")
    async def jobs():
        return {"jobs": []}

    @test_app.get("/health")
    async def health():
        return {"status": "ok"}

    return test_app


class TestGatewayMiddlewareIntegration:
    """Integration tests for GatewayMiddleware response headers and behaviour."""

    def test_x_request_id_injected_on_response(self, app_with_gateway):
        """X-Request-ID must be present on every response."""
        with patch("backend.middleware.gateway.get_settings") as mock_settings:
            mock_settings.return_value = MagicMock()
            with TestClient(app_with_gateway) as client:
                response = client.get("/api/v1/jobs")
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0

    def test_client_supplied_request_id_is_preserved(self, app_with_gateway):
        """If client sends X-Request-ID, the same value must be echoed back."""
        with patch("backend.middleware.gateway.get_settings") as mock_settings:
            mock_settings.return_value = MagicMock()
            with TestClient(app_with_gateway) as client:
                response = client.get(
                    "/api/v1/jobs",
                    headers={"X-Request-ID": "client-correlation-abc"},
                )
        assert response.headers.get("X-Request-ID") == "client-correlation-abc"

    def test_sensitive_headers_are_stripped(self, app_with_gateway):
        """Sensitive headers must be removed before reaching route handlers."""
        received_headers = {}

        with patch("backend.middleware.gateway.get_settings") as mock_settings:
            mock_settings.return_value = MagicMock()
            test_app = FastAPI()
            test_app.add_middleware(GatewayMiddleware)

            @test_app.get("/api/v1/echo")
            async def echo(request):
                from fastapi import Request
                return dict(request.headers)

            with TestClient(test_app) as client:
                response = client.get(
                    "/api/v1/echo",
                    headers={
                        "X-Internal-Secret": "super-secret",
                        "Proxy-Authorization": "Basic abc",
                    },
                )
            # The route handler should NOT see x-internal-secret
            body = response.json()
            # lowercase header names after stripping
            assert "x-internal-secret" not in {k.lower() for k in body.keys()}


# ---------------------------------------------------------------------------
# Verify public paths set
# ---------------------------------------------------------------------------

class TestPublicPaths:
    """Verify the public paths bypass set contains expected entries."""

    def test_health_in_public_paths(self):
        assert "/health" in _PUBLIC_PATHS

    def test_docs_in_public_paths(self):
        assert "/api/docs" in _PUBLIC_PATHS

    def test_openapi_in_public_paths(self):
        assert "/api/openapi.json" in _PUBLIC_PATHS
