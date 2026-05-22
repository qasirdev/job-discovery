# Learning: Step 15 - Admin Tooling & Resilience

## Learning Objectives
- Learn how to handle async task failures using a Dead Letter Queue (DLQ).
- Understand how to build recovery scripts for autonomous agents.

## Technical Details

### 1. The Dead Letter Queue (DLQ) Pattern
In a distributed scraper architecture, HTTP requests will inevitably fail due to rate limits, DOM changes, or network timeouts. Instead of silently dropping these failures, the system catches the exception and routes the raw request payload into a `dlq_jobs` table (the Dead Letter Queue).

### 2. Admin Recovery (replay_dlq.py)
We built an administrative script `backend/admin/replay_dlq.py`. 
- **Idempotency**: It safely queries the DLQ for all items marked as `failed`, resolves the correct agent class dynamically using the registry, and attempts to re-run the scrape.
- **DIFA Fallback**: Just like the main application, if the PostgreSQL database is completely down, the DLQ script gracefully falls back to inspecting a local `dlq_fallback.json` file. This ensures that engineers can manually replay and debug failed payloads on their local machines even without an active connection to the production cluster.
