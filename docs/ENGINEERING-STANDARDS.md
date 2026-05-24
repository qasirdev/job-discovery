# ENGINEERING STANDARDS

This document merges system architecture principles, production engineering constraints, and enforceable coding standards into a single authoritative reference for backend, frontend, and AI-driven systems.

---

# 1. Technology Stack Standards

## Frontend Stack

* Next.js 16
* React 19
* TypeScript
* Tailwind CSS
* MUI (Material UI)
* TanStack Query
* Zustand
* Zod

## Backend Stack

* Python 3.14 (strict)
* FastAPI
* uv (dependency management)
* Pydantic v2
* SQLAlchemy 2
* pgvector
* Redis
* LiteLLM
* OpenTelemetry
* Testing: pytest-asyncio (asyncio_mode="auto")

## Database Stack

* Supabase PostgreSQL
* pgvector enabled
* Row Level Security (RLS)
* Partitioning strategy required
* JSONB usage allowed with schema control
* WAL enabled for durability

---

# 2. Twelve-Factor App Compliance (Modern 2026 Interpretation)

All services MUST comply with the Twelve-Factor App principles:

1. **Codebase**: Single monorepo, multiple deploys.
2. **Dependencies**: Explicit (`uv`, `npm ci`). No implicit installs.
3. **Config**: Environment-based config only (`.env`, validated via Pydantic Settings).
4. **Backing Services**: Treat as attached resources (Postgres, Redis, LLM APIs).
5. **Build, Release, Run**: Strict separation via Docker multi-stage builds.
6. **Processes**: Stateless processes only.
7. **Port Binding**: Services expose ports directly (FastAPI: 8000).
8. **Concurrency**: Horizontal scaling via Uvicorn workers.
9. **Disposability**: Fast startup, graceful shutdown required.
10. **Dev/Prod Parity**: Docker parity across environments.
11. **Logs**: Structured JSON logs as event streams.
12. **Admin Processes**: One-off tasks (migrations, replays) via `/admin`.

---

# 3. Python Engineering Standards

* Python 3.14 strictly enforced
* Use modern typing (`X | Y`, `type` keyword)
* Strict `mypy` compliance (no exceptions)
* Dependency management: `uv`
* Security updates enforced via Dependabot (weekly)
* No unused dependencies allowed

---

# 4. FastAPI & API Design Standards

* Pydantic v2 required for all schemas
* Strict mode:

```python
model_config = {"extra": "forbid"}
```

* No raw HTTP status integers

  * Always use `fastapi.status`
* All dependencies MUST use `Depends()`

  * Auth
  * RBAC
  * DB sessions
* API must be explicit, no implicit request context usage

---

# 5. Code Quality Standards

* Linting: `ruff` (mandatory)
* Formatting: `ruff format`
* Type checking: `mypy --strict`
* No silent failures allowed
* All functions must be typed
* No dynamic typing for public interfaces

---

# 6. Agent Architecture Standards (LLM Systems)

All agents MUST follow this strict 6-file structure:

```
prompts/<agent-name>/
```

1. `AGENT.md` → Orchestration rules
2. `CONTRACT.md` → Input/output JSON schemas
3. `system.md` → Exact system prompt (XML format allowed)
4. `tools.md` → Tool definitions
5. `guardrails.md` → Safety + constraints
6. `CHANGELOG.md` → Version history

Rules:

* No agent logic outside this structure
* Contracts must be machine-validated
* Guardrails must be deterministic

---

# 7. Logging & Observability Standards

## Logging

* Structured JSON logging only (`logging_config.py`)

### Log Levels

* INFO → Normal workflow events
* WARNING → Recoverable issues
* ERROR → System failures requiring action

### Rules

* No PII in logs
* No high-cardinality fields (e.g., `job_id`, `user_email`) in metrics
* Logs must be machine-parseable

## Observability

* OpenTelemetry required for tracing
* Metrics must be safe for Prometheus

---

# 8. System Architecture Principles

* Stateless services only
* Horizontal scaling preferred
* All services must be containerized
* Backing services are external dependencies
* Use Redis for caching and ephemeral state
* Use pgvector for semantic search workloads

---

# 9. Security Standards

* No sensitive data in logs or metrics
* Strict schema validation on all inputs
* RLS enabled on all database tables
* Pydantic validation required at all API boundaries
* No direct DB exposure to frontend

---

# 10. Testing Standards

* pytest-asyncio required
* asyncio_mode="auto"
* Unit + integration tests mandatory
* No untested business logic allowed
* Mock external APIs (LLMs, Redis, DB) in unit tests

---

# 11. Deployment Standards

* Docker required for all environments
* Multi-stage builds mandatory
* CI/CD must include:

  * lint
  * typecheck
  * tests
  * security scan

---

# 12. Performance Standards

* Async-first backend design
* Avoid blocking I/O
* Use connection pooling for DB
* Cache expensive computations in Redis

---

# FINAL PRINCIPLE

This standard prioritizes:

* Consistency over flexibility
* Explicitness over convention
* Safety over convenience
* Scalability over local optimization
