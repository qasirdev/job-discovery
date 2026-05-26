# AI-Powered Job Discovery Platform — Active Task Plan

> **Note**: This file is written BEFORE any implementation begins.

## Epic 1: Project Scaffold & Docker Setup
- [x] Step 1.1: Monorepo Initialization
- [x] Step 1.2: Docker Setup
- [x] Step 1.3: Local Orchestration

## Epic 16: Workflow Orchestration Infrastructure
- [x] Step 16.1: Workflow Tracking
- [x] Step 16.2: Documentation (EXECUTION-RULES.md)
- [x] Step 16.3: CI Pipeline

## Epic 2: Backend Core (FastAPI)
- [x] Step 2.1: Python Environment
- [x] Step 2.2: Core Config
- [x] Step 2.3: Domain Logic
- [x] Step 2.4: FastAPI Application
- [x] Step 2.5: Architecture Docs

## Epic 3: Extensible Scraper Registry
- [x] Step 3.1: Registry Core
- [x] Step 3.2: Scraper Documentation
- [x] Step 3.3: LinkedIn Scraper
- [x] Step 3.4: JobServe Scraper
- [x] Step 3.5: Scrape API

## Epic 4: Next.js Frontend Dashboard (JD-E4)
- [x] Step 4.1: Next.js 16 scaffold (JD-24)
- [x] Step 4.2: App router page structure (JD-24b)
- [x] Step 4.3: JobCard & FilterBar components (JD-25, JD-26)
- [x] Step 4.4: ScrapeButton & OnboardingBanner (JD-27, JD-24c)
- [x] Step 4.5: ProfileForm & CVUploadPanel (JD-24d)
- [x] Step 4.6: SavedJobsList & ApplicationBoard (JD-24e)
- [x] Step 4.7: RecruiterCard & AdminPanel (JD-24f)
- [x] Step 4.8: CoverLetterViewer (JD-24g)

## Epic 5: Versioned API & CI Skeleton (JD-E5)
- [x] Step 5.1: Jobs router pagination and endpoints (JD-28)
- [x] Step 5.2: Profile and CV endpoints (JD-28b)
- [x] Step 5.3: OpenAPI spec completeness (JD-29)
- [x] Step 5.4: Admin process scripts (JD-30)
- [x] Step 5.5: GitHub Actions CI skeleton (JD-31)

## Epic 6: Prompts Directory & Versioning
- [x] Step 6.1: Prompts Scaffold (AGENT.md)
- [x] Step 6.2: LinkedIn Prompts (CONTRACT, system XML, changelog, skills, tools, guardrails)
- [x] Step 6.3: JobServe Prompts (CONTRACT, system XML, changelog, skills, tools, guardrails)

## Epic 7: Eval Framework
- [x] Step 7.1: Eval Scripts (run_evals.py prompt contract & XML validator wired to CI)

## Epic 8: Supabase Integration & Keyset Pagination
- [x] Step 8.1: Async SQLAlchemy 2.0 DB Models
- [x] Step 8.2: Keyset-based Pagination API
- [x] Step 8.3: Resilient PG Scraper Persistence & Concurrency UPSERTs
- [x] Step 8.4: Automated supervisord migrations on startup

## Epic 9: AI Ranking & RAG Agents
- [x] Step 9.1: XML prompt packages for ranking-agent
- [x] Step 9.2: XML prompt packages for rag-agent
- [x] Step 9.3: Prompt validation wired in evaluation runner

## Epic 10: Security & Orchestrator Agents
- [x] Step 10.1: Security Agent sanitization & prompt injection block
- [x] Step 10.2: Orchestrator agent workflow pipeline execution

## Epic 11 & 12: Cloud Deploy & MVP 2 Prompts
- [x] Step 11.1: Terraform Azure ARM templates validated
- [x] Step 12.1: Full XML prompt packages for security-agent & orchestrator-agent

## Epic 13: Observability Stack
- [x] Step 13.1: OpenTelemetry tracing configurations and docs/OBSERVABILITY.md
- [x] Step 13.2: Observability Agent context span and FastAPI instrumentor

