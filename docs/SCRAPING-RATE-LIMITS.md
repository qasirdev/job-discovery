# Outbound Scraping Rate Limiting Strategy

**MVP:** 2  
**Reference:** `proposal-v4-structure.md` § SCRAPING-RATE-LIMITS, `docs/ANTI-BOT.md`, `docs/RELIABILITY.md`

This document defines the complete outbound scraping rate limiting strategy for all Playwright-based scraper agents (LinkedIn, JobServe, and any future registered agents).

---

## Per-Domain Concurrency Controls

Each target job board domain is subject to a **hard concurrency limit** — the maximum number of simultaneous Playwright page contexts open for that domain at any time.

| Domain | Max Concurrent Sessions | Notes |
|---|---|---|
| `linkedin.com` | 1 | Public job search only. No authenticated scraping. |
| `jobserve.com` | 1 | Public job search only. |
| Any future domain | 1 (default) | Override per agent in `AGENT.md` |

The global scrape concurrency gate is enforced at the API layer:

- **MVP 1**: `asyncio.Lock` in `backend/routers/v1/scrape.py` — in-process, single-container only.
- **MVP 2+**: Redis distributed lock `scrape:global` (timeout: 3600s) — safe across multiple uvicorn workers and Temporal workers.

```python
# MVP 1 — asyncio.Lock (single-process gate)
_scrape_lock = asyncio.Lock()
if _scrape_lock.locked():
    raise HTTPException(status_code=429, detail="Scrape already in progress")
async with _scrape_lock:
    ...

# MVP 2+ — Redis distributed lock
lock = redis.lock("scrape:global", timeout=3600)
if not await lock.acquire(blocking=False):
    raise HTTPException(status_code=429, detail="Scrape already in progress")
```

---

## Request Pacing with Randomised Delay

All scraper agents inject randomised delays between page interactions to simulate human browsing cadence and avoid triggering velocity-based bot detection.

| Action | Delay Range |
|---|---|
| After page navigation (`goto`) | 2000–4000 ms (random uniform) |
| Between card extractions | 0–500 ms (random uniform) |
| After browser context creation | 500–1500 ms (random uniform) |

Implementation example (both agents):

```python
import random
await page.wait_for_timeout(random.uniform(2000, 4000))
```

Randomisation prevents predictable timing fingerprints that bot-detection systems detect.

---

## Retry Policy with Exponential Backoff and Jitter

All transient scraping failures (network timeouts, 5xx responses, Playwright navigation errors) trigger a retry with exponential backoff.

| Parameter | Value |
|---|---|
| Base delay | 1 second |
| Maximum delay | 60 seconds |
| Multiplier | 2× per attempt |
| Jitter | ±25% of computed delay (uniform random) |
| Max attempts | 3 |

Formula:

```
delay = min(base * (2 ** attempt) + jitter, max_delay)
jitter = random.uniform(-0.25 * base_delay, 0.25 * base_delay)
```

This is aligned with the `docs/RELIABILITY.md` circuit breaker configuration.

---

## Failure Threshold / Circuit Breaker

**Rule**: A domain-level circuit breaker opens after **3 consecutive failures**.

When the circuit opens:
1. No further scrape requests are sent to that domain for the remainder of the current Temporal workflow activity.
2. The failure is logged as a structured event: `{"event": "circuit_breaker_open", "domain": "...", "trigger_count": 3}`.
3. The agent falls back to the DIFA framework: returns an empty result with `errors` populated, rather than raising an unhandled exception.

Circuit breaker states:

| State | Condition | Behaviour |
|---|---|---|
| Closed (healthy) | `consecutive_failures < 3` | Normal scraping proceeds |
| Open (tripped) | `consecutive_failures >= 3` | Reject all requests immediately; log and return empty result |
| Half-open (recovery) | Next Temporal retry triggers a single probe | If probe succeeds, reset to closed |

---

## Session Rotation

Browser contexts and sessions are rotated between scraping runs to reset fingerprint heuristics:

