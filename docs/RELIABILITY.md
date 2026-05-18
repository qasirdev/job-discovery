# RELIABILITY ENGINEERING

To ensure agentic stability against erratic external systems (web scrapers, LLM endpoints), we employ the following patterns:

## 1. Failure Modes & Defenses
- **Rate Limits (429s)**: Handled via Exponential Backoff with Jitter.
- **Broken Selectors (Scraping)**: Handled via AI vision fallback or graceful degradation (skipping the field).
- **LLM Hallucination**: Bounded by Pydantic schema validation and retry-on-parse-failure loops.

## 2. The DIFA Framework
*Detect, Isolate, Fallback, Alert*
- **Detect**: Catch the exact exception (e.g., Playwright timeout).
- **Isolate**: Prevent the failure of one job scrape from crashing the batch.
- **Fallback**: Attempt an alternative retrieval method or use default values.
- **Alert**: Emit structured error logs for the Observability Agent.

## 3. Resilience Patterns
- **Circuit Breakers**: If a specific job board returns >50% errors in a 5-minute window, trip the circuit breaker and pause scraping for that board.
- **Dead Letter Queues (DLQ)**: Jobs that fail AI relevance scoring due to parsing errors must be saved to a DLQ for offline analysis and replay.
- **Idempotency**: All ingestion endpoints and scraper pipelines must be safely repeatable without creating duplicate records.