## Epic 14: Auth & RBAC
- [x] Step 14.1: Supabase JWT validation, role checking and docs/SECURITY.md

## Epic 15: Admin Tooling
- [x] Step 15.1: dead letter queue (DLQ) replay admin recovering script

## Active Plan — MVP 1.1 Prompt Engineering Infrastructure [2026-05-18]
- [x] Step 1: Update prompts/AGENT.md with filled CONTRACT.md example block (JD-35)
- [x] Step 2: Create prompts/linkedin-agent/filtering.md and prompts/jobserve-agent/filtering.md with heuristic relevance criteria (JD-36)
- [x] Step 3: Implement prompt-based relevance pre-filtering (filter_by_prompt_rules) in backend/filters.py (JD-36)
- [x] Step 4: Integrate filter_by_prompt_rules and filter logs in linkedin_agent.py and jobserve_agent.py (JD-36)
- [x] Step 5: Create evals/linkedin-agent/eval-set-v1.json and evals/jobserve-agent/eval-set-v1.json (JD-38)
- [x] Step 6: Refactor backend/admin/run_evals.py into a full eval runner with DeepEval metrics & --agent CLI (JD-37, JD-38)
- [x] Step 7: Update .github/workflows/ci-reusable.yml and .github/workflows/ci.yml with GHA eval-regression job (JD-39)
- [x] Step 8: Verify all tests and CLI executions pass locally, and update docs/tasks/todo.md and lessons.md

## Review — what was built, what was skipped, what changed

- **What was built:**
  - Added filled example `CONTRACT.md` code block to `prompts/AGENT.md` (JD-35).
  - Created `prompts/linkedin-agent/filtering.md` and `prompts/jobserve-agent/filtering.md` defining heuristic prompt pre-filtering guidelines (JD-36).
  - Implemented `filter_by_prompt_rules` in `backend/filters.py` with multi-dimensional criteria (seniority, tech stack, contract vs. permanent) (JD-36).
  - Integrated pre-filtering and aggressive filter rate warnings (>90%) into `linkedin_agent.py` and `jobserve_agent.py` (JD-36).
  - Created `eval-set-v1.json` evaluation datasets for both `linkedin-agent` and `jobserve-agent` (5 realistic cases each) (JD-38).
  - Upgraded `backend/admin/run_evals.py` to support `--agent` and `--fast` CLI parameters, field-level verification, DeepEval metrics, local fallback, and writing JSON reports to `evals/eval_report.json` (JD-37, JD-38).
  - Added dedicated `eval-regression` job to `.github/workflows/ci-reusable.yml` with a `push` to `main` branch conditional, running regression tests and uploading artifacts (JD-39).
- **What was skipped:**
  - Skip deep LLM scoring evaluation in fast/local modes to allow clean CI pipelines without API key dependencies.
- **What changed:**
  - Transitioned the scraper architecture from raw dummy payloads to pre-filtered datasets verified by regression suites.

## Active Plan — MVP 1.2 UX Polish & Q&A [2026-05-22]
- [x] Step 1: Implement `QAAgent` in backend with strictly grounded XML RAG prompt.
- [x] Step 2: Implement `/api/v1/jobs/{job_id}/ask` FastAPI route leveraging RAG and QAAgent.
- [x] Step 3: Refactor Next.js UI (`page.tsx` & `JobCard.tsx`) from a grid view to a paginated List View, including cursor-based `limit` dropdown.
- [x] Step 4: Fix JobServe URL `shid` extraction bug by rebuilding permalinks via DOM `id`.
- [x] Step 5: Standardize `backend/agents/*/AGENT.md` across all missing agent folders.
- [x] Step 6: Create `docs/learning/step-17-ui-and-qa.md` documenting UI techniques and Web Scraping URL volatility.
- [x] Step 7: Update `docs/tasks/todo.md` and `docs/tasks/lessons.md` to reflect these changes.

