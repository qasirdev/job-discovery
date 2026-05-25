"""
backend/agents/proxy.py

Proxy Abstraction Layer — JD-104.

ProxyManager provides rotating proxy support for all Playwright-based scraper agents.
Implements the strategy defined in docs/ANTI-BOT.md:
  - Datacenter proxy pool: round-robin rotation via PROXY_POOL_URLS (comma-separated)
  - Residential proxy: single endpoint via RESIDENTIAL_PROXY_URL — activated only when
    anti-bot detection is triggered (CAPTCHA frequency exceeds threshold)
  - No proxy when neither env var is set (MVP 1 / local dev compatibility)

Usage in scraper agents:
    proxy_manager = ProxyManager()
    proxy_config = proxy_manager.get_playwright_proxy()   # Returns dict or None
    context = await browser.new_context(proxy=proxy_config, ...)

After a CAPTCHA or 429 event, call:
    proxy_manager.report_antibot_trigger()
to escalate to residential proxy automatically.

Reference: docs/ANTI-BOT.md, proposal-v4-structure.md MVP 2 scope, JD-104.
"""

from __future__ import annotations

import itertools
import threading
from dataclasses import dataclass, field
from typing import Optional

from ..logging_config import get_logger
from ..settings import get_settings

logger = get_logger("proxy")


@dataclass
class _ProxyState:
    """Mutable shared proxy rotation state (thread-safe via lock)."""
    antibot_triggers: int = 0
    residential_escalated: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)


# Module-level singleton state — shared across all ProxyManager instances in the process
_state = _ProxyState()


class ProxyManager:
    """
    Manages rotating proxy selection for Playwright scraper agents.

    Rotation strategy:
    - Datacenter proxies (PROXY_POOL_URLS) → round-robin
    - Residential proxy (RESIDENTIAL_PROXY_URL) → engaged when antibot_triggers
      reaches RESIDENTIAL_ESCALATION_THRESHOLD (default 3)

    Proxy URL format (all types):
        protocol://[user:pass@]host:port
        e.g. http://user:pass@proxy.example.com:8080

    The residential proxy URL supports authentication embedded in the URL:
        http://username:password@residential.proxy.net:8080
    """

    # Number of anti-bot events before escalating to residential proxy
    RESIDENTIAL_ESCALATION_THRESHOLD: int = 3

    def __init__(self) -> None:
        settings = get_settings()

        # Parse datacenter proxy pool
        pool_raw: str | None = settings.proxy_pool_urls
        if pool_raw:
            urls = [u.strip() for u in pool_raw.split(",") if u.strip()]
            self._datacenter_pool: list[str] = urls
        else:
            self._datacenter_pool = []

        # Residential proxy endpoint (single URL)
        self._residential_url: str | None = settings.residential_proxy_url

        # Round-robin iterator (cycle is infinite — always restarts after last)
        self._cycle = itertools.cycle(self._datacenter_pool) if self._datacenter_pool else None

        logger.info(
            "proxy_manager_initialized",
            extra={
                "datacenter_pool_size": len(self._datacenter_pool),
                "residential_configured": self._residential_url is not None,
            },
        )

    # ── Public API ──────────────────────────────────────────────────────────

    def rotate_proxy(self) -> Optional[str]:
        """
        Return the next proxy URL to use for a scraping session.

        Returns None if no proxy is configured (direct connection).

        Residential proxy is returned when anti-bot trigger count has reached
        the escalation threshold. If residential proxy is not configured,
        falls back to next datacenter proxy.
        """
        with _state._lock:
            use_residential = (
                _state.antibot_triggers >= self.RESIDENTIAL_ESCALATION_THRESHOLD
                and self._residential_url is not None
            )

        if use_residential:
            proxy_url = self._residential_url
            logger.info(
                "proxy_rotated",
                extra={
                    "proxy_type": "residential",
                    "reason": "antibot_threshold_reached",
                    "trigger_count": _state.antibot_triggers,
                },
            )
            return proxy_url

        if not self._cycle:
            # No proxies configured — direct connection
            return None

        try:
            proxy_url = next(self._cycle)
            logger.info(
                "proxy_rotated",
                extra={"proxy_type": "datacenter", "reason": "round_robin"},
            )
            return proxy_url
        except StopIteration:
            # Exhausted pool (shouldn't happen with itertools.cycle, but defensive)
            logger.warning(
                "proxy_pool_exhausted",
                extra={"fallback": "direct_connection"},
            )
            return None

    def get_playwright_proxy(self) -> Optional[dict]:
        """
        Return a Playwright browser context proxy config dict, or None.

        Usage:
            context = await browser.new_context(proxy=proxy_manager.get_playwright_proxy())

        Playwright proxy format:
            {"server": "http://host:port", "username": "...", "password": "..."}
        or simply:
            {"server": "http://user:pass@host:port"}  when creds are embedded in URL
        """
        proxy_url = self.rotate_proxy()
        if proxy_url is None:
            return None

        # Playwright accepts embedded credentials in the server URL
        return {"server": proxy_url}

    def report_antibot_trigger(self, reason: str = "captcha_detected") -> None:
        """
        Increment the anti-bot trigger counter.

        Call this from scraper agents when a CAPTCHA, 429, or DOM-stability
        anomaly is detected. Once the counter reaches RESIDENTIAL_ESCALATION_THRESHOLD,
        subsequent proxy rotations escalate to residential proxy automatically.
        """
        with _state._lock:
            _state.antibot_triggers += 1
            triggered = _state.antibot_triggers

        logger.warning(
            "antibot_trigger_reported",
            extra={
                "reason": reason,
                "total_triggers": triggered,
                "threshold": self.RESIDENTIAL_ESCALATION_THRESHOLD,
                "residential_will_escalate": triggered >= self.RESIDENTIAL_ESCALATION_THRESHOLD,
            },
        )

    def reset_triggers(self) -> None:
        """Reset anti-bot trigger counter (e.g. after a successful scrape session)."""
        with _state._lock:
            _state.antibot_triggers = 0
            _state.residential_escalated = False
        logger.info("proxy_trigger_counter_reset")

    @property
    def has_proxies(self) -> bool:
        """True if any proxy (datacenter or residential) is configured."""
        return bool(self._datacenter_pool or self._residential_url)
