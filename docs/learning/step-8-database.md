# Learning: Step 8 - Database & Migrations

## Learning Objectives
- Learn how to set up an async Postgres connection pool using `asyncpg`.
- Understand database migrations using `alembic` with async support.

## Technical Details
- **SQLAlchemy Async**: We use `create_async_engine` and `AsyncSession` to maintain non-blocking database queries, crucial for high-throughput FastAPI backends.
- **Alembic**: The migration framework manages database schema changes over time. We created an initial migration (`init`) that contains the `jobs` table creation SQL representation.
- **Supabase**: While not directly implemented yet, the connection string defaults to local Postgres but will cleanly accept a Supabase pooler connection string when pushed to production.
