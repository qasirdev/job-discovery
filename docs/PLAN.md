# Auto-Mode Implementation Plan: AI-Powered Job Discovery Platform

## 🤖 System Prompt for AI Agent (Cursor, Windsurf, Antigravity, Claude, GPT, etc.)

You are operating in an autonomous "Auto/YOLO" mode to implement the **AI-Powered Job Discovery Platform**.
Your source of truth for the architecture, project structure, and requirements are the following files in the project root:
- `docs/proposal-v4.md`
- `docs/proposal-v4-structure.md`
- `docs/proposal-v4-epics.md`
- `docs/tasks/todo.md`
- `docs/tasks/lessons.md`
- `docs/jira-tickets/*.md`


### 🔄 Execution Loop (MANDATORY FOR EVERY STEP)
For **EVERY** step listed below, you MUST execute the following loop:
1. **Implement**: Write code with production grade 2026 industry level best practices using official documentation of the techstack used, create files, and configure systems as described in the step. Adhere strictly to the multi-file `AGENT.md` structure outlined in `proposal-v4-structure.md`. Do not guess; read the proposal files to extract specific code snippets (e.g., `supervisord.conf`, `Dockerfile`).
2. **Verify**: Run necessary commands to prove it works (e.g., `tsc --noEmit`, `npm run lint`, `uv run ruff check .`, `docker build -t job-discovery .`). Do not move to the next step if errors exist.
3. **Track**: Append a detailed completion entry to `implementation-done.md`. Include the Step ID, a summary of what was built, and the timestamp.
4. **Teach**: Create a new markdown file in the `docs/learning/` directory (e.g., `docs/learning/step-1.1-monorepo.md`). This file MUST contain:
   - **Learning Objectives:** What a beginner developer should learn from the code/setup introduced in this step.
   - **Technical Details:** A clear, beginner-friendly explanation of the concepts, tools (like Docker multi-stage builds, Pydantic, or Next.js static exports), and design patterns used in the step.

---

## 🚀 Phase 1: MVP 1 — Scraper Foundation & In-Memory Store

### Epic 1: Project Scaffold & Docker Setup
- [ ] **Step 1.1:** Monorepo Initialization. Create `.env.example`, `.gitignore`, and the root `AGENT.md` index file.
- [ ] **Step 1.2:** Docker Setup. Create the multi-stage `Dockerfile` (frontend build -> backend runtime), `nginx.conf`, and `supervisord.conf`. *(Extract exact code from proposal-v4-structure.md)*
- [ ] **Step 1.3:** Local Orchestration. Create `docker-compose.yml` for local development.

### Epic 16: Workflow Orchestration Infrastructure
- [ ] **Step 16.1:** Workflow Tracking. Create `tasks/todo.md` and `tasks/lessons.md`.
- [ ] **Step 16.2:** Documentation. Create `docs/EXECUTION-RULES.md` and populate with MUST/MUST NOT rules. Update root `AGENT.md` workflow rules.
- [ ] **Step 16.3:** CI Pipeline. Create `.github/workflows/ci.yml` (lint, type checks, check-workflow-docs stub).

### Epic 2: Backend Core (FastAPI)
- [ ] **Step 2.1:** Python Environment. Create `backend/pyproject.toml`, set up `uv`, and install FastAPI + dependencies. Create `backend/AGENT.md`.
- [ ] **Step 2.2:** Core Config. Create `backend/settings.py` (Pydantic Settings) and `backend/logging_config.py` (JSON structured logger).
- [ ] **Step 2.3:** Domain Logic. Create `backend/models.py` (`Job`, `ScrapeResult`) and `backend/filters.py` (keyword filtering).
- [ ] **Step 2.4:** FastAPI Application. Create `backend/main.py` with `/api/v1/` routing and an in-memory fake DB (MVP 1 exception).
- [ ] **Step 2.5:** Architecture Docs. Create `docs/ARCHITECTURE.md`, `docs/ENGINEERING-STANDARDS.md`, `docs/RELIABILITY.md`.

### Epic 3: Extensible Scraper Registry
- [ ] **Step 3.1:** Registry Core. Create `backend/agents/base.py` (`BaseScrapeAgent` ABC) and `backend/agents/registry.py` (`@register` decorator).
- [ ] **Step 3.2:** Scraper Documentation. Create `backend/agents/AGENT.md`.
- [ ] **Step 3.3:** LinkedIn Scraper. Create `backend/agents/linkedin/linkedin_agent.py` and its `AGENT.md`.
- [ ] **Step 3.4:** JobServe Scraper. Create `backend/agents/jobserve/jobserve_agent.py` and its `AGENT.md`.
- [ ] **Step 3.5:** Scrape API. Create `backend/routers/scrape.py` handling `POST /api/v1/scrape`.

