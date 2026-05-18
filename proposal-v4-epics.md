# AI-Powered Job Discovery Platform — Epics & Tasks

**Proposal:** 004-01-saas-job-search-proposal-v4.md (v1.2.0)
**Total Epics:** 15 | **Total Tasks:** 70

---

## MVP 1 — Scraper Foundation & In-Memory Store

### E1 — Project Scaffold & Docker Setup

- **1.1** `Monorepo init` — create `job-discovery/` root with `AGENT.md`, `.env.example`, `.gitignore`
- **1.2** `Multi-stage Dockerfile` — node:22-alpine FE build → python:3.14-slim runtime; exposes port 80
- **1.3** `Supervisor config` — `supervisord.conf` with migrate (priority 1) → nginx (10) → fastapi (10)
- **1.4** `Nginx reverse proxy` — `/` → static export, `/api/v1/*` → FastAPI, `/health` passthrough
- **1.5** `docker-compose.yml` — local dev orchestration with healthcheck
- **1.6** `docs/tasks/ directory` — create `docs/tasks/todo.md` and `docs/tasks/lessons.md` at monorepo root; add `tasks/` to root `AGENT.md` index

---

### E2 — Backend Core

- **2.1** `FastAPI entrypoint` — `main.py` with `/api/v1/` prefix; agent auto-discovery imports
- **2.2** `Pydantic Settings` — `settings.py`; all env vars typed and validated at startup
- **2.3** `Structured JSON logger` — `logging_config.py`; shared `get_logger(name)` imported by all modules
- **2.4** `Domain models` — `models.py` with `Job` and `ScrapeResult` Pydantic schemas
- **2.5** `Keyword filter` — `filters.py`; title/description substring matching
- **2.6** `In-memory fake DB` — dict-backed store in `main.py`; explicit MVP 1 exception, replaced by Supabase in MVP 2

---

### E3 — Extensible Scraper Registry

- **3.1** `BaseScrapeAgent ABC` — `agents/base.py`; defines `source_id`, `display_name`, `run()` interface
- **3.2** `Registry module` — `agents/registry.py`; `@register` decorator, `get_all_agents()`, `get_agent(source_id)`
- **3.3** `LinkedIn agent` — Playwright scraper; `source_id="linkedin"`; anti-bot randomisation, deduplication
- **3.4** `JobServe agent` — Playwright scraper; `source_id="jobserve"`; pagination randomisation, data normalisation
- **3.5** `Scrape router` — `routers/scrape.py`; calls `get_all_agents()` — no hardcoded source names

---

### E4 — Next.js Frontend Dashboard

- **4.1** `Next.js 16 scaffold` — `output: "export"`, Tailwind 4, MUI 7, TanStack Query, Zustand, Zod
- **4.2** `JobCard component` — displays title, company, source badge, relevance score
- **4.3** `FilterBar component` — source and keyword filters; client-side
- **4.4** `ScrapeButton component` — triggers `POST /api/v1/scrape`; shows in-progress state

---

### E5 — Versioned API & CI Skeleton

- **5.1** `Jobs router` — `GET /api/v1/jobs` with cursor-based pagination; `GET /api/v1/jobs/{id}`
- **5.2** `OpenAPI spec` — all routes typed with Pydantic request/response models; auto-generated docs
- **5.3** `Admin process scripts` — `backend/admin/`: `seed_keywords.py`, `clear_db.py`, stubs for DLQ and evals
- **5.4** `GitHub Actions CI skeleton` — Ruff lint, mypy, ESLint, tsc, pytest, Vitest, Docker build

---

### E16 — Workflow Orchestration Infrastructure

- **16.1** `docs/tasks/todo.md` — create file; structure: Active Plan header, checkable steps, Review section appended on completion
- **16.2** `docs/tasks/lessons.md` — create file; structure: session date header, mistake pattern, root cause, rule to prevent recurrence
- **16.3** `Root AGENT.md update` — add Workflow Rules table (plan mode, task log, verify plan, subagents, lessons review, correction loop, done gate, elegance check, bug reports); add `docs/tasks/todo.md` and `docs/tasks/lessons.md` to the Where to look index
- **16.4** `docs/EXECUTION-RULES.md update` — add Workflow Execution Rules section: MUST list (plan mode, task log, check-in, lessons review, correction capture, incremental done marking, verification evidence, elegance pause, autonomous bug fix) and MUST NOT list (implement before confirmation, mark done without evidence, hacky fixes, out-of-scope file edits, repeat mistakes)
- **16.5** `backend/agents/AGENT.md update` — add Subagent Execution Rules section: one task per subagent, offload strategy (research/exploration/parallel analysis/eval runs), context window reservation, result summarisation protocol, escalation on subagent failure
- **16.6** `CI enforcement stub` — add `check-workflow-docs` step to `ci.yml`; fails if `docs/tasks/todo.md` or `docs/tasks/lessons.md` is missing from the repository

---

## MVP 1.1 — Advanced Prompt Engineering Infrastructure

### E6 — Prompts Directory & Versioning Framework

- **6.1** `prompts/ root scaffold` — `prompts/AGENT.md` with XML prompt structure standard and reasoning effort matrix
- **6.2** `LinkedIn agent prompts` — `CONTRACT.md`, `CHANGELOG.md`, `system.md`, `skills.md`, `tools.md`, `guardrails.md`
- **6.3** `JobServe agent prompts` — same six-file structure; `source_id="jobserve"`-specific selectors and guardrails
- **6.4** `CONTRACT.md template` — model pin, reasoning effort, max tokens, temperature, permitted tools, token budget, eval set ref
- **6.5** `Prompt-based relevance filtering` — heuristic pre-filtering before pgvector ranking; integrated into scraper agents

---

