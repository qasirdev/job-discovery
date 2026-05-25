"""
backend/agents/test_proxy.py

Unit tests for the ProxyManager proxy abstraction layer — JD-104.

Tests round-robin datacenter rotation, residential escalation on antibot triggers,
trigger counter reset, and graceful no-proxy fallback.

Run with: uv run pytest backend/agents/test_proxy.py -v
"""

import pytest
from unittest.mock import patch, MagicMock

from .proxy import ProxyManager, _state


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_proxy_state():
    """Reset the module-level shared state before each test."""
    _state.antibot_triggers = 0
    _state.residential_escalated = False
    yield
    _state.antibot_triggers = 0
    _state.residential_escalated = False


def _make_proxy_manager(
    datacenter_urls: str | None = None,
    residential_url: str | None = None,
) -> ProxyManager:
    """Factory that creates a ProxyManager with mocked settings."""
    mock_settings = MagicMock()
    mock_settings.proxy_pool_urls = datacenter_urls
    mock_settings.residential_proxy_url = residential_url

    with patch("backend.agents.proxy.get_settings", return_value=mock_settings):
        return ProxyManager()


# ---------------------------------------------------------------------------
# No-proxy fallback
# ---------------------------------------------------------------------------

class TestNoProxy:
    """When no proxies are configured, direct connection must be used."""

    def test_rotate_proxy_returns_none(self):
        pm = _make_proxy_manager()
        assert pm.rotate_proxy() is None

    def test_get_playwright_proxy_returns_none(self):
        pm = _make_proxy_manager()
        assert pm.get_playwright_proxy() is None

    def test_has_proxies_is_false(self):
        pm = _make_proxy_manager()
        assert pm.has_proxies is False


# ---------------------------------------------------------------------------
# Datacenter pool — round-robin
# ---------------------------------------------------------------------------

class TestDatacenterPool:
    """Tests for round-robin rotation across datacenter proxies."""

    def test_single_proxy_always_returned(self):
        pm = _make_proxy_manager(datacenter_urls="http://proxy1.example.com:8080")
        for _ in range(5):
            assert pm.rotate_proxy() == "http://proxy1.example.com:8080"

    def test_two_proxies_round_robin(self):
        pm = _make_proxy_manager(
            datacenter_urls="http://proxy1.example.com:8080,http://proxy2.example.com:8080"
        )
        results = [pm.rotate_proxy() for _ in range(4)]
        assert results == [
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            "http://proxy1.example.com:8080",  # wraps around
            "http://proxy2.example.com:8080",
        ]

    def test_whitespace_stripped_from_urls(self):
        pm = _make_proxy_manager(
            datacenter_urls="  http://proxy1.example.com:8080  ,  http://proxy2.example.com:8080  "
        )
        assert pm.rotate_proxy() == "http://proxy1.example.com:8080"

    def test_playwright_proxy_format(self):
        pm = _make_proxy_manager(datacenter_urls="http://user:pass@proxy1.example.com:8080")
        result = pm.get_playwright_proxy()
        assert result == {"server": "http://user:pass@proxy1.example.com:8080"}

    def test_has_proxies_is_true_with_datacenter_pool(self):
        pm = _make_proxy_manager(datacenter_urls="http://proxy1.example.com:8080")
        assert pm.has_proxies is True


# ---------------------------------------------------------------------------
# Antibot escalation — residential proxy
# ---------------------------------------------------------------------------

class TestAntibotEscalation:
    """Tests for automatic escalation to residential proxy on antibot triggers."""

    def test_residential_proxy_not_used_below_threshold(self):
        pm = _make_proxy_manager(
            datacenter_urls="http://proxy1.example.com:8080",
            residential_url="http://user:pass@residential.proxy.net:8080",
        )
        # 2 triggers — below threshold of 3
        pm.report_antibot_trigger(reason="captcha_detected")
        pm.report_antibot_trigger(reason="dom_stability_anomaly")
        result = pm.rotate_proxy()
        assert result == "http://proxy1.example.com:8080"

    def test_residential_proxy_used_at_threshold(self):
        pm = _make_proxy_manager(
            datacenter_urls="http://proxy1.example.com:8080",
            residential_url="http://user:pass@residential.proxy.net:8080",
        )
        # Exactly 3 triggers → threshold reached
        pm.report_antibot_trigger()
        pm.report_antibot_trigger()
        pm.report_antibot_trigger()
        result = pm.rotate_proxy()
        assert result == "http://user:pass@residential.proxy.net:8080"

    def test_residential_proxy_used_above_threshold(self):
        pm = _make_proxy_manager(
            datacenter_urls="http://proxy1.example.com:8080",
            residential_url="http://user:pass@residential.proxy.net:8080",
        )
        for _ in range(5):
            pm.report_antibot_trigger()
        result = pm.rotate_proxy()
        assert result == "http://user:pass@residential.proxy.net:8080"

    def test_falls_back_to_datacenter_when_no_residential_configured(self):
        """When threshold is reached but no residential proxy is set, use datacenter."""
        pm = _make_proxy_manager(datacenter_urls="http://proxy1.example.com:8080")
        for _ in range(5):
            pm.report_antibot_trigger()
        result = pm.rotate_proxy()
        assert result == "http://proxy1.example.com:8080"

    def test_trigger_counter_increments(self):
        pm = _make_proxy_manager()
        pm.report_antibot_trigger()
        pm.report_antibot_trigger()
        assert _state.antibot_triggers == 2

    def test_reset_triggers_clears_state(self):
        pm = _make_proxy_manager(
            datacenter_urls="http://proxy1.example.com:8080",
            residential_url="http://user:pass@residential.proxy.net:8080",
        )
        for _ in range(5):
            pm.report_antibot_trigger()
        pm.reset_triggers()
        assert _state.antibot_triggers == 0
        assert _state.residential_escalated is False
        # After reset, datacenter proxy is used again
        result = pm.rotate_proxy()
        assert result == "http://proxy1.example.com:8080"

    def test_has_proxies_is_true_with_only_residential(self):
        pm = _make_proxy_manager(
            residential_url="http://user:pass@residential.proxy.net:8080"
        )
        assert pm.has_proxies is True
