# AI-Powered Job Discovery Platform — Active Task Plan

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