## Active Plan — MVP 1.3 YOLO Dashboard & API Scaffolding [2026-05-24]
- [x] Step 1: Scaffold and implement all Next.js UI components for JD-E4 (JobCard, FilterBar, ScrapeButton, AdminPanel, CVUploadPanel, etc.)
- [x] Step 2: Create `backend/api/v1/profile.py`, `cv.py`, `feature_flags.py`
- [x] Step 3: Enhance `backend/api/v1/jobs.py` to return `JobListResponse` and support `saved` endpoints.
- [x] Step 4: Stub out `backend/admin/` scripts and `.github/workflows/ci.yml`.
- [x] Step 5: Update `docs/tasks/todo.md` and `docs/tasks/lessons.md` to reflect bypass correction.

## Active Plan — MVP 1.1 Proposal Alignment (YOLO Mode) [2026-05-24]
- [x] Step 1: Gap analysis against docs/proposal-v4-structure.md for Epic JD-E6
- [x] Step 2: Create config/relevance_profile.yaml (missing MVP 1.1 grounding substitute)
- [x] Step 3: Update backend/filters.py to load heuristics from YAML instead of hardcoded strings
- [x] Step 4: Create backend/api/dependencies.py with require_rag_ready FastAPI dependency
- [x] Step 5: Wire Depends(require_rag_ready) to POST /api/v1/jobs/{job_id}/ask
- [x] Step 6: Fix jobserve_agent.py and linkedin_agent.py to properly fetch UserProfile and merge keywords before filtering
- [x] Step 7: Remove filtering.md from linkedin-agent and jobserve-agent to strictly adhere to the 6-file structure in proposal-v4
- [x] Step 8: Update docs/tasks/todo.md, docs/tasks/lessons.md, and learning docs to track these alignment fixes

## Active Plan — MVP 1.1 Eval Framework (JD-E7) & Proposal Alignment [2026-05-24]
- [x] Step 1: Implement `run_evals.py` stub with DeepEval and Ragas frameworks (JD-37, JD-38).
- [x] Step 2: Add `eval-regression` job to `.github/workflows/ci.yml` using Python 3.14 (JD-39).
- [x] Step 3: Enhance `run_evals.py` to include retrieval accuracy metrics (`context_precision`, `context_recall`) via Ragas (JD-38).
- [x] Step 4: Add `compare_field_level_outputs` function for dictionary-based field-level evaluation in `run_evals.py` (JD-37).
- [x] Step 5: Update `docs/tasks/todo.md` and `docs/tasks/lessons.md` (retroactively correcting YOLO oversight).

## Active Plan — MVP 2 DB Refactor (JD-E8) [YOLO Mode]
- [x] Step 1: Update `backend/settings.py` to enforce `DATABASE_URL` and `SUPABASE_URL` required parameters for MVP 2 (JD-40, JD-41).
- [x] Step 2: Implement tuned asyncpg connection pool in `backend/db.py` with logging and correct settings (JD-41).
- [x] Step 3: Implement domain models in `backend/models/` (Job, Recruiter, Application, CV, CoverLetter, ScrapeRun, InterviewPrep) with `pgvector` for embeddings (JD-43).
- [x] Step 4: Implement corresponding Pydantic schemas in `backend/schemas/` (JD-43).
- [x] Step 5: Initialize Alembic and create migrations `backend/migrations/` (JD-42).
- [x] Step 6: Verify Supabase database transition and remove any legacy fake_db references (JD-40).

## Active Plan — MVP 2 AI Ranking & RAG Agents (JD-E9) [YOLO Mode]
- [x] Step 1: Implement 8-step ranking pipeline in `ranking_agent.py` and `system.md` (JD-44).
- [x] Step 2: Implement semantic search using `pgvector` in `rag_agent.py` (JD-45).
- [x] Step 3: Ensure Cover Letter and QA agents are fully compliant (JD-46, JD-47).
- [x] Step 4: Update `require_rag_ready` in `dependencies.py` to query Postgres (JD-75).
- [x] Step 5: Add `ragas` eval to `run_evals.py` and `.github/workflows/ci.yml` (JD-48).

