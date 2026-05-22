# Learning: Step 8 - Database & Migrations

## Learning Objectives
- Learn how to set up an async Postgres connection pool using `asyncpg`.
- Understand database migrations using `alembic` with async support.

## Technical Details
- **SQLAlchemy Async**: We use `create_async_engine` and `AsyncSession` to maintain non-blocking database queries, crucial for high-throughput FastAPI backends.
- **Alembic**: The migration framework manages database schema changes over time. We created an initial migration (`init`) that contains the `jobs` table creation SQL representation.
- **Keyset-Based Pagination**: Unlike traditional `OFFSET`/`LIMIT` pagination which suffers from performance degradation on large tables, we implemented Keyset pagination using base64-encoded cursors (e.g. `scraped_at|id`) in `backend/repositories/job.py`. This ensures fast, stable paginated queries even as the job table scales to millions of rows.
- **Resilient UPSERTs (ON CONFLICT)**: Scrapers often encounter the same jobs multiple times. To avoid primary key constraint violations and duplicate data, `backend/repositories/job.py` uses PostgreSQL's `ON CONFLICT DO UPDATE` to gracefully overwrite changing fields (like `description`) while keeping the `id` stable.
- **Graceful Fallbacks (DIFA)**: The system implements the *Design In Fallback Availability (DIFA)* pattern. If the Supabase Postgres database drops connection, the `JobRepository` automatically downgrades to storing and querying against an in-memory `fake_db`, preventing catastrophic application crashes and allowing scrapers to finish their workloads.
- **Automated Container Migrations**: Our `supervisord.conf` is configured to run `uv run alembic upgrade head` as a high-priority startup command (Priority 1) before the FastAPI web workers start (Priority 10). This ensures the DB schema is always perfectly in sync with the deployment image.
