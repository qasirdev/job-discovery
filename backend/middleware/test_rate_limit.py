"""
backend/middleware/test_rate_limit.py

Unit tests for the RateLimitMiddleware (JD-102).

Tests the sliding window logic, per-endpoint rule matching, bypass paths,
Redis failure graceful degradation, and response header injection.

Run with: uv run pytest backend/middleware/test_rate_limit.py -v
"""

import pytest
import time
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .rate_limit import (
    RateLimitMiddleware,
    _match_rule,
    _user_key,
    _sliding_window_check,
    _BYPASS_PATHS,
)


# ---------------------------------------------------------------------------
# Unit tests — _match_rule
# ---------------------------------------------------------------------------

class TestMatchRule:
    """Tests for the endpoint rule matching logic."""

    def test_matches_jobs_get(self):
        result = _match_rule("GET", "/api/v1/jobs")
        assert result is not None
        _, window, limit = result
        assert window == 60
        assert limit == 300

    def test_matches_jobs_with_trailing_slash(self):
        result = _match_rule("GET", "/api/v1/jobs/")
        assert result is not None
        _, window, limit = result
        assert limit == 300

    def test_matches_jobs_with_id(self):
        """Job detail endpoint should match the jobs rule."""
        result = _match_rule("GET", "/api/v1/jobs/abc-123")
        assert result is not None
        _, window, limit = result
        assert limit == 300

    def test_matches_cover_letter_post(self):
        result = _match_rule("POST", "/api/v1/cover-letter/some-job-id")
        assert result is not None
        _, window, limit = result
        assert limit == 20

    def test_does_not_match_cover_letter_get(self):
        """GET on cover-letter should fall through to general cap."""
        result = _match_rule("GET", "/api/v1/cover-letter/some-job-id")
        assert result is not None
        # Should match general API cap, not the 20 req/min cover-letter rule
        _, window, limit = result
        assert limit == 600  # General cap

    def test_matches_question_answer_post(self):
        result = _match_rule("POST", "/api/v1/question-answer/job-id")
        assert result is not None
        _, window, limit = result
        assert limit == 30

    def test_matches_interview_prep_post(self):
        result = _match_rule("POST", "/api/v1/interview-prep/job-id")
        assert result is not None
        _, window, limit = result
        assert limit == 10

    def test_matches_general_api_any_method(self):
        """Any /api/ path should match the general cap."""
        result = _match_rule("DELETE", "/api/v1/profile")
        assert result is not None
        _, window, limit = result
        assert limit == 600

    def test_no_match_for_non_api_path(self):
        """Non-API paths return None (no rate limiting)."""
        result = _match_rule("GET", "/some-random-path")
        assert result is None

    def test_most_specific_rule_wins(self):
        """Cover letter rule (20/min) must win over general API cap (600/min)."""
        result = _match_rule("POST", "/api/v1/cover-letter/job-123")
        assert result is not None
        _, _, limit = result
        assert limit == 20, "Most specific rule must win — 20 req/min, not 600"


# ---------------------------------------------------------------------------
# Unit tests — _user_key
# ---------------------------------------------------------------------------

class TestUserKey:
    """Tests for user key derivation."""

    def _make_request(self, jwt_sub=None, forwarded_for=None, client_host="127.0.0.1"):
        request = MagicMock()
        if jwt_sub:
            request.state.jwt_claims = {"sub": jwt_sub}
        else:
            request.state.jwt_claims = None
        request.headers = {}
        if forwarded_for:
            request.headers = {"X-Forwarded-For": forwarded_for}
        request.client = MagicMock()
        request.client.host = client_host
        return request

    def test_jwt_sub_takes_priority(self):
        request = self._make_request(jwt_sub="user-uuid-123")
        key = _user_key(request)
        assert key == "user:user-uuid-123"

    def test_forwarded_for_used_when_no_jwt(self):
        request = self._make_request(forwarded_for="10.0.0.1, 10.0.0.2")
        key = _user_key(request)
        assert key == "ip:10.0.0.1"  # First IP in chain

    def test_client_host_fallback(self):
        request = self._make_request()
        key = _user_key(request)
        assert key == "ip:127.0.0.1"


# ---------------------------------------------------------------------------
# Unit tests — _sliding_window_check
# ---------------------------------------------------------------------------