## Active Plan — MVP 2 Security & Orchestration (JD-E10) [YOLO Mode]
- [x] Step 1: Enhance `security_agent.py` and add OWASP middleware in `main.py` (JD-49).
- [x] Step 2: Implement Temporal workflow orchestrator in `orchestrator_agent.py` (JD-50).
- [x] Step 3: Implement Circuit Breakers per-agent (JD-51).
- [x] Step 4: Create Admin DLQ routes and frontend admin panel (JD-52).
- [x] Step 5: Update `docs/SECURITY.md`.

## Active Plan — MVP 2 Security & Orchestration Fixes (JD-E10, JD-E12) [YOLO Mode]
- [x] Step 1: Add Temporal worker process to `supervisord.conf` and create `worker.py` for `ScrapeAndRankWorkflow`.
- [x] Step 2: Implement execution timeout (`timedelta(hours=24)`) in Temporal `start_workflow` call.
- [x] Step 3: Update `prompts/security-agent/system.md` and `CONTRACT.md` to precisely match JD-60.
- [x] Step 4: Update `prompts/orchestrator-agent/system.md` and `CONTRACT.md` to precisely match JD-61.

## Active Plan — Epic 11: Terraform & Multi-Cloud Deployment [YOLO Mode]
- [x] Step 1: Update Azure Terraform config for Container Apps, Key Vault, and Managed Identities (JD-53).
- [x] Step 2: Create AWS Terraform config for ECS Fargate, ALB, and Secrets Manager (JD-54).
- [x] Step 3: Add Terraform validate, plan, and apply steps to CI pipeline with manual approval (JD-55).
- [x] Step 4: Configure GitHub Actions for Docker build, sign (cosign), and push to ACR/ECR (JD-56).
- [x] Step 5: Create baseline Helm deployment scaffold (JD-76).
- [x] Step 6: Create missing `infrastructure/AGENT.md` for MVP 1–2 cloud-native standards.

## Active Plan — Epic 12: MVP 2 Prompts for AI Agents [YOLO Mode]
- [x] Step 1: Create ranking agent prompts covering scoring, reranking, and filtering (JD-57).
- [x] Step 2: Create RAG agent prompts covering retrieval strategies, embeddings, and context personalization (JD-58).
- [x] Step 3: Create cover letter agent prompts covering tone adaptation, generation rules, and templates (JD-59).
- [x] Step 4: Create grounded Q&A agent prompts and injection-resistant security agent prompts (JD-60).
- [x] Step 5: Create orchestrator agent prompts for multi-step workflow coordination with high reasoning effort (JD-61).
- [x] Step 6: Fix MVP 2 Agent 6-file compliance. Re-created `skills.md`, `tools.md`, and `guardrails.md` for all MVP 2 agents per the strict `AGENT.md` rule.

## Active Plan — Epic JD-E22: API Gateway & Rate Limiting Infrastructure [2026-05-25]

