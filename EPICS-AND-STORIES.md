# Epics, Stories and Tasks — AI-Powered Job Discovery Platform

**Proposal:** 004-01-saas-job-search-proposal-v4.md (v1.2.0)
**Total Epics:** 16 | **Total Stories:** 70

---

## MVP 1 — Scraper Foundation & In-Memory Store

### EPIC 1 — Project Scaffold & Docker Setup

#### Story 1.1 — Monorepo init
- Create `job-discovery/` root with `AGENT.md`, `.env.example`, `.gitignore`.

#### Story 1.2 — Multi-stage Dockerfile
- Node:22-alpine FE build → python:3.14-slim runtime; exposes port 80.

#### Story 1.3 — Supervisor config
- `supervisord.conf` with migrate (priority 1) → nginx (10) → fastapi (10).

#### Story 1.4 — Nginx reverse proxy
- `/` → static export, `/api/v1/*` → FastAPI, `/health` passthrough.

#### Story 1.5 — Local Dev Orchestration
- `docker-compose.yml` for local dev orchestration with healthcheck.

#### Story 1.6 — Tasks directory
- Create `tasks/todo.md` and `tasks/lessons.md` at monorepo root; add `tasks/` to root `AGENT.md` index.

---

### EPIC 16 — Workflow Orchestration Infrastructure

#### Story 16.1 — Active Task Plan
- Create `tasks/todo.md` with Active Plan header, checkable steps, and Review section.

#### Story 16.2 — Lessons Log
- Create `tasks/lessons.md` with session date header, mistake pattern, root cause, and rules.

#### Story 16.3 — Root AGENT.md Update
- Add Workflow Rules table to the root `AGENT.md` (plan mode, task log, verify plan, etc.).

#### Story 16.4 — Execution Rules Update
- Update `docs/EXECUTION-RULES.md` with MUST/MUST NOT execution workflow rules.

#### Story 16.5 — Subagent Rules
- Update `backend/agents/AGENT.md` with Subagent Execution Rules (offload strategy, summarisation).

#### Story 16.6 — CI Enforcement Stub
- Add `check-workflow-docs` step to `ci.yml` failing if tracking docs are missing.

---

### EPIC 2 — Backend Core

#### Story 2.1 — FastAPI entrypoint
- `main.py` with `/api/v1/` prefix; agent auto-discovery imports.

#### Story 2.2 — Pydantic Settings
- `settings.py`; all env vars typed and validated at startup.

#### Story 2.3 — Structured JSON logger
- `logging_config.py`; shared `get_logger(name)` imported by all modules.

#### Story 2.4 — Domain models
- `models.py` with `Job` and `ScrapeResult` Pydantic schemas.

#### Story 2.5 — Keyword filter
- `filters.py`; title/description substring matching.

#### Story 2.6 — In-memory fake DB
- Dict-backed store in `main.py`; explicit MVP 1 exception, replaced by Supabase in MVP 2.

---

### EPIC 3 — Extensible Scraper Registry

#### Story 3.1 — BaseScrapeAgent ABC
- `agents/base.py`; defines `source_id`, `display_name`, `run()` interface.

#### Story 3.2 — Registry module
- `agents/registry.py`; `@register` decorator, `get_all_agents()`, `get_agent(source_id)`.

#### Story 3.3 — LinkedIn agent
- Playwright scraper; `source_id="linkedin"`; anti-bot randomisation, deduplication.

#### Story 3.4 — JobServe agent
- Playwright scraper; `source_id="jobserve"`; pagination randomisation, data normalisation.

#### Story 3.5 — Scrape router
- `routers/scrape.py`; calls `get_all_agents()` — no hardcoded source names.

---

### EPIC 4 — Next.js Frontend Dashboard

#### Story 4.1 — Next.js 16 scaffold
- `output: "export"`, Tailwind 4, MUI 7, TanStack Query, Zustand, Zod.

#### Story 4.2 — JobCard component
- Displays title, company, source badge, relevance score.

