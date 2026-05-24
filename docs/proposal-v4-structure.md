
# PROJECT-STRUCTURE.md

# AI-Powered Job Discovery Platform — Proposed Multi-File Project Structure

**Proposal Version:** 1.2.0 (based on `004-01-saas-job-search-proposal-v4.md`)
**Last Updated:** May 2026

This document replaces the single `AGENT-updated.md` monolith.
Every section of that file maps to a purpose-specific `.md` file
living alongside the code it governs.

---

## MVP DELIVERY OVERVIEW

| Milestone | Scope Summary |
|---|---|
| **MVP 1** | LinkedIn + JobServe scrapers, extensible registry, in-memory DB, FastAPI `/api/v1/`, Next.js dashboard, single Docker container, GitHub Actions CI skeleton |
| **MVP 1.1** | Advanced prompt engineering infrastructure (`prompts/`), system prompt versioning, Contract + Changelog management, prompt-based relevance filtering, DeepEval + Ragas evaluation framework |
| **MVP 2** | Supabase PostgreSQL + pgvector, Alembic migrations, AI ranking pipeline, Terraform (Azure Container Apps + AWS ECS Fargate), OWASP middleware, observability stack, circuit breakers, connection pool tuning |
| **MVP 3** | Full Twelve-Factor compliance, OpenTelemetry, Grafana, Prometheus, Loki, Sentry, RBAC, RLS, JWT auth, structured admin process tooling |

---

## DESIGN PRINCIPLES

