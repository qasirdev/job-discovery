# Learning: Step 13 - Observability Stack

## Learning Objectives
- Learn how to instrument an asynchronous FastAPI application using OpenTelemetry.
- Understand the concept of Request Correlation via ContextVars.

## Technical Details

### 1. OpenTelemetry and The Observability Agent
Our `ObservabilityAgent` encapsulates all standard OpenTelemetry instrumentation logic. By calling `obs_agent.instrument_fastapi_app(app)` in `main.py`, we automatically generate standard W3C Trace Contexts for every incoming HTTP request. This gives us visibility into route latencies, DB query times, and external API calls without polluting the business logic.

### 2. Request Correlation (X-Request-ID)
FastAPI operates asynchronously across many concurrent threads/coroutines. To trace logs effectively, `backend/logging_config.py` uses Python's `contextvars.ContextVar`.
When the middleware generates or extracts an `X-Request-ID`, it sets it in the `request_id_ctx`. Our custom `JSONFormatter` then automatically injects this `request_id` into every single `logger.info()` or `logger.error()` line.
This guarantees that if an error occurs deep within a database repository, we can easily query our centralized logging system for that exact Request ID and see the full journey of the request.