#### Story 4.3 — FilterBar component
- Source and keyword filters; client-side.

#### Story 4.4 — ScrapeButton component
- Triggers `POST /api/v1/scrape`; shows in-progress state.

---

### EPIC 5 — Versioned API & CI Skeleton

#### Story 5.1 — Jobs router
- `GET /api/v1/jobs` with cursor-based pagination; `GET /api/v1/jobs/{id}`.

#### Story 5.2 — OpenAPI spec
- All routes typed with Pydantic request/response models; auto-generated docs.

#### Story 5.3 — Admin process scripts
- `backend/admin/`: `seed_keywords.py`, `clear_db.py`, stubs for DLQ and evals.

#### Story 5.4 — GitHub Actions CI skeleton
- Ruff lint, mypy, ESLint, tsc, pytest, Vitest, Docker build.

---

## MVP 1.1 — Advanced Prompt Engineering Infrastructure

### EPIC 6 — Prompts Directory & Versioning Framework

#### Story 6.1 — Prompts root scaffold
- `prompts/AGENT.md` with XML prompt structure standard and reasoning effort matrix.

#### Story 6.2 — LinkedIn agent prompts
- `CONTRACT.md`, `CHANGELOG.md`, `system.md`, `skills.md`, `tools.md`, `guardrails.md`.

#### Story 6.3 — JobServe agent prompts
- Same six-file structure; `source_id="jobserve"`-specific selectors and guardrails.

#### Story 6.4 — CONTRACT.md template
- Model pin, reasoning effort, max tokens, temperature, permitted tools, token budget, eval set ref.

#### Story 6.5 — Prompt-based relevance filtering
- Heuristic pre-filtering before pgvector ranking; integrated into scraper agents.

---

### EPIC 7 — Eval Framework (DeepEval + Ragas)

#### Story 7.1 — Eval runner script
- `backend/admin/run_evals.py`; per-agent eval set execution.

#### Story 7.2 — DeepEval integration
- Faithfulness and relevance metrics wired to CI; fail threshold defined in CONTRACT.md.

#### Story 7.3 — CI prompt regression step
- GitHub Actions runs evals on every merge; blocks deploy if threshold drops.

---

## MVP 2 — AI Ranking, Persistence & Cloud Infrastructure

### EPIC 8 — Supabase PostgreSQL & Alembic

#### Story 8.1 — Replace fake DB
- Supabase PostgreSQL with pgvector; all models migrated from in-memory dict.

#### Story 8.2 — asyncpg connection pool
- `db.py`; `pool_size=10`, `max_overflow=20`, `pool_timeout=30`, `pool_pre_ping=True`.

#### Story 8.3 — Alembic migrations
- `backend/migrations/`; runs via Supervisor priority 1 before uvicorn starts.

#### Story 8.4 — Full domain models
- `Job`, `Recruiter`, `Application`, `CV`, `CoverLetter`, `ScrapeRun`, `InterviewPrep`.

---

### EPIC 9 — AI Ranking & RAG Agents

#### Story 9.1 — Ranking agent
- 8-step pipeline: embeddings → cosine sim → cross-encoder rerank → sentiment → recruiter quality → salary normalisation → skill extraction → seniority validation.

#### Story 9.2 — RAG agent
- Contextual retrieval from CV, applications, recruiter messages, saved jobs, preferences, skill graph.

#### Story 9.3 — Cover letter agent
- Structured playbook; ATS keyword match ≥ 60% enforced before delivery.

#### Story 9.4 — Question answer agent
- RAG-grounded Q&A on specific job listings; `POST /api/v1/question-answer/{job_id}`.

#### Story 9.5 — Ragas eval in CI
- Retrieval precision and context recall; blocks deploy if precision < 0.80.

---

### EPIC 10 — Security & Orchestration Agents

#### Story 10.1 — Security agent
- Prompt injection detection, OWASP middleware, schema validation, RBAC enforcement, HTML sanitisation.