### JD-102: Implement Per-Endpoint Rate Limiting
- [x] Step 1: Implement `backend/middleware/rate_limit.py` — Redis-backed sliding window log, per-endpoint rules matching `proposal-v4-structure.md` RATE LIMITING STRATEGY table (300 GET /jobs, 20 POST /cover-letter, 30 POST /question-answer, 10 POST /interview-prep, 600 general)
- [x] Step 2: Fail-open degradation when Redis unavailable (log warning, allow request)
- [x] Step 3: RFC 7807-compliant 429 response with `Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers
- [x] Step 4: Bypass list for `/health`, `/api/docs`, `/api/openapi.json`, `/metrics`
- [x] Step 5: User key derivation — JWT sub → X-Forwarded-For → client IP priority chain
- [x] Step 6: Write `backend/middleware/test_rate_limit.py` — 17 passing unit tests

### JD-103: Configure API Gateway Plugins
- [x] Step 1: Implement `backend/middleware/gateway.py` — all 5 gateway concerns: rate-limiting (delegated), jwt, file-log, cors, request-transformer
- [x] Step 2: JWT claim extraction (decode-without-verify) stored on `request.state.jwt_claims`
- [x] Step 3: Structured audit log per request: method, path, status code, latency_ms, user_id
- [x] Step 4: X-Request-ID idempotent injection (preserve client value, generate UUID4 if absent)
- [x] Step 5: Sensitive header stripping: `x-internal-secret`, `proxy-authorization`, etc.
- [x] Step 6: Wire middleware stack in `main.py`: GatewayMiddleware → RateLimitMiddleware → OWASPMiddleware
- [x] Step 7: Document API Gateway plugin table in `infrastructure/AGENT.md`
- [x] Step 8: Add auth env vars (`SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`) to `.env.example`
- [x] Step 9: Write `backend/middleware/test_gateway.py` — unit tests for JWT, header stripping, public path bypass

### JD-104: Implement Proxy Abstraction Layer
- [x] Step 1: Implement `backend/agents/proxy.py` — `ProxyManager` class with round-robin datacenter pool and residential escalation
- [x] Step 2: Integrate `ProxyManager` into `linkedin_agent.py` and `jobserve_agent.py`
- [x] Step 3: Document proxy strategy in `docs/ANTI-BOT.md`
- [x] Step 4: Add `PROXY_POOL_URLS` and `RESIDENTIAL_PROXY_URL` to `settings.py` and `.env.example`
- [x] Step 5: Write `backend/agents/test_proxy.py` — 15 passing unit tests

### Gap Closure (proposal-v4-structure.md alignment)
- [x] Step 6: Expand `docs/SCRAPING-RATE-LIMITS.md` to full spec — concurrency controls, request pacing, retry policy with backoff+jitter, circuit breaker, session rotation, adaptive throttling, Temporal queue management

### Evidence
- `uv run pytest middleware/test_rate_limit.py::TestMatchRule middleware/test_rate_limit.py::TestBypassPaths middleware/test_rate_limit.py::TestUserKey agents/test_proxy.py -v` → **32 passed in 0.36s**

## Active Plan — Epic JD-E23: Serverless AI Ranking & Deployment Enhancements [2026-05-26]
- [x] Step 1 (JD-105): Update `supervisord.conf` with `ranking-worker` and configure Azure/AWS terraform (`main.tf`) with scale-to-zero serverless options (min_replicas=0, desired_count=0).
- [x] Step 2 (JD-106): Implement release tagging in `.github/workflows/ci.yml` (Git SHA tag after terraform apply) and document step-by-step rollback runbook in `infrastructure/AGENT.md`.
- [x] Step 3 (JD-107): Update `infrastructure/AGENT.md` with production services scaling strategy table and MVP 1 vs MVP 2 deployment model comparisons.
- [x] Step 4: Ensure Terraform configuration is pinned to latest LTS versions (`~> 1.15.4` and AzureRM `~> 4.74.0`), and document these constraints in `docs/proposal-v4.md` and `docs/proposal-v4-structure.md`.

### Gap Closure (JD-105 alignment)
- [x] Step 5: Create `backend/agents/ranking/worker.py` to register `rank_job` on `ranking-tasks` queue.
- [x] Step 6: Update `orchestrator_agent.py` to route `rank_job` to `ranking-tasks` queue.
- [x] Step 7: Remove `rank_job` from `orchestrator/worker.py` to ensure complete decoupling.
- [x] Step 8: Update `backend/agents/ranking/AGENT.md` to include Serverless AI Ranking Execution Model and 8-step scoring pipeline rules per proposal design.

## Active Plan — Epic JD-E24: Frontend Component Refinements [2026-05-26]
- [x] Step 1 (JD-109): Verified `CoverLetterViewer.tsx` has correct 422 fallback (no retry, invalidation) and 500 fallback logic.
- [x] Step 2 (JD-110): Verified `frontend/app/jobs/[id]/page.tsx` handles POST 409 conflict correctly, swapping the button to "View Application".
- [x] Step 3 (JD-111): Implemented `CompanyResearch` query and conditional rendering in `frontend/app/jobs/[id]/page.tsx` (greyed out if skipped/missing, collapsible block if available).
