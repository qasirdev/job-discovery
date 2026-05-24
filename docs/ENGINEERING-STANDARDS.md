# ENGINEERING STANDARDS

## Technology Stacks
- **Frontend Stack**: Next.js 16, React 19, TypeScript, Tailwind, MUI, TanStack Query, Zustand, Zod.
- **Backend Stack**: Python 3.14, FastAPI, uv, Pydantic v2, SQLAlchemy 2, pgvector, Redis, LiteLLM, OpenTelemetry. Testing config includes `pytest-asyncio` with `asyncio_mode="auto"`.
- **Database Stack**: Supabase PostgreSQL, pgvector, RLS, partitioning, JSONB, WAL.

## Twelve-Factor Compliance
This platform strictly adheres to the Twelve-Factor App methodology (2026 modern interpretation).

1. **Codebase**: One codebase tracked in revision control (monorepo), many deploys.
2. **Dependencies**: Explicitly declare and isolate dependencies (using `uv` for Python, `npm ci` for Node).
3. **Config**: Store config in the environment (`.env`, validated via Pydantic Settings).
4. **Backing Services**: Treat backing services (PostgreSQL, Redis, LLM APIs) as attached resources.
5. **Build, Release, Run**: Strictly separate build and run stages (handled via Multi-stage Docker).
6. **Processes**: Execute the app as one or more stateless processes (Nginx + Uvicorn).
7. **Port Binding**: Export services via port binding (FastAPI on 8000, Nginx proxying to 80).
8. **Concurrency**: Scale out via the process model (Uvicorn workers).
9. **Disposability**: Maximize robustness with fast startup and graceful shutdown.
10. **Dev/Prod Parity**: Keep development, staging, and production as similar as possible (Docker everywhere).
11. **Logs**: Treat logs as event streams (Structured JSON logging via `logging_config.py`).
12. **Admin Processes**: Run admin/management tasks as one-off processes (e.g., Alembic migrations, DLQ replays in `backend/admin/`).

13. **Testing**: Python testing uses `pytest-asyncio` with `asyncio_mode="auto"`.