#### Story 10.2 — Workflow orchestrator
- Temporal workflows; retry with exponential backoff and jitter; DLQ; idempotency via SHA-256 job ID.

#### Story 10.3 — Circuit breakers
- Per agent; opens after 3 consecutive failures; base 1s backoff, max 60s.

#### Story 10.4 — Admin DLQ routes
- `GET /api/v1/admin/dlq`, retry and discard endpoints; `replay_dlq.py` admin script.

---

### EPIC 11 — Terraform & Multi-Cloud Deployment

#### Story 11.1 — Azure Container Apps Terraform
- `infrastructure/terraform/azure/`; `main.tf`, `variables.tf`, `outputs.tf`.

#### Story 11.2 — AWS ECS Fargate Terraform
- `infrastructure/terraform/aws/`; multi-cloud portability via provider abstraction.

#### Story 11.3 — Terraform CI steps
- Validate + plan on every PR; apply on merge to main.

#### Story 11.4 — Docker image signing
- GitHub Actions; tagged with Git commit SHA; pushed to registry on merge.

---

### EPIC 12 — MVP 2 Prompts for AI Agents

#### Story 12.1 — Ranking agent prompts
- `system.md`, `scoring.md`, `reranking.md`, `filtering.md`, CONTRACT.md pinned to medium effort.

#### Story 12.2 — RAG agent prompts
- `system.md`, `retrieval.md`, `embeddings.md`, `personalization.md`; high reasoning effort.

#### Story 12.3 — Cover letter agent prompts
- `system.md`, `tone.md`, `generation.md`, `templates.md`; medium effort.

#### Story 12.4 — Question answer & security agent prompts
- Respective `system.md` and `tools.md`; high reasoning effort.

#### Story 12.5 — Orchestrator prompts
- `system.md`; xhigh reasoning effort for long-horizon coordination.

---

## MVP 3 — Full Twelve-Factor Compliance, Observability & Auth

### EPIC 13 — Observability Stack

#### Story 13.1 — OpenTelemetry integration
- Distributed tracing and metrics across all agents and routers.

#### Story 13.2 — Grafana dashboards
- Latency p50/p95, token usage, hallucination rate, retrieval precision, reranker confidence.

#### Story 13.3 — Prometheus + Loki
- Metrics scraping; log aggregation from stdout structured JSON streams.

#### Story 13.4 — Sentry integration
- Error tracking and alerting; Microsoft Clarity for frontend session replay.

#### Story 13.5 — Observability agent
- `agents/observability/`; traces, schema conformance rate ≥ 99%, hallucination alert if > 1%.

---

### EPIC 14 — Auth, RBAC & Row-Level Security

#### Story 14.1 — Supabase Auth + JWT
- JWT validation middleware in FastAPI; RBAC enforced at route level via JWT claims.

#### Story 14.2 — Row-Level Security
- Supabase RLS policies; users read and write only their own rows.

#### Story 14.3 — OWASP Top 10 hardening
- Trivy + Bandit scans in CI; SSRF allowlist; encrypted secrets via Azure Key Vault.

#### Story 14.4 — GDPR compliance
- Export (PDF/JSON/CSV), deletion (PostgreSQL + pgvector + Redis + object storage), audit logging.

---

### EPIC 15 — Twelve-Factor Completion & Admin Tooling

#### Story 15.1 — Twelve-Factor audit
- Verify all 12 factors against production config; document any gaps and close them.

#### Story 15.2 — Graceful shutdown
- SIGTERM handlers in all long-running processes; uvicorn drain, Temporal checkpoint, Playwright session close.

#### Story 15.3 — Structured admin tooling
- `replay_dlq.py`, `run_evals.py` fully wired; schedule pause/resume routes.

#### Story 15.4 — Disaster recovery validation
- Backup restore drill; PostgreSQL WAL + Redis AOF; RTO ≤ 1 hr, RPO ≤ 15 min.