- **User-Agent rotation**: Selected randomly from a curated pool of realistic Chrome/Firefox user-agent strings per browser context creation.
- **Viewport randomisation**: Width randomised between 1280–1920px, height between 720–1080px.
- **Context isolation**: Each scraping run creates a new Playwright browser context (no shared cookies, storage, or sessions between runs).
- **Proxy rotation**: Delegated to `ProxyManager` in `backend/agents/proxy.py` — see `docs/ANTI-BOT.md`.

---

## Adaptive Throttling

The scraper agents implement adaptive throttling: dynamically adjusting request pace based on real-time signals from the target site.

### Throttling Triggers

| Signal | Detection | Response |
|---|---|---|
| **CAPTCHA frequency** | Playwright detects CAPTCHA elements (e.g., `iframe[src*="captcha"]`, `div.g-recaptcha`) | Call `proxy_manager.report_antibot_trigger(reason="captcha_detected")` → escalate to residential proxy after threshold |
| **429 Too Many Requests** | HTTP response status = 429 | Pause for `Retry-After` header value (default: 60s); increment antibot trigger counter |
| **DOM stability anomaly** | Layout change rate exceeds expected pattern (frequent element reflows within 500ms) | Increase inter-request delay by 2× for remainder of session |
| **Latency spike** | Navigation timeout exceeds 10s | Abort current page; retry with exponential backoff |

### Escalation to Residential Proxy

When `antibot_triggers >= 3` (configurable via `RESIDENTIAL_ESCALATION_THRESHOLD`), `ProxyManager.get_playwright_proxy()` automatically returns the residential proxy endpoint instead of the datacenter pool. This is transparent to the scraper agents — they always call `proxy_manager.get_playwright_proxy()` and let `ProxyManager` decide.

```python
# In scraper agents — no conditional logic needed
proxy_config = proxy_manager.get_playwright_proxy()  # Returns residential if threshold reached
context = await browser.new_context(proxy=proxy_config, ...)
```

---

## Queue Management via Temporal

Temporal manages all scraping queues with strict operational guarantees (MVP 2+):

### Concurrency Caps

| Queue Type | Max Active Workers |
|---|---|
| `scrape-queue` (LinkedIn + JobServe combined) | 1 global concurrent session |
| `rank-queue` (AI ranking after scrape completes) | 3 parallel ranking tasks |

### Retry Ceilings

| Failure Type | Max Retries | Backoff |
|---|---|---|
| Playwright navigation timeout | 3 | Exponential (base 1s, max 60s, jitter) |
| Proxy connection failure | 2 | Fixed 5s |
| Database upsert failure | 5 | Exponential (base 0.5s, max 30s) |

Maximum total retries per workflow activity: **3** (scraping) / **5** (DB writes).

### DLQ Routing

Failed scrape activities that exhaust all retries are routed to the **dead-letter queue (DLQ)**:
- DLQ item is written to `backend/dlq_fallback.json` (MVP 1) or a dedicated PostgreSQL table (MVP 2+).
- DLQ items are surfaced in the admin panel at `GET /api/v1/admin/dlq`.
- Admin can replay via `POST /api/v1/admin/dlq/{id}/retry` or discard via `POST /api/v1/admin/dlq/{id}/discard`.

### Priority Scheduling

| Trigger Type | Priority |
|---|---|
| User-initiated on-demand (`POST /api/v1/scrape`) | High — runs immediately |
| Scheduled background sweep (Temporal cron) | Normal — queued after high-priority jobs |

On-demand scrapes are signalled to the Temporal worker with a higher task queue priority. Background cron sweeps run on the default priority queue.

---

## Logging

All rate limiting and throttling events are logged via `get_logger('proxy')` and `get_logger('scraper')` as structured JSON to stdout (Loki-compatible):

```json
{"event": "proxy_rotated", "proxy_type": "datacenter", "reason": "round_robin"}
{"event": "antibot_trigger_reported", "reason": "captcha_detected", "total_triggers": 1, "threshold": 3}
{"event": "circuit_breaker_open", "domain": "linkedin.com", "trigger_count": 3}
{"event": "scrape_throttled", "reason": "dom_stability_anomaly", "delay_multiplier": 2}
{"event": "proxy_pool_exhausted", "fallback": "direct_connection"}
```
