# ENGINEERING STANDARDS

This document merges system architecture principles, production engineering constraints, and enforceable coding standards into a single authoritative reference for backend, frontend, and AI-driven systems.

---

# 1. Technology Stack Standards

## Frontend Stack

* **Next.js 16**: (App Router paradigm for server-side rendering and routing)
* **React 19**: (Server components support)
* **TypeScript (strict mode)**: (Ensures type safety across the application)
* **Tailwind CSS**: (Utility-first styling, primary layout tool)
* **MUI v6**: (Selective use for complex interactive components where Tailwind would be inefficient)
* **TanStack Query v5**: (Data fetching, caching, and state synchronization)
* **Zustand**: (Lightweight global state management)
* **Zod**: (Schema validation matching backend Pydantic models)

### UI Styling Guidelines
* **Tailwind CSS**: Use as the primary tool for layout, spacing, typography, and modern custom aesthetics (e.g., glassmorphism, gradients, micro-animations).
* **Material UI (MUI)**: Use selectively for complex interactive components (e.g., Snackbars, CircularProgress, Modals) where building from scratch with Tailwind would reinvent the wheel. Ensure MUI components are styled to seamlessly blend with the Tailwind design system.
## Backend Stack

* **Python 3.14** (strict)
* **FastAPI** (Async web framework)
* **uv** (Dependency management, not pip)
* **Pydantic v2** (Data validation and settings management)
* **SQLAlchemy 2** (mapped_column syntax for ORM)
* **pgvector** (Semantic search embeddings)
* **Redis** (Caching, rate-limiting, and ephemeral state)
* **LiteLLM** (LLM provider multiplexing)
* **OpenTelemetry** (Distributed tracing and metrics)
* **Testing**: pytest with pytest-asyncio (asyncio_mode=auto)
* **Logging rules**: no print() calls anywhere (enforced in CI via grep)

## Database Stack

* Supabase PostgreSQL
* pgvector enabled
* Row Level Security (RLS)
* Partitioning strategy required
* JSONB usage allowed with schema control
* WAL enabled for durability

---

# 2. Twelve-Factor App Compliance (Modern 2026 Interpretation)

All services MUST comply with the Twelve-Factor App principles. The compliance status for this platform is detailed below:

| Factor | Requirement | Implementation in this platform | MVP Introduced | Compliance Status |
|--------|-------------|---------------------------------|----------------|-------------------|
| **I. Codebase** | Single repo, no per-env branches | Monorepo tracked in Git; single codebase for all deploys | MVP 1 | Compliant |
| **II. Dependencies** | Explicit, no system-level deps | `uv` pyproject.toml + package-lock.json | MVP 1 | Compliant |
| **III. Config** | Config via environment variables | `.env`, Pydantic Settings; git-secrets scan in CI | MVP 1 | Compliant |
| **IV. Backing Services** | Treat as attached resources | PostgreSQL, Redis, Temporal via connection strings | MVP 1 | Compliant |
| **V. Build, Release, Run** | Strict separation | Docker multi-stage builds, GitHub Actions CI/CD | MVP 1 | Compliant |
| **VI. Processes** | Stateless processes | fake_db removed in MVP 2; no in-process session state | MVP 2 | Compliant |
| **VII. Port Binding** | Expose ports directly | FastAPI on 127.0.0.1:8000; Next.js on :3000; Nginx on :80 | MVP 1 | Compliant |
| **VIII. Concurrency** | Horizontal scaling | `uvicorn --workers 2`; Temporal worker as separate process | MVP 1 | Compliant |
| **IX. Disposability** | Fast startup, graceful shutdown | SIGTERM handling for uvicorn, Temporal, Playwright | MVP 3 | Compliant |
| **X. Dev/Prod Parity** | Docker parity | Docker Compose mirrors staging/production | MVP 1 | Compliant |
| **XI. Logs** | Structured JSON as event streams | `get_logger` to stdout; no `print()` calls (enforced by CI) | MVP 1 | Compliant |
| **XII. Admin Processes** | One-off tasks via admin scripts | `backend/admin/` scripts run in same Docker image | MVP 1 | Compliant |

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
