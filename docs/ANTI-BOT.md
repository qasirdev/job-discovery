# Anti-Bot, Proxy, and Fingerprinting Disclaimer

This document defines the constraints and strategies for job board scraping, ensuring compliance and platform stability.

## Constraints

- **Respect robots.txt:** The platform must respect `robots.txt` constraints for all scraped domains.
- **No CAPTCHA Solving:** The platform must not implement or use any CAPTCHA solving or bypassing mechanisms.
- **No Authenticated Scraping:** The platform must not perform authenticated scraping of LinkedIn (or other platforms where it violates Terms of Service).

## Browser Fingerprinting Strategy

To ensure reliable discovery without triggering aggressive blocks, the scraper agents employ the following strategies:
- User-Agent Rotation
- Viewport Randomisation
- Context Isolation
- Proxy Abstraction
- Residential Proxy Support (implemented in MVP 2)

## Proxy Abstraction Layer

Introduced in MVP 2. Implemented in `backend/agents/proxy.py` via the `ProxyManager` class.

All Playwright-based scraper agents (LinkedIn, JobServe, and any future agents) use `ProxyManager` to obtain a proxy configuration before creating a browser context:

```python
proxy_manager = ProxyManager()
proxy_config = proxy_manager.get_playwright_proxy()  # Returns dict or None
context = await browser.new_context(proxy=proxy_config, ...)
```

### Proxy Types

| Type | Environment Variable | Description |
|---|---|---|
| Datacenter (default) | `PROXY_POOL_URLS` | Comma-separated list of proxy URLs. Rotated round-robin per scraping session. |
| Residential (anti-bot escalation) | `RESIDENTIAL_PROXY_URL` | Single residential proxy endpoint. Activated automatically when anti-bot triggers exceed the escalation threshold (default: 3 consecutive failures). |

### Configuration

Add the following to your `.env` file (values shown are examples):

```bash
# Datacenter proxy pool — comma-separated list
PROXY_POOL_URLS=http://user:pass@proxy1.example.com:8080,http://user:pass@proxy2.example.com:8080

# Residential proxy — single endpoint, authentication embedded in URL
RESIDENTIAL_PROXY_URL=http://username:password@residential.proxy.net:8080
```

If neither variable is set, scraper agents connect directly (no proxy). This is the default for MVP 1 / local development.

### Rotation Strategy

- **Datacenter proxies**: Round-robin across all configured proxy URLs using `itertools.cycle`.
- **Residential proxy**: Activated when `antibot_triggers >= RESIDENTIAL_ESCALATION_THRESHOLD` (3 by default). Call `proxy_manager.report_antibot_trigger(reason=...)` from scraper agents upon CAPTCHA detection, 429 responses, or DOM-stability anomalies.
- **Fallback**: If all proxies fail or the pool is exhausted, the agent falls back to direct connection and logs a warning.

### Proxy URL Format

Supports both plain and authenticated formats:

```
http://host:port
http://user:pass@host:port
socks5://user:pass@host:port
```

Residential proxy URLs may contain authentication credentials embedded directly in the URL — this is supported and handled by Playwright's proxy configuration.

### Logging

All proxy rotation events are logged via `get_logger('proxy')` as structured JSON:

```json
{"event": "proxy_rotated", "proxy_type": "datacenter", "reason": "round_robin"}
{"event": "antibot_trigger_reported", "reason": "captcha_detected", "total_triggers": 1, "threshold": 3}
{"event": "proxy_pool_exhausted", "fallback": "direct_connection"}
```

### Integration Example (Playwright)

```python
from backend.agents.proxy import ProxyManager

proxy_manager = ProxyManager()

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    proxy_config = proxy_manager.get_playwright_proxy()
    context = await browser.new_context(
        user_agent=user_agent,
        viewport=viewport,
        **({"proxy": proxy_config} if proxy_config else {}),
    )
    # ... scraping logic ...
    proxy_manager.reset_triggers()  # Reset on success
```

## Compliance Disclaimer & Terms of Service

This software is for personal intelligence and orchestration use. Users run scraping agents locally or within their own dedicated cloud environments. The developer of this platform is not responsible for any Terms of Service violations incurred by the user running the scraping workloads.
