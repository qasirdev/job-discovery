# Outbound Scraping Rate Limiting Strategy

To ensure platform reliability and avoid IP bans, strict rate limiting is applied to all outbound scraping tasks.

## Concurrency and Pacing
- **Per-domain concurrency controls**: Hard limits on parallel requests per target job board.
- **Request pacing**: Enforced randomised delays between sequential requests to simulate human pacing.
- **Session rotation**: Periodic rotation of browser contexts and sessions to reset fingerprint heuristics.

## Resilience and Recovery
- **Retry policy**: Exponential backoff with jitter on transient failures (e.g., timeouts, 5xx errors).
- **Failure threshold / circuit breaker**: Automatically halts scraping for a specific domain after consecutive failures, preventing further blacklisting.
- **Adaptive throttling**: Dynamically slows down or pauses requests based on specific signals:
  - CAPTCHA frequency spikes
  - 429 Too Many Requests responses
  - DOM stability issues (frequent layout changes detected)
  - Latency spikes on target servers

## Queue Management (Temporal)
Temporal manages the scraping queues with strict guarantees:
- **Concurrency caps**: Limits total active Playwright workers.
- **Retry ceilings**: Prevents infinite loops on permanently blocked endpoints.
- **DLQ routing**: Dead-Letter Queue for failed scrapes requiring manual admin review.
- **Priority scheduling**: Ensures user-initiated on-demand scrapes take precedence over background sweeps.