class TestSlidingWindowCheck:
    """Tests for the Redis sliding window algorithm."""

    @pytest.mark.asyncio
    async def test_allows_request_under_limit(self):
        """Sliding window allows requests under the limit."""
        # Use a real-like pipeline mock with proper async execute
        pipe = MagicMock()
        pipe.zremrangebyscore = MagicMock(return_value=pipe)
        pipe.zcard = MagicMock(return_value=pipe)
        pipe.zadd = MagicMock(return_value=pipe)
        pipe.expire = MagicMock(return_value=pipe)
        pipe.execute = AsyncMock(return_value=[0, 5, 1, 1])  # 5 in window

        redis = MagicMock()
        redis.pipeline = MagicMock(return_value=pipe)
        redis.zrange = AsyncMock(return_value=[])

        allowed, remaining, retry_after = await _sliding_window_check(
            redis, "rate:key:user", 60, 300
        )
        assert allowed is True
        assert remaining == 294  # 300 - 5 - 1
        assert retry_after == 0

    @pytest.mark.asyncio
    async def test_blocks_request_over_limit(self):
        """Sliding window blocks requests at or over the limit."""
        now = time.time()

        pipe = MagicMock()
        pipe.zremrangebyscore = MagicMock(return_value=pipe)
        pipe.zcard = MagicMock(return_value=pipe)
        pipe.zadd = MagicMock(return_value=pipe)
        pipe.expire = MagicMock(return_value=pipe)
        pipe.execute = AsyncMock(return_value=[0, 300, 1, 1])  # 300 in window — at limit

        redis = MagicMock()
        redis.pipeline = MagicMock(return_value=pipe)
        # Oldest entry is 55 seconds old → Retry-After ≈ 5s
        redis.zrange = AsyncMock(return_value=[(b"ts", now - 55)])

        allowed, remaining, retry_after = await _sliding_window_check(
            redis, "rate:key:user", 60, 300
        )
        assert allowed is False
        assert remaining == 0
        assert retry_after >= 1


# ---------------------------------------------------------------------------
# Integration tests — RateLimitMiddleware via TestClient
# ---------------------------------------------------------------------------

@pytest.fixture
def app_with_rate_limiter():
    """Build a minimal FastAPI app with RateLimitMiddleware for integration testing."""
    test_app = FastAPI()
    test_app.add_middleware(RateLimitMiddleware)

    @test_app.get("/api/v1/jobs")
    async def jobs():
        return {"jobs": []}

    @test_app.get("/health")
    async def health():
        return {"status": "ok"}

    return test_app


class TestRateLimitMiddlewareIntegration:
    """Integration tests using FastAPI TestClient."""

    def test_health_bypass_no_rate_limit_headers(self, app_with_rate_limiter):
        """Health endpoint is always bypassed — no X-RateLimit headers."""
        with TestClient(app_with_rate_limiter) as client:
            response = client.get("/health")
        assert response.status_code == 200
        assert "X-RateLimit-Limit" not in response.headers

    def test_degrades_gracefully_without_redis(self, app_with_rate_limiter):
        """Without Redis on app.state, requests must pass through (fail-open)."""
        with TestClient(app_with_rate_limiter) as client:
            response = client.get("/api/v1/jobs")
        # Should succeed — middleware degrades gracefully when Redis is absent
        assert response.status_code == 200

    def test_rate_limit_headers_present_with_redis(self, app_with_rate_limiter):
        """When Redis is present and allows the request, response headers are set."""
        # Build a synchronous-compatible mock pipeline (Starlette TestClient runs async in thread)
        pipe = MagicMock()
        pipe.zremrangebyscore = MagicMock(return_value=pipe)
        pipe.zcard = MagicMock(return_value=pipe)
        pipe.zadd = MagicMock(return_value=pipe)
        pipe.expire = MagicMock(return_value=pipe)
        pipe.execute = AsyncMock(return_value=[0, 0, 1, 1])  # 0 in window → first request

        mock_redis = MagicMock()
        mock_redis.pipeline = MagicMock(return_value=pipe)
        mock_redis.zrange = AsyncMock(return_value=[])

        app_with_rate_limiter.state.redis = mock_redis

        with TestClient(app_with_rate_limiter) as client:
            response = client.get("/api/v1/jobs")

        assert response.status_code == 200
        # Headers should be present when rate limiting is active
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Window" in response.headers


# ---------------------------------------------------------------------------
# Bypass path tests
# ---------------------------------------------------------------------------

class TestBypassPaths:
    """Verify the bypass path set contains expected entries."""

    def test_health_is_bypassed(self):
        assert "/health" in _BYPASS_PATHS

    def test_docs_is_bypassed(self):
        assert "/api/docs" in _BYPASS_PATHS

    def test_openapi_is_bypassed(self):
        assert "/api/openapi.json" in _BYPASS_PATHS

    def test_metrics_is_bypassed(self):
        assert "/metrics" in _BYPASS_PATHS