### Epic 4: Next.js Frontend Dashboard
- [ ] **Step 4.1:** Next.js Init. Scaffold `frontend/` (Next.js 16, output: "export", Tailwind 4, TS). Create `frontend/AGENT.md`. Adjust `next.config.ts`.
- [ ] **Step 4.2:** UI Components. Create `JobCard.tsx`, `FilterBar.tsx`, and `ScrapeButton.tsx` inside `frontend/components/`.
- [ ] **Step 4.3:** Dashboard View. Update `frontend/app/page.tsx` to list jobs and trigger the scraper API.

### Epic 5: Versioned API & CI Skeleton
- [ ] **Step 5.1:** Jobs API. Create `backend/routers/jobs.py` (`GET /api/v1/jobs` with cursor pagination).
- [ ] **Step 5.2:** Admin Scripts. Create `backend/admin/seed_keywords.py` and `backend/admin/clear_db.py`.

---

## 🧠 Phase 2: MVP 1.1 — Prompt Engineering Infrastructure

### Epic 6: Prompts Directory & Versioning
- [ ] **Step 6.1:** Prompts Scaffold. Create `prompts/` folder and `prompts/AGENT.md`.
- [ ] **Step 6.2:** LinkedIn Prompts. Create `prompts/linkedin-agent/CONTRACT.md`, `system.md`, etc.
- [ ] **Step 6.3:** JobServe Prompts. Create `prompts/jobserve-agent/CONTRACT.md`, `system.md`, etc.

### Epic 7: Eval Framework
- [ ] **Step 7.1:** Eval Scripts. Create `backend/admin/run_evals.py` and wire it up to run tests on agents.

---

## 💾 Phase 3: MVP 2 — Supabase, AI Ranking & Terraform

### Epic 8: Supabase & Alembic
- [ ] **Step 8.1:** Database Setup. Create `backend/db.py` (asyncpg pool configuration).
- [ ] **Step 8.2:** Migrations. Initialize Alembic `backend/migrations/` and create initial schemas replacing the fake DB.

### Epic 9: AI Ranking & RAG Agents
- [ ] **Step 9.1:** Ranking Agent. Implement `backend/agents/ranking/ranking_agent.py` and its `AGENT.md`.
- [ ] **Step 9.2:** RAG Agent. Implement `backend/agents/rag/rag_agent.py` and its `AGENT.md`.
- [ ] **Step 9.3:** Cover Letter Agent. Implement `backend/agents/cover-letter/cover_letter_agent.py` and its `AGENT.md`.

### Epic 10: Security & Orchestrator Agents
- [ ] **Step 10.1:** Security Agent. Implement `backend/agents/security/security_agent.py` (Prompt injection, OWASP).
- [ ] **Step 10.2:** Orchestrator. Implement `backend/agents/orchestrator/orchestrator_agent.py`.

### Epic 11 & 12: Cloud Deploy & MVP 2 Prompts
- [ ] **Step 11.1:** Terraform. Create `infrastructure/terraform/azure/main.tf`, `variables.tf`, `outputs.tf`.
- [ ] **Step 12.1:** MVP 2 Prompts. Populate `prompts/` for ranking, RAG, security, and orchestrator agents.

---

## 🛡️ Phase 4: MVP 3 — Twelve-Factor & Observability

### Epic 13: Observability Stack
- [ ] **Step 13.1:** OpenTelemetry. Add tracing configurations. Create `docs/OBSERVABILITY.md`.
- [ ] **Step 13.2:** Observability Agent. Implement `backend/agents/observability/observability_agent.py`.

### Epic 14: Auth & RBAC
- [ ] **Step 14.1:** Supabase Auth. Add JWT validation middleware to FastAPI. Update `docs/SECURITY.md`.

### Epic 15: Admin Tooling
- [ ] **Step 15.1:** DR & Admin. Polish all scripts in `backend/admin/` (`replay_dlq.py`, etc.) and ensure graceful shutdown.

---
## 🎯 AI Agent: Start Execution
When you are ready to begin, start with **Phase 1, Epic 1, Step 1.1**. Follow the Execution Loop precisely.