### E7 — Eval Framework (DeepEval + Ragas)

- **7.1** `Eval runner script` — `backend/admin/run_evals.py`; per-agent eval set execution
- **7.2** `DeepEval integration` — faithfulness and relevance metrics wired to CI; fail threshold defined in CONTRACT.md
- **7.3** `CI prompt regression step` — GitHub Actions runs evals on every merge; blocks deploy if threshold drops

---

## MVP 2 — AI Ranking, Persistence & Cloud Infrastructure

### E8 — Supabase PostgreSQL & Alembic

- **8.1** `Replace fake DB` — Supabase PostgreSQL with pgvector; all models migrated from in-memory dict
- **8.2** `asyncpg connection pool` — `db.py`; `pool_size=10`, `max_overflow=20`, `pool_timeout=30`, `pool_pre_ping=True`
- **8.3** `Alembic migrations` — `backend/migrations/`; runs via Supervisor priority 1 before uvicorn starts
- **8.4** `Full domain models` — `Job`, `Recruiter`, `Application`, `CV`, `CoverLetter`, `ScrapeRun`, `InterviewPrep`

---

### E9 — AI Ranking & RAG Agents

- **9.1** `Ranking agent` — 8-step pipeline: embeddings → cosine sim → cross-encoder rerank → sentiment → recruiter quality → salary normalisation → skill extraction → seniority validation
- **9.2** `RAG agent` — contextual retrieval from CV, applications, recruiter messages, saved jobs, preferences, skill graph
- **9.3** `Cover letter agent` — structured playbook; ATS keyword match ≥ 60% enforced before delivery
- **9.4** `Question answer agent` — RAG-grounded Q&A on specific job listings; `POST /api/v1/question-answer/{job_id}`
- **9.5** `Ragas eval in CI` — retrieval precision and context recall; blocks deploy if precision < 0.80

---

### E10 — Security & Orchestration Agents

- **10.1** `Security agent` — prompt injection detection, OWASP middleware, schema validation, RBAC enforcement, HTML sanitisation
- **10.2** `Workflow orchestrator` — Temporal workflows; retry with exponential backoff and jitter; DLQ; idempotency via SHA-256 job ID
- **10.3** `Circuit breakers` — per agent; opens after 3 consecutive failures; base 1s backoff, max 60s
- **10.4** `Admin DLQ routes` — `GET /api/v1/admin/dlq`, retry and discard endpoints; `replay_dlq.py` admin script

---

### E11 — Terraform & Multi-Cloud Deployment

- **11.1** `Azure Container Apps Terraform` — `infrastructure/terraform/azure/`; `main.tf`, `variables.tf`, `outputs.tf`
- **11.2** `AWS ECS Fargate Terraform` — `infrastructure/terraform/aws/`; multi-cloud portability via provider abstraction
- **11.3** `Terraform CI steps` — validate + plan on every PR; apply on merge to main
- **11.4** `Docker image signing` — GitHub Actions; tagged with Git commit SHA; pushed to registry on merge

---

### E12 — MVP 2 Prompts for AI Agents

- **12.1** `Ranking agent prompts` — `system.md`, `scoring.md`, `reranking.md`, `filtering.md`, CONTRACT.md pinned to medium effort
- **12.2** `RAG agent prompts` — `system.md`, `retrieval.md`, `embeddings.md`, `personalization.md`; high reasoning effort
- **12.3** `Cover letter agent prompts` — `system.md`, `tone.md`, `generation.md`, `templates.md`; medium effort
- **12.4** `Question answer & security agent prompts` — respective `system.md` and `tools.md`; high reasoning effort
- **12.5** `Orchestrator prompts` — `system.md`; xhigh reasoning effort for long-horizon coordination

---

## MVP 3 — Full Twelve-Factor Compliance, Observability & Auth

### E13 — Observability Stack

- **13.1** `OpenTelemetry integration` — distributed tracing and metrics across all agents and routers
- **13.2** `Grafana dashboards` — latency p50/p95, token usage, hallucination rate, retrieval precision, reranker confidence
- **13.3** `Prometheus + Loki` — metrics scraping; log aggregation from stdout structured JSON streams
- **13.4** `Sentry integration` — error tracking and alerting; Microsoft Clarity for frontend session replay
- **13.5** `Observability agent` — `agents/observability/`; traces, schema conformance rate ≥ 99%, hallucination alert if > 1%

---

### E14 — Auth, RBAC & Row-Level Security

- **14.1** `Supabase Auth + JWT` — JWT validation middleware in FastAPI; RBAC enforced at route level via JWT claims
- **14.2** `Row-Level Security` — Supabase RLS policies; users read and write only their own rows
- **14.3** `OWASP Top 10 hardening` — Trivy + Bandit scans in CI; SSRF allowlist; encrypted secrets via Azure Key Vault
- **14.4** `GDPR compliance` — export (PDF/JSON/CSV), deletion (PostgreSQL + pgvector + Redis + object storage), audit logging

---

### E15 — Twelve-Factor Completion & Admin Tooling

- **15.1** `Twelve-Factor audit` — verify all 12 factors against production config; document any gaps and close them
- **15.2** `Graceful shutdown` — SIGTERM handlers in all long-running processes; uvicorn drain, Temporal checkpoint, Playwright session close
- **15.3** `Structured admin tooling` — `replay_dlq.py`, `run_evals.py` fully wired; schedule pause/resume routes
- **15.4** `Disaster recovery validation` — backup restore drill; PostgreSQL WAL + Redis AOF; RTO ≤ 1 hr, RPO ≤ 15 min

---

_15 epics · 70 tasks · 4 milestones_
_E16 (Workflow Orchestration Infrastructure) added per workflow-impact-analysis.md — 6 tasks across MVP 1_