- one `.md` file per concern — no mixed responsibilities
- each `.md` lives in the folder it governs so context is co-located with code
- the root `AGENT.md` becomes a lightweight index that references all child files
- the entire FE + BE runs in a single Docker container using a multi-stage build (MVP 1 local dev; distributed containers from MVP 2 onwards)
- Nginx proxies / to the Next.js Node server on port 3000 and reverse-proxies `/api` to FastAPI on port 8000
- all secrets are injected at runtime via environment variables — never baked into images
- `prompts/` lives at the monorepo root — not inside `backend/` — so prompt versioning is independent of backend deployments (introduced in **MVP 1.1**)
- `tasks/` lives at the monorepo root — workflow management is process-level and applies across all areas of the codebase (introduced in **MVP 1**)
- use production grade 2026 industry level tools and practices - reference [Reusing Workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- use production grade 2026 industry level best practices for each technology. Reference the official documentation of the technologies being used for best practices.

---

## FULL PROJECT TREE

job-discovery/
│
├── AGENT.md                               # Root index — no standards content; includes workflow rules
├── docker-compose.yml
├── Dockerfile                             # Multi-stage: FE build + BE runtime + Nginx
├── nginx.conf
├── supervisord.conf                       # MVP 1: Supervisor process config (migrate → nginx → fastapi)
├── .env.example                           # All required env vars documented
│
│
├── .github/
│   └── workflows/
│       └── ci.yml                         # MVP 1: GitHub Actions CI skeleton
│
│
├── docs/                                  # Cross-cutting documentation
│   ├── jira-tickets/
│   │   ├── jd-mvp1.4b.csv
│   │   ├── jd-mvp1.1.csv
│   │   └── ... etc
│   ├── tasks/                             # MVP 1: Workflow management — process-level, not architecture-level
│   │   ├── todo.md                        # Active task plan with checkable items; written before any implementation
│   │   └── lessons.md                     # Self-improvement log; updated after every user correction
│   ├── ARCHITECTURE.md                    # ← from: SYSTEM ROLE + PRIMARY OBJECTIVE
│   ├── ENGINEERING-STANDARDS.md           # ← from: CORE ENGINEERING STANDARDS (FE/BE/DB stacks)
│   ├── SECURITY.md                        # ← from: AUTH & SECURITY + OWASP + PROMPT INJECTION DEFENSE
│   ├── OBSERVABILITY.md                   # ← from: OBSERVABILITY (MANDATORY)
│   ├── RELIABILITY.md                     # ← from: RELIABILITY ENGINEERING + DIFA + REACT LOOP
│   ├── REAL-TIME.md                       # ← from: REAL-TIME ARCHITECTURE
│   ├── ANALYTICS.md                       # ← from: ANALYTICS & USER TRACKING
│   ├── ADTECH-CONTEXT.md                  # ← from: ADTECH DOMAIN CONTEXT
│   └── EXECUTION-RULES.md                 # ← from: FINAL EXECUTION RULES; includes workflow MUST/MUST NOT section
│
│
├── config/
│   ├── relevance_profile.yaml             # MVP 1.1 grounding substitute
│
├── frontend/                              # Next.js 16 + React 19 — MVP 1
│   ├── AGENT.md                           # ← from: FRONTEND DASHBOARD features + FE stack requirements
│   ├── next.config.ts                     # output: "standalone" — runs Next.js Node server
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── .env.local.example
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                           # Dashboard — renders OnboardingBanner if not ready
│   │   ├── globals.css
│   │   ├── onboarding/
│   │   │   └── page.tsx                       # Onboarding flow: ProfileForm → CVUploadPanel → status
│   │   ├── profile/
│   │       └── page.tsx                       # Edit existing UserProfile and replace CV
│   │   ├── jobs/
│   │   │   └── [id]/
│   │   │       └── page.tsx                   # Job detail: Save button, Generate Cover Letter button, Generate Interview Prep button
│   │   ├── saved/
│   │   │   └── page.tsx                       # Saved jobs list — renders SavedJobsList.tsx
│   │   ├── applications/
│   │   │   ├── page.tsx                       # Application list — status board grouped by enum state
│   │   │   └── [id]/
│   │   │       └── page.tsx                   # Application detail — status transitions, notes
│   │   ├── recruiters/
│   │   │   └── page.tsx                       # Recruiter list — notes, interaction score, log interaction
│   │   ├── admin/
│   │   │   └── page.tsx                       # Admin panel: DLQ list, retry/discard, schedule pause/resume
│   └── components/
│       ├── JobCard.tsx
│       ├── FilterBar.tsx
│       ├── ScrapeButton.tsx
│       ├── ObservabilityPanel.tsx         # MVP 2+: agent trace + token usage panel
│       ├── SavedJobsList.tsx
│       ├── ApplicationBoard.tsx               # Kanban-style board grouped by Application.status enum
│       ├── ApplicationStatusBadge.tsx         # Colour-coded badge for each status value
│       ├── RecruiterCard.tsx                  # Recruiter name, company, score, interaction log button
│       ├── AdminPanel.tsx                     # DLQ table with retry/discard buttons; scrape schedule controls
│       ├── CoverLetterViewer.tsx
│       ├── CVUploadPanel.tsx
│       ├── ProfileForm.tsx
│       └── OnboardingBanner.tsx
│
│
├── backend/                               # Python 3.14 + FastAPI + uv
│   ├── AGENT.md                           # ← from: BACKEND STACK + API DESIGN STANDARDS + MCP + PROMPT CACHING
│   ├── pyproject.toml
│   ├── main.py                            # MVP 1: app entrypoint + agent auto-discovery imports
│   ├── models/                            # MVP 1: SQLAlchemy models (Job, ScrapeResult); MVP 2+: full domain models
│   ├── schemas/                           # MVP 1: Pydantic v2 schemas for request/response validation
│   ├── repositories/                      # MVP 1: Data access layer (no SQLAlchemy in route handlers)
│   ├── services/                          # MVP 1: Business logic layer
│   ├── fake_db.json                       # MVP 1: file-backed in-memory store (gitignored) — survives container restarts
│   ├── filters.py                         # MVP 1: keyword filtering; MVP 1.1: merges UserProfile fields over relevance_profile.yaml defaults
│   ├── logging_config.py                  # MVP 1: Twelve-Factor XI — structured JSON logger (shared by all agents)
│   ├── db.py                              # MVP 2: asyncpg connection pool (pool_size=10, max_overflow=20)
│   ├── settings.py                        # MVP 1: Pydantic Settings (PostgresDsn, BaseSettings) — all env vars typed and validated at startup
│   │
│   ├── admin/                             # MVP 1+: Twelve-Factor XII — one-off admin processes
│   │   ├── seed_keywords.py
│   │   ├── replay_dlq.py
│   │   ├── clear_db.py                    # Dev only
│   │   └── run_evals.py
│   │
│   ├── agents/                            # One subfolder per agent
│   │   ├── AGENT.md                       # ← from: MULTI-AGENT ARCHITECTURE rules; includes subagent execution rules
│   │   ├── base.py                        # MVP 1: BaseScrapeAgent ABC
│   │   ├── registry.py                    # MVP 1: @register decorator + get_all_agents()
│   │   │
│   │   ├── linkedin/                      # MVP 1
│   │   │   ├── AGENT.md                   # ← from: LinkedIn Agent responsibilities
│   │   │   └── linkedin_agent.py
│   │   │
│   │   ├── jobserve/                      # MVP 1
│   │   │   ├── AGENT.md                   # ← from: JobServe Agent responsibilities
│   │   │   └── jobserve_agent.py
│   │   │
│   │   ├── ranking/                       # MVP 2
│   │   │   ├── AGENT.md                   # ← from: Ranking Agent + AI RELEVANCE MATCHING (scoring pipeline)
│   │   │   └── ranking_agent.py
│   │   │
│   │   ├── rag/                           # MVP 2
│   │   │   ├── AGENT.md                   # ← from: RAG Agent + RAG PERSONALIZATION (retrieval sources: CV, SavedJob, UserProfile, Application history, etc. + eval metrics. RAG corpus bootstrap: upload CV -> parse/chunk -> pgvector -> ready)
│   │   │   └── rag_agent.py
│   │   │
│   │   ├── cover-letter/                  # MVP 2
│   │   │   ├── AGENT.md                   # ← from: Cover Letter Agent + COVER LETTER PLAYBOOK (parses raw description into job_structured JSONB)
│   │   │   └── cover_letter_agent.py
│   │   │
│   │   ├── question-answer/               # MVP 2
│   │   │   ├── AGENT.md
│   │   │   └── question_answer_agent.py
│   │   │
│   │   ├── security/                      # MVP 2
│   │   │   ├── AGENT.md                   # ← from: Security Agent responsibilities
│   │   │   └── security_agent.py
│   │   │
│   │   ├── observability/                 # MVP 3
│   │   │   ├── AGENT.md                   # ← from: Observability Agent responsibilities
│   │   │   └── observability_agent.py
│   │   │
│   │   ├── orchestrator/                  # MVP 2
│   │   │   ├── AGENT.md                   # ← from: Workflow Orchestrator Agent responsibilities
│   │   │   └── orchestrator_agent.py
│   │   │
│   │   ├── application-assistant/         # Optional (post-MVP 3)
│   │   │   ├── AGENT.md                   # ← from: Autonomous Job Application Assistant Agent
│   │   │   └── application_agent.py
│   │   │
│   │   └── interview-prep/                # Optional (post-MVP 3)
│   │       ├── AGENT.md                   # ← from: Interview Preparation Intelligence Agent (fetches company research via web search)
 The `company_research` collapsible section checks the shape of the JSONB field before rendering: - If `company_research.status === "skipped"`: render the section header as greyed/muted, with body text: `"Company intelligence is not available for this listing — the company could not be identified from the job data."`  No expand/collapse interaction is needed; the section is shown collapsed and non-interactive. - If `company_research` contains structured research data (has `website`, `tech_stack`, etc.): render normally as a collapsible section with the research content. - If `company_research` is null or absent: treat identically to the skipped state. 
│   │       └── interview_agent.py
│   │
│   ├── migrations/                        # MVP 2: Alembic migrations (Twelve-Factor XII)
│   │   ├── env.py
│   │   ├── alembic.ini
│   │   └── versions/
│   │
│   └── api/                               # MVP 1: Domain-driven API routes
│       ├── v1/
│       │   ├── jobs.py                    # MVP 1: GET /api/v1/jobs, GET /api/v1/jobs/{id}
│       │   ├── scrape.py                  # MVP 1: POST /api/v1/scrape (registry-driven)
│       │   ├── cover_letter.py            # MVP 2: POST /api/v1/cover-letter/{job_id}
│       │   ├── question_answer.py         # MVP 2: POST /api/v1/question-answer/{job_id}
│       │   ├── interview.py               # MVP 2+: POST /api/v1/interview-prep/{job_id}
│       └── dependencies.py                # MVP 1.1+: require_rag_ready FastAPI dependency — enforces CV + profile prerequisites at API layer
│
│
├── prompts/                               # MVP 1.1: All LLM prompt files — versioned by agent
│   ├── AGENT.md                           # ← from: MULTI-AGENT PROMPT STRUCTURE + PROMPT VERSIONING + AI PROMPT ENGINEERING STANDARDS
│   │
│   ├── linkedin-agent/                    # MVP 1.1
│   │   ├── CONTRACT.md                    # Model pin, token budget, reasoning effort, eval set ref
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── jobserve-agent/                    # MVP 1.1
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── ranking-agent/                     # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   ├── guardrails.md
│   │   ├── scoring.md
│   │   ├── reranking.md
│   │   └── filtering.md
│   │
│   ├── rag-agent/                         # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   ├── guardrails.md
│   │   ├── retrieval.md
│   │   ├── embeddings.md
│   │   └── personalization.md
│   │
│   ├── cover-letter-agent/                # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   ├── guardrails.md
│   │   ├── tone.md
│   │   ├── generation.md
│   │   └── templates.md
│   │
│   ├── question-answer-agent/             # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── security-agent/                    # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── orchestrator/                      # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── application-assistant/             # Optional (post-MVP 3)
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   └── interview-prep/                    # Optional (post-MVP 3)
│       ├── CONTRACT.md
│       ├── CHANGELOG.md
│       ├── system.md
│       ├── skills.md
│       ├── tools.md
│       └── guardrails.md
│
│
└── infrastructure/                        # Cloud-native deployment
├── AGENT.md                           # ← from: CLOUD-NATIVE ENGINEERING + CI/CD
├── terraform/
│   ├── azure/                         # MVP 2: Azure Container Apps (primary)
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── aws/                           # MVP 2: AWS ECS Fargate
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── helm/
└── job-discovery/
├── Chart.yaml
└── values.yaml
---

## SECTION-TO-FILE MAPPING TABLE

Every section from the proposal maps to exactly one file below.
No section is lost. No section appears in more than one file.

| Proposal Section | Target File | MVP |
|---|---|---|
| SYSTEM ROLE | `docs/ARCHITECTURE.md` | MVP 1 |
| PRIMARY OBJECTIVE | `docs/ARCHITECTURE.md` | MVP 1 |
| CORE ENGINEERING STANDARDS — Frontend Stack | `frontend/AGENT.md` | MVP 1 |
| CORE ENGINEERING STANDARDS — Backend Stack | `backend/AGENT.md` | MVP 1 |
| CORE ENGINEERING STANDARDS — Database Stack | `backend/AGENT.md` | MVP 2 |
| Twelve-Factor Compliance (all 12 factors) | `docs/ENGINEERING-STANDARDS.md` | MVP 1–3 |
| Structured JSON Logger | `backend/logging_config.py` | MVP 1 |
| Pydantic Settings (BaseSettings + PostgresDsn) | `backend/settings.py` | MVP 1 |
| asyncpg Connection Pool | `backend/db.py` | MVP 2 |
| Admin Processes (Factor XII) | `backend/admin/` | MVP 1 |
| Alembic Migrations | `backend/migrations/` | MVP 2 |
| Extensible Scraper Registry | `backend/agents/base.py` + `backend/agents/registry.py` | MVP 1 |
| MULTI-AGENT ARCHITECTURE (rules) | `backend/agents/AGENT.md` | MVP 1 |
| LinkedIn Agent | `backend/agents/linkedin/AGENT.md` | MVP 1 |
| JobServe Agent | `backend/agents/jobserve/AGENT.md` | MVP 1 |
| Ranking Agent | `backend/agents/ranking/AGENT.md` | MVP 2 |
| RAG Agent | `backend/agents/rag/AGENT.md` | MVP 2 |
| Cover Letter Agent | `backend/agents/cover-letter/AGENT.md` | MVP 2 |
| Question Answer Agent | `backend/agents/question-answer/AGENT.md` | MVP 2 |
| Security Agent | `backend/agents/security/AGENT.md` | MVP 2 |
| Observability Agent | `backend/agents/observability/AGENT.md` | MVP 3 |
| Workflow Orchestrator Agent | `backend/agents/orchestrator/AGENT.md` | MVP 2 |
| Autonomous Job Application Assistant Agent | `backend/agents/application-assistant/AGENT.md` | Optional |
| Interview Preparation Intelligence Agent (fetches company research via web search) | `backend/agents/interview-prep/AGENT.md` | Optional |
| Scalable API Design (versioning, pagination, RFC 7807 structured errors) | `backend/AGENT.md` | MVP 1–2 |
| MULTI-AGENT PROMPT STRUCTURE | `prompts/AGENT.md` | MVP 1.1 |
| PROMPT VERSIONING | `prompts/AGENT.md` | MVP 1.1 |
| AI PROMPT ENGINEERING STANDARDS (full section) | `prompts/AGENT.md` | MVP 1.1 |
| Prompt Contract + Changelog for LinkedIn Agent | `prompts/linkedin-agent/` | MVP 1.1 |
| Prompt Contract + Changelog for JobServe Agent | `prompts/jobserve-agent/` | MVP 1.1 |
| Prompt Contract + Changelog for Ranking Agent | `prompts/ranking-agent/` | MVP 2 |
| Prompt Contract + Changelog for RAG Agent | `prompts/rag-agent/` | MVP 2 |
| Prompt Contract + Changelog for Cover Letter Agent | `prompts/cover-letter-agent/` | MVP 2 |
| Prompt Contract + Changelog for Question Answer Agent | `prompts/question-answer-agent/` | MVP 2 |
| Prompt Contract + Changelog for Security Agent | `prompts/security-agent/` | MVP 2 |
| Prompt Contract + Changelog for Orchestrator | `prompts/orchestrator/` | MVP 2 |
| JOB DISCOVERY WORKFLOW | `backend/agents/linkedin/AGENT.md` + `backend/agents/jobserve/AGENT.md` | MVP 1 |
| AI RELEVANCE MATCHING (scoring pipeline) | `backend/agents/ranking/AGENT.md` | MVP 2 |
| RAG PERSONALIZATION | `backend/agents/rag/AGENT.md` | MVP 2 |
| AUTHENTICATION & SECURITY | `docs/SECURITY.md` | MVP 3 |
| OWASP TOP 10 COMPLIANCE | `docs/SECURITY.md` | MVP 2 |
| PROMPT INJECTION DEFENSE | `docs/SECURITY.md` | MVP 2 |
| MCP (MODEL CONTEXT PROTOCOL) | `backend/AGENT.md` | MVP 2 |
| RELIABILITY ENGINEERING | `docs/RELIABILITY.md` | MVP 2 |
| DIFA FRAMEWORK | `docs/RELIABILITY.md` | MVP 1 |
| REACT LOOP | `docs/RELIABILITY.md` | MVP 1 |
| DETERMINISTIC STRUCTURED OUTPUTS | `prompts/AGENT.md` | MVP 1.1 |
| OBSERVABILITY | `docs/OBSERVABILITY.md` | MVP 3 |
| PROMPT CACHING | `backend/AGENT.md` | MVP 2 |
| CLOUD-NATIVE ENGINEERING (Azure) | `infrastructure/AGENT.md` + `infrastructure/terraform/azure/` | MVP 2 |
| CLOUD-NATIVE ENGINEERING (AWS) | `infrastructure/AGENT.md` + `infrastructure/terraform/aws/` | MVP 2 |
| REAL-TIME ARCHITECTURE | `docs/REAL-TIME.md` | MVP 2 |
| FRONTEND DASHBOARD | `frontend/AGENT.md` | MVP 1 |
| ANALYTICS & USER TRACKING | `docs/ANALYTICS.md` | MVP 2 |
| ADTECH DOMAIN CONTEXT | `docs/ADTECH-CONTEXT.md` | MVP 2 |
| CI/CD | `infrastructure/AGENT.md` | MVP 1 |
| COVER LETTER PLAYBOOK | `backend/agents/cover-letter/AGENT.md` | MVP 2 |
| FINAL EXECUTION RULES | `docs/EXECUTION-RULES.md` | MVP 1 |
| WORKFLOW ORCHESTRATION RULES | `AGENT.md` (root) + `docs/EXECUTION-RULES.md` + `backend/agents/AGENT.md` | MVP 1 |
| Active task plan | `docs/tasks/todo.md` | MVP 1 |
| Self-improvement log | `docs/tasks/lessons.md` | MVP 1 |

---

## ROOT AGENT.md (INDEX ONLY)

The root `AGENT.md` becomes a lightweight index. Its only job is to tell any LLM or developer where each concern lives.

```markdown
# AGENT.md — Job Discovery Platform

## What this file is

This is the root index for the AI-Powered Job Discovery Platform.
All engineering standards, agent specs, and prompt rules live in
co-located AGENT.md files alongside the code they govern.

## Workflow Rules (read at every session start)

| Rule | Behaviour |
|---|---|
| Plan mode | Required for any task with 3+ steps or architectural decisions |
| Task log | Write plan to `docs/tasks/todo.md` before any implementation |
| Verify plan | Check in before starting — do not build on an unconfirmed plan |
| Subagents | Offload research, exploration, parallel analysis to subagents |
| Lessons review | Read `docs/tasks/lessons.md` at session start before touching code |
| Correction loop | After any user correction: update `docs/tasks/lessons.md` immediately |
| Done gate | Never mark complete without proving it works (tests, logs, diff) |
| Elegance check | For non-trivial changes: pause and ask "is there a more elegant way?" |
| Bug reports | Fix autonomously — point at logs/errors and resolve without hand-holding |
| Reference standards | Consult `docs/example-code/` for implementation examples and best practices before writing new code |

## Where to look

| Concern | File | MVP |
|---|---|---|
| Architecture and objectives | docs/ARCHITECTURE.md | MVP 1 |
| Engineering standards (FE/BE/DB) | frontend/AGENT.md, backend/AGENT.md | MVP 1 |
| Twelve-Factor compliance | docs/ENGINEERING-STANDARDS.md | MVP 1–3 |
| Structured JSON logger | backend/logging_config.py | MVP 1 |
| Env var validation | backend/settings.py | MVP 1 |
| asyncpg connection pool | backend/db.py | MVP 2 |
| Admin processes | backend/admin/ | MVP 1 |
| Alembic migrations | backend/migrations/ | MVP 2 |
| Security, OWASP, injection defense | docs/SECURITY.md | MVP 2–3 |
| Observability | docs/OBSERVABILITY.md | MVP 3 |
| Reliability, DIFA, ReAct | docs/RELIABILITY.md | MVP 1 |
| Real-time architecture | docs/REAL-TIME.md | MVP 2 |
| Analytics | docs/ANALYTICS.md | MVP 2 |
| Adtech domain context | docs/ADTECH-CONTEXT.md | MVP 2 |
| Final execution rules | docs/EXECUTION-RULES.md | MVP 1 |
| Active task plan | docs/tasks/todo.md | MVP 1 |
| Self-improvement log | docs/tasks/lessons.md | MVP 1 |
| Extensible scraper registry | backend/agents/base.py, backend/agents/registry.py | MVP 1 |
| Multi-agent rules (applies to all agents) | backend/agents/AGENT.md | MVP 1 |
| LinkedIn agent | backend/agents/linkedin/AGENT.md | MVP 1 |
| JobServe agent | backend/agents/jobserve/AGENT.md | MVP 1 |
| Ranking agent | backend/agents/ranking/AGENT.md | MVP 2 |
| RAG agent | backend/agents/rag/AGENT.md | MVP 2 |
| Cover letter agent | backend/agents/cover-letter/AGENT.md | MVP 2 |
| Question answer agent | backend/agents/question-answer/AGENT.md | MVP 2 |
| Security agent | backend/agents/security/AGENT.md | MVP 2 |
| Observability agent | backend/agents/observability/AGENT.md | MVP 3 |
| Orchestrator agent | backend/agents/orchestrator/AGENT.md | MVP 2 |
| Application assistant agent (optional) | backend/agents/application-assistant/AGENT.md | Optional |
| Interview prep agent (optional) | backend/agents/interview-prep/AGENT.md | Optional |
| Prompt engineering standards | prompts/AGENT.md | MVP 1.1 |
| All prompt files and versioning | prompts/ | MVP 1.1 |
| Infrastructure — Azure | infrastructure/terraform/azure/ | MVP 2 |
| Infrastructure — AWS | infrastructure/terraform/aws/ | MVP 2 |
| CI/CD | infrastructure/AGENT.md | MVP 1 |
| Docker multi-stage build | Dockerfile, nginx.conf, supervisord.conf | MVP 1 |
```

---

## DEPLOYMENT SPEC

### Strategy by MVP

| MVP | Deployment Model |
|---|---|
| MVP 1 | Single Docker container — Supervisor manages Nginx + FastAPI + Alembic migrate |
| MVP 2 | Azure Container Apps (primary) + AWS ECS Fargate (multi-cloud portability) |
| MVP 3 | Full distributed — separate containers per service; Temporal workers; Redis; observability stack |

### Process Start Order (Supervisor)

priority=1   migrate   → alembic upgrade head (exits on completion)
priority=10  nginx     → serves static export on port 80
priority=10  fastapi   → fastapi run on 127.0.0.1:8000

### Request Routing
Browser → port 80 → Nginx
/          → 127.0.0.1:3000 (Next.js Node server)
/api/v1/*  → 127.0.0.1:8000 (FastAPI)
/health    → 127.0.0.1:8000/health

### Dockerfile

```dockerfile
# ─── Stage 1: Build Next.js standalone ──────────────────────────────────────
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# ─── Stage 2: Backend runtime + Nginx + Node Server ─────────────────────
FROM python:3.14-slim AS runtime
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt-get update && apt-get install -y --no-install-recommends nginx supervisor nodejs npm && rm -rf /var/lib/apt/lists/*
WORKDIR /app/backend
COPY backend/pyproject.toml ./
RUN uv sync --no-dev
COPY backend/ .
RUN uv run playwright install chromium --with-deps
WORKDIR /app/frontend
COPY --from=frontend-builder /app/frontend/.next/standalone ./
COPY --from=frontend-builder /app/frontend/.next/static ./.next/static
COPY --from=frontend-builder /app/frontend/public ./public
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 80
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### nginx.conf

```nginx
events {}
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    server {
        listen 80;
        location / {
            proxy_pass         http://127.0.0.1:3000;
            proxy_http_version 1.1;
            proxy_set_header   Upgrade $http_upgrade;
            proxy_set_header   Connection 'upgrade';
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_cache_bypass $http_upgrade;
        }
        location /api/ {
            proxy_pass         http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_read_timeout 120s;
        }
        location /health {
            proxy_pass http://127.0.0.1:8000/health;
        }
    }
}
```

### supervisord.conf

```ini
[supervisord]
nodaemon=true

[program:migrate]
command=bash -c "[ -z \"$DATABASE_URL\" ] && echo 'DATABASE_URL not set, skipping migration' && exit 0; uv run alembic upgrade head"
directory=/app/backend
autostart=true
autorestart=false
startsecs=0
priority=1
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:nextjs]
command=node server.js
directory=/app/frontend
autostart=true
autorestart=true
priority=10
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
priority=10
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:fastapi]
command=uv run fastapi run main.py --host 127.0.0.1 --port 8000 --workers 2
directory=/app/backend
autostart=true
autorestart=true
priority=10
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
```

### docker-compose.yml (local dev)

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "80:80"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### .env.example

```bash
# Supabase (MVP 2+)
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=postgresql+asyncpg://...

# LLM providers
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
LITELLM_API_BASE=

# Redis (MVP 2+)
REDIS_URL=redis://localhost:6379

# Temporal (MVP 2+)
TEMPORAL_SERVER_URL=

# Observability (MVP 3)
OTEL_EXPORTER_OTLP_ENDPOINT=
SENTRY_DSN=

# Analytics (MVP 2+)
NEXT_PUBLIC_CLARITY_PROJECT_ID=

# API Gateway (MVP 2+)
KONG_ADMIN_URL=
KONG_PROXY_URL=

# Frontend
NEXT_PUBLIC_API_URL=/api/v1
SINGLE_USER_ID=00000000-0000-0000-0000-000000000000
```

---

## next.config.ts UPDATE REQUIRED

```typescript
import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
};
export default nextConfig;
```

`output: "standalone"` produces a self-contained Node.js server in `.next/standalone`. Supervisor starts it as `node server.js` on port 3000. Nginx proxies port 80 to it. All dynamic data is fetched client-side from FastAPI at `/api/v1/*`.

---

## BUILD AND RUN

```bash
# Build the single image
docker build -t job-discovery:latest .

# Run locally
docker-compose up

# Open in browser
http://localhost
```

---

## WHAT EACH FILE CONTAINS

### `docs/ARCHITECTURE.md` — MVP 1
System role definition, persona list, output requirements, primary objective, platform priorities.

### `docs/ENGINEERING-STANDARDS.md` — MVP 1–3
Frontend stack (Next.js 16, React 19, TypeScript, Tailwind, MUI, TanStack Query, Zustand, Zod).
Backend stack (Python 3.14, FastAPI, uv, Pydantic v2, SQLAlchemy 2, pgvector, Redis, LiteLLM, OpenTelemetry). Testing config includes `pytest-asyncio` with `asyncio_mode="auto"`.
Database stack (Supabase PostgreSQL, pgvector, RLS, partitioning, JSONB, WAL).
Full Twelve-Factor compliance notes (all 12 factors explicitly addressed).

### `docs/SECURITY.md` — MVP 2–3
Supabase Auth, JWT (`pyjwt[crypto]`), RBAC, RLS. OWASP Top 10 checklist. GPU-resistant hashing (`pwdlib[argon2]`). Redis token denylist. Prompt injection defense. Required protections.

### `docs/OBSERVABILITY.md` — MVP 3
OpenTelemetry, Grafana, Prometheus, Loki, Sentry. All tracked metrics: schema conformance, latency p50/p95, token usage, hallucination rate, retrieval quality, reranker confidence, agent failures.

### `docs/RELIABILITY.md` — MVP 1
Failure modes the system must handle. Circuit breakers, exponential backoff, dead-letter queues, jitter, idempotency. DIFA framework. ReAct loop pattern.

### `docs/REAL-TIME.md` — MVP 2
SSE, WebSockets, event-driven pipelines. Real-time update surfaces: AI scoring, job ingestion, notifications, cover letter status, workflow status.

### `docs/ANALYTICS.md` — MVP 2
Microsoft Clarity integration. Tracked signals: user journeys, rage clicks, session replay, UX bottlenecks.

### `docs/ADTECH-CONTEXT.md` — MVP 2
SSP/DSP ecosystem knowledge. Google Ad Manager, StackAdapt, The Trade Desk. Bid request timing context (~50–120ms). Application to recruiter intelligence and adtech job scoring.

### `docs/EXECUTION-RULES.md` — MVP 1
Final MUST and MUST NOT rules. Production-ready code requirements. No pseudo-code. No auto-apply. No fabricated metrics. No monolithic agents. No untyped APIs. Includes workflow execution rules: plan mode, task logging, verification gate, lessons review, correction loop, done gate, elegance check, bug fix autonomy.

### `docs/tasks/todo.md` — MVP 1
Active task plan with checkable items. Written before any implementation starts. Updated as steps complete. Reviewed at each session start.

### `docs/tasks/lessons.md` — MVP 1
Self-improvement log. Updated immediately after every user correction. Each entry documents the mistake pattern, root cause, and a rule to prevent recurrence.

### `frontend/app/admin/page.tsx` — MVP 2
Admin panel. Fetches GET /api/v1/admin/dlq and GET /api/v1/admin/schedule on mount. Renders AdminPanel.tsx. Retry button calls POST /api/v1/admin/dlq/{id}/retry. Discard button calls POST /api/v1/admin/dlq/{id}/discard. Pause/Resume buttons call POST /api/v1/admin/schedule/pause and /resume. Access linked from dashboard navigation (developer mode only — hidden behind feature flag feature_admin_panel).

### `frontend/app/recruiters/page.tsx` — MVP 2
Recruiter directory. Fetches GET /api/v1/recruiters. Renders RecruiterCard.tsx per recruiter. "Log interaction" button calls POST /api/v1/recruiters/{id}/interaction. Notes field calls PATCH /api/v1/recruiters/{id} on blur. Linked from dashboard navigation.

### `frontend/app/applications/page.tsx` — MVP 2
Application tracking board. Fetches GET /api/v1/applications. Renders ApplicationBoard.tsx grouping applications by status (draft, applied, awaiting_response, interviewing, offered, rejected, withdrawn). Linked from dashboard navigation.

### `frontend/components/ApplicationBoard.tsx` — MVP 2
Kanban-style columns, one per Application.status value. Each card shows job title, company, applied_at. Clicking a card navigates to /applications/{id}. Status transitions are triggered by PATCH /api/v1/applications/{id}.

### `frontend/app/saved/page.tsx` — MVP 1
Renders SavedJobsList.tsx. Fetches GET /api/v1/jobs/saved.

`SavedJobsList.tsx` handles three render states:
- **Loading:** render a skeleton list of 3 placeholder cards.
- **Empty (zero saved jobs):** render an empty state with the message: `"No saved jobs yet. Browse the job feed and save roles you're interested in."` Include a link/button labelled `"Browse jobs"` that navigates to `/` (the dashboard/job feed).
- **Populated:** render one `JobCard.tsx` per saved job, same as the main feed. Linked from the dashboard navigation.

### `frontend/app/jobs/[id]/page.tsx` — MVP 2
Job detail page. Fetches GET /api/v1/jobs/{id}. Renders job description, a Save/Unsave toggle button (calls POST or DELETE /api/v1/jobs/{id}/save, uses useOptimistic for instant feedback).

A "Generate cover letter" button. This button is disabled unless `embedding_status = ready`. On mount the page calls `GET /api/v1/cv/status` using the same TanStack Query key `['cv-status']` used by `CVUploadPanel.tsx`. If the status is not `ready`, the button renders greyed. In MVP1: when `embedding_status = pending`, the button renders greyed with tooltip: "Cover letter generation is available from MVP2. CV embedding is not yet active." In MVP2+: when `embedding_status` is `pending` or `processing`, keep the existing tooltip: "Upload and process your CV to enable cover letter generation." When enabled and clicked, calls `POST /api/v1/cover-letter/{job_id}`, then renders `CoverLetterViewer.tsx`.

A "Generate interview prep" button. Disabled in MVP1 and MVP2. Enabled only when the feature flag `feature_interview_prep` evaluates to `true`. Flag evaluation happens server-side: the page fetches `GET /api/v1/feature-flags` on mount (returns a JSON object of flag name to boolean). When the flag is `false`, the button renders greyed with the label "Interview Prep — Available from MVP3" and no click handler is attached. When the flag is `true`, clicking calls `POST /api/v1/interview-prep/{job_id}`. The component maintains a local state variable: `const [interviewPrepBlocked, setInterviewPrepBlocked] = useState(false)`.

On mount, `GET /api/v1/feature-flags` is fetched. If `feature_interview_prep` is `false`, the button renders disabled — `interviewPrepBlocked` is not used in this case; the flag result is the authoritative source.

If the flag is `true`, the button is enabled. On click, calls `POST /api/v1/interview-prep/{job_id}`. If the response is 503, the handler calls `setInterviewPrepBlocked(true)` and shows a toast: `"Interview prep is not yet available."` The button renders disabled for the remainder of the session.

On page refresh, `GET /api/v1/feature-flags` is re-fetched and is again authoritative. `interviewPrepBlocked` is not persisted — it resets to `false` on mount. This means a 503 disables the button for the current session only; the flag controls the permanent state.

A "Log application" button. The component maintains a local state variable: `const [existingApplicationId, setExistingApplicationId] = useState<string | null>(null)`.

The `onClick` handler calls `POST /api/v1/applications`. On 409, it reads `response.json()` to extract `existing_id` and calls `setExistingApplicationId(existing_id)`.

Render logic:
- If `existingApplicationId` is null: render button labelled "Log application" with the POST handler.
- If `existingApplicationId` is set: render button labelled "View application" with `onClick={() => router.push('/applications/' + existingApplicationId)}`. No POST call is made.

### `frontend/app/onboarding/page.tsx` — MVP 1
Renders ProfileForm.tsx then CVUploadPanel.tsx in sequence. On ProfileForm submit, calls POST /api/v1/profile. The `onSubmit` handler passed to `ProfileForm.tsx` from `/onboarding/page.tsx` must, on successful `POST /api/v1/profile` response, call `queryClient.invalidateQueries(['profile'])`. This causes `OnboardingBanner.tsx` — which shares the `['profile']` query key — to re-fetch and re-render without a page reload, transitioning from the "Complete your profile" state to the "Upload your CV" state automatically. On CV upload, calls POST /api/v1/cv. After upload, polls GET /api/v1/cv/status every 5 seconds using useEffect + useState until embedding_status = ready or the MVP1 stub message applies. On ready, redirects to /.

### `frontend/app/profile/page.tsx` — MVP 1
Renders ProfileForm.tsx pre-populated from GET /api/v1/profile. Renders CVUploadPanel.tsx showing current CV filename and re-upload option.
On mount, calls `GET /api/v1/profile`. If the response is 404, passes a `POST` handler to `ProfileForm.tsx`. If the response is 200, passes a `PATCH /api/v1/profile` handler. The form does not know which verb is in use. Once the profile is saved successfully, the banner hides and the page transitions to edit mode.

### `frontend/components/OnboardingBanner.tsx` — MVP 1
**Query key contract:** `OnboardingBanner.tsx` uses query key `['profile']` for the profile fetch and `['cv-status']` for the CV status fetch. Any component or page that mutates profile or CV data **must** invalidate the corresponding query key on success. This is the mechanism by which the banner updates without a page reload.

### `frontend/components/JobCard.tsx` — MVP 1
Renders a single job listing. Displays title, company, source badge, salary range, and created_at. Contains a Save toggle button: saved state is tracked in local component state initialised from the job's saved property. On toggle: calls POST /api/v1/jobs/{id}/save (to save) or DELETE /api/v1/jobs/{id}/save (to unsave) using useOptimistic for instant UI feedback before the server confirms. On click of the card title, navigates to /jobs/{id}.

### `frontend/components/CoverLetterViewer.tsx` — MVP 2
Renders the cover letter for a given job_id. On mount, calls GET /api/v1/cover-letter/{job_id}. If status = pending or generating, polls every 3 seconds using TanStack Query refetchInterval until status = ready. When ready, renders the cover letter content as formatted text. Two download buttons: "Download PDF" and "Download Markdown". These do NOT use TanStack Query. Each button has an `onClick` handler that calls `fetch('/api/v1/cover-letter/{job_id}/export?format=pdf|markdown')`, reads the response as a `Blob`, creates an object URL via `URL.createObjectURL(blob)`, programmatically clicks a hidden `<a download="cover-letter.pdf|md">` element, then revokes the object URL. On a non-2xx response from the export endpoint:
- If the response is 422: show a toast — `"Cover letter is no longer available. Please regenerate it."` — and do NOT offer a retry. Also call `queryClient.invalidateQueries(['cover-letter', job_id])` to force `CoverLetterViewer.tsx` to re-poll status and re-render based on the actual current state.
- For any other error (network failure, 500): show a toast — `"Download failed. Please try again."` — and restore the button to its normal state (no spinner).

### `frontend/components/ProfileForm.tsx` — MVP 1
`ProfileForm.tsx` accepts an `onSubmit: (data: ProfileFormData) => Promise<void>` prop. The component itself never calls an API directly. The parent page (`/onboarding/page.tsx` or `/profile/page.tsx`) is responsible for passing the correct handler — `POST` from onboarding, `POST` or `PATCH` from profile depending on whether a `UserProfile` record exists. This keeps the component reusable and the verb decision co-located with the page that owns the routing logic.

### `frontend/AGENT.md` — MVP 1
Frontend stack spec. Dashboard feature list: AI relevance scoring, RAG insights, recruiter intelligence, cover letter generation, observability dashboards, token usage dashboards, agent traces, prompt debugging, saved jobs, filtering, dark/light mode.

### `backend/AGENT.md` — MVP 1
Backend stack spec. API design standards: typed request/response objects, OpenAPI specs, schema-first design, Pydantic v2, versioned routes (`/api/v1/`), cursor-based pagination, RFC 7807 structured errors, connection pooling. Domain-driven folder layout. MCP integration rules. Prompt caching strategy.

### `backend/logging_config.py` — MVP 1
Shared structured JSON logger (`get_logger(name)`) using `structlog` and `dict_tracebacks`. Twelve-Factor XI compliance. All agents and routers import from this module — no `print()` calls anywhere.

### `backend/settings.py` — MVP 1
Pydantic `BaseSettings` class. All environment variables typed and validated at startup using types like `PostgresDsn`. Fails fast if any required var is missing.

### `backend/routers/scrape.py` — MVP 1
Scrape trigger endpoint. MVP1: uses asyncio.Lock for in-process concurrency guard. MVP2: replaced with Redis distributed lock (redis.lock("scrape:global", timeout=3600)).

### `backend/db.py` — MVP 2
asyncpg connection pool configuration: `pool_size=10`, `max_overflow=20`, `pool_timeout=30`, `pool_recycle=1800`, `pool_pre_ping=True`. Tuned to uvicorn worker count.

### `backend/admin/` — MVP 1+
One-off admin process scripts (Twelve-Factor XII). All tracked in version control. Run as isolated processes in the same Docker image: `seed_keywords.py`, `replay_dlq.py`, `clear_db.py` (dev only), `run_evals.py`.

### `backend/migrations/` — MVP 2
Alembic migration history. `env.py`, `alembic.ini`, versioned migration files. Migration runs automatically via Supervisor `priority=1` before uvicorn starts.

### `backend/agents/base.py` — MVP 1
`BaseScrapeAgent` abstract base class. Defines `source_id`, `display_name`, and `run()` interface. All scraper agents extend this — no exceptions.

### `backend/agents/registry.py` — MVP 1
`@register` decorator and `get_all_agents()` / `get_agent(source_id)` functions. Orchestrator uses `get_all_agents()` — no hardcoded source names anywhere.

### `backend/agents/AGENT.md` — MVP 1
Cross-agent rules: no monoliths, isolated specialised agents, DIFA compliance required, ReAct loop required, OWASP validation required, all agents extend `BaseScrapeAgent` or appropriate base, all import `get_logger`. Includes subagent execution rules: one task per subagent, offload strategy, context window discipline, result summarisation, escalation on failure.

### `backend/agents/linkedin/AGENT.md` — MVP 1
LinkedIn scraping responsibilities. Anti-bot strategy. Search keywords. Execution interval (every 3–5 hours). Randomisation rules. Retry handling. Deduplication. Data normalisation. `source_id = "linkedin"`.

### `backend/agents/jobserve/AGENT.md` — MVP 1
JobServe scraping responsibilities. Randomised search patterns. Pagination randomisation. Data normalisation. Anti-detection rules. `source_id = "jobserve"`.

### `backend/agents/ranking/AGENT.md` — MVP 2
Similarity scoring. Reranking with `cross-encoder/ms-marco-MiniLM-L-6-v2`. Embedding models (BAAI/bge-large-en-v1.5, all-mpnet-base-v2). Full 8-step scoring pipeline. Storage thresholds (similarity >= 75%, reranker confidence >= threshold). Async execution via Temporal.

### `backend/agents/rag/AGENT.md` — MVP 2
Contextual retrieval, semantic memory, CV enrichment, personalised recommendations. Retrieval sources: CV, applications, recruiter messages, saved jobs, preferences, skill graph. Evaluation metrics: Ragas (retrieval precision, context recall), DeepEval (faithfulness, relevance).

### `backend/agents/cover-letter/AGENT.md` — MVP 2
Cover letter generation responsibilities. Recruiter outreach. Tone adaptation. ATS optimisation. Cover letter playbook: role summary, matching skills, quantified achievements, AI narrative, ATS keywords, recruiter-focused language. ATS keyword match >= 60% enforced.

### `backend/agents/question-answer/AGENT.md` — MVP 2
RAG-powered Q&A on specific job listings. Answers technical or cultural questions grounded in job descriptions, company metadata, and user's professional background.

### `backend/agents/security/AGENT.md` — MVP 2
Prompt injection detection. OWASP validation. Schema validation. Payload sanitisation. RBAC enforcement. Instruction hierarchy enforcement. Context isolation. Allowlisted tools. HTML and markdown sanitisation. Audit logging.

### `backend/agents/observability/AGENT.md` — MVP 3
Tracing. Latency monitoring. Token usage monitoring. Hallucination monitoring. AI reliability metrics. Links to `docs/OBSERVABILITY.md` for the full metric list.

### `backend/agents/orchestrator/AGENT.md` — MVP 2
Orchestration rules. Retry logic (exponential backoff, jitter). Dead-letter queues. Workflow coordination via Temporal. Async execution. Checkpoint recovery. Event replay. Idempotency enforcement.

### `backend/agents/application-assistant/AGENT.md` — Optional (post-MVP 3)
Full spec from the optional Application Assistant Agent: trigger syntax, responsibilities, safety rules (NEVER auto-submit, NEVER bypass CAPTCHA, ALWAYS require manual review), recommended technologies (Playwright, Browserbase, Puppeteer, MCP browser tools, Temporal).

### `backend/agents/interview-prep/AGENT.md` — Optional (post-MVP 3)
Full spec from the optional Interview Preparation Agent: trigger syntax, responsibilities, RAG context sources (job description, company blogs, recruiter profile, CV, historical interviews, GitHub repositories, tech stack signals), AI output requirements, recommended technologies. Orchestration dependency: before generating the prep pack, the agent checks for an existing CompanyResearch record. If absent or older than 7 days, it triggers POST /api/v1/company-research/{company_name} synchronously within the Temporal workflow before proceeding.

### `prompts/AGENT.md` — MVP 1.1
Multi-agent prompt structure rules. Prompt versioning (semver). CONTRACT.md and CHANGELOG.md requirements. Full AI Prompt Engineering Standards section: system prompt XML structure (`<role>`, `<context>`, `<instructions>`, `<constraints>`, `<output_format>`, `<example>`), reasoning effort calibration per agent, OpenAI and Claude guidance, few-shot example requirements, prompt authoring rules, anti-patterns list.

### `infrastructure/AGENT.md` — MVP 1–2
Cloud-native stack: Docker, Supervisor, Nginx, Terraform, Helm, GitHub Actions. Deployment targets: Azure Container Apps (`infrastructure/terraform/azure/`), AWS ECS Fargate (`infrastructure/terraform/aws/`). CI/CD pipeline steps: linting, type checking, testing, security scanning (Trivy, Bandit), Docker builds, Terraform validate + plan, prompt regression tests (DeepEval), Ragas retrieval eval, integration tests.

---

## PROMPT CONTRACT.md TEMPLATE

Every agent under `prompts/` MUST include a `CONTRACT.md` with this structure:

```markdown
# CONTRACT.md — {Agent Name}

## Target Model
Claude Sonnet 4.6 / GPT-5.x  (update per agent)

## Model Version Pinned
claude-sonnet-4-6 / gpt-5.5-2025-xx-xx

## Reasoning Effort
xhigh  (update per task shape — see prompts/AGENT.md)

## Max Output Tokens
16000  (update per agent — agentic runs start at 64k)

## Temperature
0  (all structured outputs — no exceptions without documentation)

## Permitted Tools
- list every tool by name
- no open-ended tool access

## Expected Token Budget
~XXXX tokens per invocation  (measure and document)

## Eval Set Reference
evals/{agent-name}/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set
Breaking changes increment the major version

## Last Regression Run
YYYY-MM-DD — all evals passed
```

## Working documentation

All documents for planning and executing this project will be in the docs/ directory.
Please review the docs/PLAN.md document before proceeding.