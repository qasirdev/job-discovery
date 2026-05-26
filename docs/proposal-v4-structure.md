# PROJECT-STRUCTURE.md

# AI-Powered Job Discovery Platform — Proposed Multi-File Project Structure

**Proposal Version:** 1.5.0 (based on `004-01-saas-job-search-proposal-v4.md`)
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
| **MVP 2** | Supabase PostgreSQL + pgvector, Alembic migrations, AI ranking pipeline, Terraform (~> 1.15.4, AzureRM ~> 4.74.0, AWS ~> 5.0) (Azure Container Apps + AWS ECS Fargate), OWASP middleware, observability stack, circuit breakers, connection pool tuning, Docker image signing, Proxy abstraction layer, Residential proxy support, Serverless AI ranking support |
| **MVP 3** | Full Twelve-Factor compliance, OpenTelemetry, Grafana, Prometheus, Loki, Sentry, RBAC, RLS, JWT auth, structured admin process tooling |
| **MVP 4** | Application Workflow and Interview Preparation |
| **MVP 5** | Security Hardening and Production Polish |

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

## CRITICAL REFERENCES

- **MUI Box Docs:** [https://mui.com/material-ui/react-box/](https://mui.com/material-ui/react-box/)
- **MUI Theme Provider Docs:** [https://mui.com/material-ui/customization/theming/](https://mui.com/material-ui/customization/theming/)
- **Microsoft Entra ID Docs:** [https://learn.microsoft.com/en-us/entra/identity/](https://learn.microsoft.com/en-us/entra/identity/)
- **Google Cloud Identity and OAuth Docs:** [https://cloud.google.com/identity/docs](https://cloud.google.com/identity/docs)
- **OpenAI Prompt Guidance:** [https://platform.openai.com/docs/guides/prompt-engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- **Claude Prompt Engineering Best Practices:** [https://docs.anthropic.com/claude/docs/prompt-engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- **Competitive References:** autoapplier.com, lazyapply.com, simplify.jobs
- **OWASP GenAI Security Project:** https://genai.owasp.org/
- **OWASP Top 10 for LLM Applications:** https://genai.owasp.org/llm-top-10/
- **OWASP Top 10 for Large Language Model Applications (Project Repo):** https://owasp.org/www-project-top-10-for-large-language-model-applications/
- **OWASP Top 10 for Agentic Applications:** https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

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
├── .github/
│   └── workflows/
│       └── ci.yml                         # MVP 1: GitHub Actions CI skeleton
│
├── scripts/
│   ├── start-server-mac.sh                # Local LLM Runtime support script for Mac
│   ├── start-server-pc.bat                # Local LLM Runtime support script for PC
│   ├── start-server-linux.sh              # Local LLM Runtime support script for Linux
│   ├── stop-server-mac.sh                 # Stop script for Mac
│   ├── stop-server-pc.bat                 # Stop script for PC
│   └── stop-server-linux.sh               # Stop script for Linux
│
├── docs/                                  # Cross-cutting documentation
│   ├── jira-tickets/
│   │   ├── jd-mvp1.5.csv
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
│   ├── EXECUTION-RULES.md                 # ← from: FINAL EXECUTION RULES; includes workflow MUST/MUST NOT section
│   ├── FEATURE-FLAGS.md                   # ← Feature Flag Strategy
│   ├── SCRAPING-RATE-LIMITS.md            # ← Outbound Scraping Rate Limiting Strategy
│   ├── ANTI-BOT.md                        # ← Anti-Bot, Proxy, and Fingerprinting Disclaimer
│   └── DATA-OWNERSHIP.md                  # ← Data Ownership and Portability
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
├── backend/                               # Python 3.14 + FastAPI + uv
│   ├── AGENT.md                           # ← from: BACKEND STACK + API DESIGN STANDARDS + MCP + PROMPT CACHING
│   ├── pyproject.toml
│   ├── main.py                            # MVP 1: app entrypoint + agent auto-discovery imports
│   ├── models/                            # MVP 1: SQLAlchemy models; MVP 2+: full domain models
│   │   ├── DOMAIN-MODELS.md               # Domain Model Definitions (UserProfile, SavedJob, InteractionEvent, CompanyResearch, etc.)
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
│   │   │   ├── AGENT.md                   # ← from: RAG Agent + RAG PERSONALIZATION
│   │   │   └── rag_agent.py
│   │   │
│   │   ├── cover-letter/                  # MVP 2
│   │   │   ├── AGENT.md                   # ← from: Cover Letter Agent + COVER LETTER PLAYBOOK
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
│   │       ├── AGENT.md                   # ← from: Interview Preparation Intelligence Agent
│   │       └── interview_agent.py
│   │
│   ├── migrations/                        # MVP 2: Alembic migrations (Twelve-Factor XII)
│   │   ├── env.py
│   │   ├── alembic.ini
│   │   └── versions/
│   │
│   └── routers/                           # MVP 1: Domain-driven API routes (formerly api/v1/)
│       ├── v1/
│       │   ├── jobs.py                    # MVP 1: GET /api/v1/jobs, GET /api/v1/jobs/{id}
│       │   ├── scrape.py                  # MVP 1: POST /api/v1/scrape (registry-driven)
│       │   ├── cover_letter.py            # MVP 2: POST /api/v1/cover-letter/{job_id}
│       │   ├── question_answer.py         # MVP 2: POST /api/v1/question-answer/{job_id}
│       │   ├── interview.py               # MVP 2+: POST /api/v1/interview-prep/{job_id}
│       │   ├── profile.py                 # MVP 1: GET, POST, PATCH /api/v1/profile
│       │   ├── cv.py                      # MVP 1: GET, POST /api/v1/cv
│       │   ├── recruiters.py              # MVP 2: GET, POST, PATCH /api/v1/recruiters
│       │   ├── applications.py            # MVP 2: GET, POST, PATCH /api/v1/applications
│       │   ├── company_research.py        # MVP 2: GET /api/v1/company-research
│       │   └── admin.py                   # MVP 2: GET, POST /api/v1/admin
│       └── dependencies.py                # MVP 1.1+: require_rag_ready FastAPI dependency
│
├── prompts/                               # MVP 1.1: All LLM prompt files — versioned by agent
│   ├── AGENT.md                           # ← from: MULTI-AGENT PROMPT STRUCTURE + PROMPT VERSIONING + AI PROMPT ENGINEERING STANDARDS
│   │
│   ├── linkedin-agent/                    # MVP 1.1
│   │   ├── CONTRACT.md
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
│   │   ├── guardrails.md
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
└── infrastructure/                        # Cloud-native deployment
    ├── AGENT.md                           # ← from: CLOUD-NATIVE ENGINEERING + CI/CD
    ├── DISASTER-RECOVERY.md               # ← Disaster Recovery and Backup Restore
    ├── LOCAL-LLM.md                       # ← Local LLM Runtime Support
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

## RATE LIMITING STRATEGY

Per-endpoint rate limits are enforced at the API Gateway level (or via middleware) as follows:

| Endpoint | Method | Rate Limit |
|---|---|---|
| `/api/v1/jobs` | GET | 300 req/min |
| `/api/v1/cover-letter/*` | POST | 20 req/min |
| `/api/v1/question-answer/*` | POST | 30 req/min |
| `/api/v1/interview-prep/*` | POST | 10 req/min |
| `/api/v1/scrape` | POST | 1 concurrent globally |
| General API usage | ANY | 600 req/min |

---

## WHAT EACH FILE CONTAINS

### `docs/ARCHITECTURE.md` — MVP 1
Contains: Full executive summary, Full problem statement, Full objectives section, System role definition, persona list, output requirements, primary objective, platform priorities.
Explicit out-of-scope exclusions, including SaaS mode and Mobile native applications.

### `docs/ENGINEERING-STANDARDS.md` — MVP 1–3
Contains: Full technology stack matrices.
Detailed database requirements (RLS, WAL backups, UUIDs, JSONB, partitioning, audit logging).
Frontend stack (Next.js 16, React 19 hooks explicitly named: `use`, `useTransition`, `useOptimistic`, `useActionState`, TypeScript, Tailwind, MUI, TanStack Query, Zustand, Zod).
Backend stack (Python 3.14, FastAPI, uv, Pydantic v2, SQLAlchemy 2, pgvector, Redis, LiteLLM, OpenTelemetry). Testing config includes `pytest-asyncio` with `asyncio_mode="auto"`.
Database stack (Supabase PostgreSQL, pgvector, RLS, partitioning, JSONB, WAL).
Detailed Twelve-Factor implementation explanations (Factors I–XII) including full Twelve-Factor compliance notes.
Factor IX (Disposability) implementation details explicitly defined: uvicorn draining, Temporal checkpointing, Playwright SIGTERM handler, Supervisor `stopwaitsecs=30`.
Explicit process model separation (uvicorn / Temporal / Redis).
Deployment parity guarantees (`uv sync`, `npm ci`, same Docker image).
Runtime secret injection strategy.

### `docs/FEATURE-FLAGS.md` — MVP 2
Contains: Feature Flag Strategy (Full feature flag strategy items/subsections), OpenFeature-compatible provider recommendation, LaunchDarkly integration (optional), Database-backed feature flag table for self-hosted mode, Internal-only rollout strategy, Percentage rollout strategy, Per-user rollout strategy, Canary deployment validation, Emergency kill-switch support.

### `docs/SCRAPING-RATE-LIMITS.md` — MVP 2
Contains: Full outbound scraping rate limiting strategy details, Per-domain concurrency controls, Request pacing with randomised delay, Retry policy with exponential backoff and jitter, Failure threshold / circuit breaker, Session rotation, Adaptive throttling (CAPTCHA frequency, 429 responses, DOM stability, latency spikes), Queue management via Temporal (concurrency caps, retry ceilings, DLQ routing, priority scheduling).

### `docs/ANTI-BOT.md` — MVP 1
Contains: Full anti-bot, proxy, and fingerprinting disclaimer details, Respect robots.txt constraint, No CAPTCHA solving / bypassing rule, No authenticated LinkedIn scraping rule, Browser fingerprinting strategy (user-agent rotation, viewport randomisation, context isolation, proxy abstraction, residential proxy support), Compliance disclaimer / Terms of Service note.

### `docs/DATA-OWNERSHIP.md` — MVP 3
Contains: Full data ownership and portability details, Export capabilities per resource (Exact export formats: PDF / DOCX for CVs, JSON / CSV for Applications, Markdown / PDF for Cover Letters, Markdown / PDF for Interview Packs, JSON for Recruiter Interactions), Deletion capabilities and exact propagation targets (PostgreSQL records, pgvector embeddings, Redis caches, object storage, observability metadata), GDPR compliance requirements (right to export, deletion, consent withdrawal, retention policies, audit logging).

### `infrastructure/DISASTER-RECOVERY.md` — MVP 3
Contains: Full disaster recovery and backup restore details, RPO <= 15 minutes / RTO <= 1 hour targets, Backup strategy per component (PostgreSQL, Redis, Terraform state, Docker images, prompts), Restore workflow (7 steps), DR validation (quarterly drills, automated recovery validation, consistency checks, runbooks).

### `infrastructure/LOCAL-LLM.md` — MVP 2
Contains: Full local LLM runtime support details, llama.cpp-compatible runtime support with GGUF quantized models, KV cache reuse, GPU acceleration, OpenAI-compatible local inference APIs, OpenRouter integration with OPENROUTER_API_KEY, openai/gpt-oss-120b model specification, Start/Stop server scripts for Mac, PC, Linux in scripts/, Hybrid local/cloud routing via LiteLLM. Privacy-friendly processing and offline-capable AI workflows. Use "uv" as the package manager for python in the Docker container, and everything packaged into a Docker container.

### `docs/SECURITY.md` — MVP 2–3
Contains: Supabase Auth, JWT (`pyjwt[crypto]`), RBAC, RLS. OWASP Top 10 checklist. GPU-resistant hashing (`pwdlib[argon2]`). Redis token denylist.
`SINGLE_USER_ID` temporary single-user bridge strategy.
Prompt Injection Defence exact mitigation techniques: instruction hierarchy enforcement, schema validation, context isolation, allowlisted tools only, HTML and markdown sanitisation, output validation before storage.
Detailed Mitigations:
- Cryptographic Failures: Encrypted secrets via Azure Key Vault, TLS enforced.
- SSRF (Allowlisted external domains only for all agent outbound calls)
- Software Integrity Failures (Docker image signing in CI via GitHub Actions)
- Insecure Design (Security Agent reviews all agent outputs before storage)
Exact CI security scanning tools listed: Trivy for images, Bandit for Python.

### `docs/OBSERVABILITY.md` — MVP 3
Contains: Full observability strategy details.
Loki stdout log aggregation strategy.
OpenTelemetry, Grafana, Prometheus, Loki, Sentry. 
Exact Observability Metrics Targets: "Schema conformance rate >= 99%", "HTTP latency p50 < 500ms", "HTTP latency p95 < 2s", "Agent execution latency p95 < 8s", "Hallucination rate alert > 1%", "Retrieval precision >= 0.80."

### `docs/RELIABILITY.md` — MVP 1
Contains: Full reliability engineering details.
DIFA framework exact phases: Discover, Interpret, Filter, Act.
ReAct loop exact phases: Reason, Act, Observe, Repeat, Answer.
Exact URL idempotency rule: Job id = SHA-256 of URL.
Temporal worker checkpoint recovery behavior.
Failure modes the system must handle.
Circuit breakers exact rule: opens after 3 consecutive failures.
Exponential backoff exact configuration values: Base 1s, max 60s, jitter enabled.

### `docs/REAL-TIME.md` — MVP 2
Contains: SSE, WebSockets, event-driven pipelines. Real-time update surfaces: AI scoring, job ingestion, notifications, cover letter status, workflow status.

### `docs/ANALYTICS.md` — MVP 2
Contains: Full analytics and user tracking details.
Microsoft Clarity integration. Tracked signals: user journeys, rage clicks, session replay, UX bottlenecks.

### `docs/ADTECH-CONTEXT.md` — MVP 2
Contains: Full adtech domain context details.
SSP/DSP ecosystem knowledge. Google Ad Manager, StackAdapt, The Trade Desk. Bid request timing context (~50–120ms). Application to recruiter intelligence and adtech job scoring.

### `docs/EXECUTION-RULES.md` — MVP 1
Contains: Final MUST and MUST NOT rules. Production-ready code requirements. No pseudo-code. No auto-apply. No fabricated metrics. No monolithic agents. No untyped APIs. Includes workflow execution rules: plan mode, task logging, verification gate.
Detailed workflow orchestration rules: “Elegance check” workflow rule, “Done gate” workflow rule, “Correction loop” workflow rule, “Lessons review” workflow rule, “Subagents” workflow rule, “Reference standards” workflow rule.
Production-grade 2026 engineering practices references.
Official documentation reference requirements.

### `docs/tasks/todo.md` — MVP 1
Contains: Tasks folder workflow-management rationale. Active task plan with checkable items. Written before any implementation starts. Updated as steps complete. Reviewed at each session start.

### `docs/tasks/lessons.md` — MVP 1
Contains: Self-improvement log. Updated immediately after every user correction. Each entry documents the mistake pattern, root cause, and a rule to prevent recurrence.

### `config/relevance_profile.yaml` — MVP 1.1
Contains: Prompt-based relevance filtering base config.

### `frontend/app/admin/page.tsx` — MVP 2
Contains: Admin panel. Fetches GET /api/v1/admin/dlq and GET /api/v1/admin/schedule on mount. Renders AdminPanel.tsx. Retry button calls POST /api/v1/admin/dlq/{id}/retry. Discard button calls POST /api/v1/admin/dlq/{id}/discard. Pause/Resume buttons call POST /api/v1/admin/schedule/pause and /resume. Access linked from dashboard navigation (developer mode only — hidden behind feature flag feature_admin_panel).
Detailed frontend component responsibilities (AdminPanel.tsx).

### `frontend/app/recruiters/page.tsx` — MVP 2
Contains: Recruiter directory. Fetches GET /api/v1/recruiters. Renders RecruiterCard.tsx per recruiter. "Log interaction" button calls POST /api/v1/recruiters/{id}/interaction. Notes field calls PATCH /api/v1/recruiters/{id} on blur. Linked from dashboard navigation.
Detailed frontend component responsibilities (RecruiterCard.tsx).

### `frontend/app/applications/page.tsx` — MVP 2
Contains: Application tracking board. Fetches GET /api/v1/applications. Renders ApplicationBoard.tsx grouping applications by status (draft, applied, awaiting_response, interviewing, offered, rejected, withdrawn). Linked from dashboard navigation.
Exact Application component click stream: POST `/api/v1/applications` → 409 conflict → sets `existingApplicationId` state → swaps "Log application" button to "View application".

### `frontend/components/ApplicationBoard.tsx` — MVP 2
Contains: Kanban-style columns, one per Application.status value. Each card shows job title, company, applied_at. Clicking a card navigates to /applications/{id}. Status transitions are triggered by PATCH /api/v1/applications/{id}.
Detailed frontend component responsibilities (ApplicationBoard.tsx).

### `frontend/app/saved/page.tsx` — MVP 1
Contains: Renders SavedJobsList.tsx. Fetches GET /api/v1/jobs/saved.
`SavedJobsList.tsx` loading / empty / populated render states:
- **Loading:** render a skeleton list of 3 placeholder cards.
- **Empty (zero saved jobs):** render an empty state with the message.
- **Populated:** render one `JobCard.tsx` per saved job.

### `frontend/app/jobs/[id]/page.tsx` — MVP 2
Contains: Job detail page. Fetches GET /api/v1/jobs/{id}. Renders job description.
`GET /api/v1/feature-flags` endpoint behavior and env-driven static flag model logic.
Explicit frontend gating logic: disable the Cover Letter and Interview Prep buttons on the dashboard and display `OnboardingBanner.tsx` with a prompt to complete setup first.
Exact Interview Prep click stream and fallback states: checks `CompanyResearch` using `company_slug`, logic for missing company slug rendering a `{"status": "skipped"}` collapsible section.
Interview Prep endpoint exact UI session state logic: `setInterviewPrepBlocked(true)` on 503, disabling the button for the session only and resetting on page refresh.

### `frontend/app/onboarding/page.tsx` — MVP 1
Contains: Renders ProfileForm.tsx then CVUploadPanel.tsx in sequence.
Onboarding state gating logic using `embedding_status` and `OnboardingBanner.tsx`.
`queryClient.invalidateQueries(['profile'])` onboarding refresh flow.
On ProfileForm submit, calls POST /api/v1/profile. On CV upload, calls POST /api/v1/cv. After upload, polls GET /api/v1/cv/status every 5 seconds until embedding_status = ready. On ready, redirects to /.
**Exact 5-step Onboarding Sequence table and completion signals:** (1) Profile submission → `UserProfile` row exists. (2) CV upload → `CV` row created, `embedding_status = pending`. (3) Pipeline processes → `embedding_status` transitions. (4) System confirms readiness → `{ "embedding_status": "ready" }`. (5) Features unlock → Banner hides.

### `frontend/app/profile/page.tsx` — MVP 1
Contains: Renders ProfileForm.tsx pre-populated from GET /api/v1/profile. Renders CVUploadPanel.tsx showing current CV filename and re-upload option.
`ProfileForm.tsx` reusable `onSubmit` contract and POST/PATCH ownership rules.

### `frontend/components/OnboardingBanner.tsx` — MVP 1
Contains: **Query key contract:** `OnboardingBanner.tsx` uses query key `['profile']` for the profile fetch and `['cv-status']` for the CV status fetch. Onboarding state gating logic using `embedding_status` and `OnboardingBanner.tsx` states.
**Exact 5 states of the OnboardingBanner.tsx component:** 
1. Profile missing ("Complete your profile")
2. CV not uploaded ("Upload your CV")
3. Embedding pending ("CV uploaded — embedding available from MVP2")
4. Embedding processing ("Processing your CV — this takes about 30 seconds")
5. Ready (Banner hidden)

### `frontend/components/JobCard.tsx` — MVP 1
Contains: Renders a single job listing. Displays title, company, source badge, salary range, and created_at.
`useOptimistic` save-unsave JobCard behavior: saved state is tracked in local component state initialised from the job's saved property.

### `frontend/components/CoverLetterViewer.tsx` — MVP 2
Contains: Renders the cover letter for a given job_id.
Cover letter export exact fallback handling: "do NOT offer a retry" on 422, and "show a toast 'Download failed' and restore button state" on generic 500 network errors. On a 422 response during export, triggers a toast ("Cover letter is no longer available") and calls `queryClient.invalidateQueries(['cover-letter', job_id])`.

### `frontend/components/ProfileForm.tsx` — MVP 1
Contains: `ProfileForm.tsx` reusable `onSubmit` contract and POST/PATCH ownership rules. Accepts an `onSubmit` prop. The component itself never calls an API directly.

### `frontend/AGENT.md` — MVP 1
Contains: Frontend stack spec. Dashboard feature list.
Dynamic source rendering in frontend dashboard.
Dynamic frontend rendering of scrape source counts.

### `backend/AGENT.md` — MVP 1
Contains: Backend stack spec. Full scalable API design section.
API Versioning exact lifecycle policy: `/api/v1/` remains supported for a minimum of 6 months after `/api/v2/` is published and Deprecation is signalled via a Deprecation response header.
Exact pagination query parameters listed: `page_size`, `cursor`, `source`, `keyword`. Cursor-based pagination response structure.
`JobListResponse` schema exact field definitions: `total`, `page`, `page_size`, `has_next`, `next_cursor`, `linkedin_count`, `jobserve_count`, `jobs`.
API design standards: typed request/response objects, OpenAPI specs, schema-first design, Pydantic v2, versioned routes (`/api/v1/`), cursor-based pagination, RFC 7807 structured errors, connection pooling. Domain-driven folder layout. MCP integration rules. Prompt caching strategy.

### `backend/logging_config.py` — MVP 1
Contains: Structured JSON logging implementation example.
Shared structured JSON logger (`get_logger(name)`) using `structlog` and `dict_tracebacks`.

### `backend/settings.py` — MVP 1
Contains: Pydantic `BaseSettings` class. All environment variables typed and validated at startup.
`SINGLE_USER_ID` temporary single-user bridge strategy configuration.

### `backend/filters.py` — MVP 1.1
Contains: Logic that merges `UserProfile` fields over `relevance_profile.yaml` defaults.

### `backend/routers/v1/scrape.py` — MVP 1
Contains: Scrape trigger endpoint.
Global scrape concurrency locking strategy (`asyncio.Lock` → Redis lock).
Redis distributed lock migration plan.
`ScrapeResult` response model structure.

### `backend/routers/v1/recruiters.py` — MVP 2
Contains: `POST /api/v1/recruiters` upsert endpoint with `linkedin_url` deduplication rules.
Recruiter deduplication edge case: If `linkedin_url` is absent from the scraped data, the recruiter record is skipped (not created with a null key).

### `backend/routers/v1/company_research.py` — MVP 2
Contains: `GET /api/v1/company-research`.
Company Research endpoint idempotency rule: Idempotent — if a fresh record already exists, returns 200 with the existing record.

### `backend/routers/v1/jobs.py` — MVP 1
Contains: `GET /api/v1/jobs`. Server-side `saved` field resolution behavior logic.

### `backend/routers/v1/interview.py` — MVP 2
Contains: Interview Prep endpoint returns 503 until active.

### `backend/routers/dependencies.py` — MVP 1.1+
Contains: `require_rag_ready` prerequisite dependency middleware.
Exact 422 HTTP Exception error conditions defined: UserProfile not found, CV not uploaded, CV embedding not ready.

### `backend/db.py` — MVP 2
Contains: Explicit asyncpg pool tuning configuration. Exact kwargs: `pool_size=10`, `max_overflow=20`, `pool_timeout=30`, `pool_recycle=1800`, `pool_pre_ping=True`.
MVP1 fake DB compatibility stub for `db.py`.

### `backend/main.py` — MVP 1
Contains: App entrypoint + agent auto-discovery imports.
Registry auto-discovery import strategy in `main.py`.

### `backend/admin/` — MVP 1+
Contains: Admin process command table. One-off admin process scripts (Twelve-Factor XII).
Exact one-off Admin Processes explicitly listed: Database migration, Rollback migration, Seed keyword list, Replay DLQ item, Run prompt regression eval, Clear fake database.

### `backend/migrations/` — MVP 2
Contains: Alembic migration history. Migration runs automatically via Supervisor.

### `backend/models/DOMAIN-MODELS.md` — MVP 2
Contains: Domain Model Definitions explicitly detailing fields for:
- `UserProfile` (including `target_roles`, `preferred_stack`, `seniority_level`, `target_salary_min`, `target_salary_max`, `preferred_location`, `notice_period`, `updated_at`)
- `CompanyResearch` (including `company_name_slug` which acts as a unique lookup key)
- `Job` (including the `saved` computed field populated by left join against `SavedJob`)
- `Recruiter` (including `linkedin_url` and `interaction_score`)
- `Application` (including `status` enum: draft, applied, awaiting_response, interviewing, offered, rejected, withdrawn)
- `CV` (including `embedding_status` enum: pending, processing, ready, failed)
- `CoverLetter` (including `ats_score`, `status` enum, and mandatory `user_id` for RLS isolation)
- `ScrapeRun` (including `jobs_inserted` and `errors`)

### `backend/models/` and `backend/schemas/`
Contains: SQLAlchemy models folder structure and Pydantic schema folder structure.
Repository and service layer separation documented.

### `backend/agents/base.py` — MVP 1
Contains: `BaseScrapeAgent` abstract contract details. Defines `source_id`, `display_name`, and `run()` interface.

### `backend/agents/registry.py` — MVP 1
Contains: Full extensible scraper registry architecture explanation.
`register()` decorator behavior.
`get_all_agents()` and `get_agent()` registry behavior.

### `backend/agents/AGENT.md` — MVP 1
Contains: Cross-agent DIFA and ReAct execution rules.
“No monolithic agent” architectural rule.
“No print() calls” logging rule.
`company_slug` normalization exact string manipulation rules: lowercase, strip punctuation, replace spaces with hyphens, truncate to 80 characters.
Graceful SIGTERM Playwright shutdown strategy.
Reed.co.uk extension example workflow.

### `backend/agents/linkedin/AGENT.md` — MVP 1
Contains: LinkedIn scraping responsibilities.

### `backend/agents/jobserve/AGENT.md` — MVP 1
Contains: JobServe scraping responsibilities.

### `backend/agents/ranking/AGENT.md` — MVP 2
Contains: AI Ranking Execution Model benefits (burst scaling, reduced idle compute cost, isolation of expensive AI workloads).
The architectural rule: "Ranked jobs become searchable only after scoring completes".
Exact 8 steps of the Ranking Agent scoring pipeline: embeddings, cosine similarity, cross-encoder reranking, sentiment, recruiter quality, compensation normalisation, skill extraction, seniority validation.

### `backend/agents/rag/AGENT.md` — MVP 2
Contains: Contextual retrieval, semantic memory.
RAG Agent evaluation exact metrics: Ragas (retrieval precision, context recall) and DeepEval (faithfulness, relevance).

### `backend/agents/cover-letter/AGENT.md` — MVP 2
Contains: Full cover letter playbook details.
Cover Letter Agent enforcement rule: ATS keyword match >= 60% enforced before delivery.

### `backend/agents/question-answer/AGENT.md` — MVP 2
Contains: RAG-powered Q&A on specific job listings.

### `backend/agents/security/AGENT.md` — MVP 2
Contains: Prompt injection detection.

### `backend/agents/observability/AGENT.md` — MVP 3
Contains: Tracing. Latency monitoring.

### `backend/agents/orchestrator/AGENT.md` — MVP 2
Contains: Orchestration rules. Retry logic.

### `backend/agents/application-assistant/AGENT.md` — Optional (post-MVP 3)
Contains: Full spec from the optional Application Assistant Agent.

### `backend/agents/interview-prep/AGENT.md` — Optional (post-MVP 3)
Contains: Full spec from the optional Interview Preparation Agent.

### `prompts/AGENT.md` — MVP 1.1
Contains: Full prompt engineering standards details.
Prompt Engineering mandatory XML tag structure: `<role>`, `<context>`, `<instructions>`, `<constraints>`, `<output_format>`, `<example>`.
Reasoning Effort exact values per agent: LinkedIn (low), Ranking (medium), RAG (high), Cover Letter (medium), Q&A (high), Security (high), Orchestrator (xhigh), Interview Prep (xhigh).
Deterministic structured outputs recommendation.
Prompt folder independence from backend deployments.

### `infrastructure/AGENT.md` — MVP 1–2
Contains: Cloud-native stack. Full infrastructure stack table. Detailed deployment target table.
API Gateway concern table (rate limiting, JWT, logging, CORS, request transformation).
Exact API Gateway plugins specified: rate-limiting, jwt, file-log, cors, request-transformer.
Release tagging with Git SHA strategy.
Rollback deployment strategy.
Full cloud-native engineering details.
Detailed breakdown of production services that scale independently: API containers, Temporal workers, scraper workers, ranking workers, observability services.

### `Dockerfile` and `supervisord.conf`
Contains: Docker build/release/run separation details.
Supervisor startup ordering and migration hook behavior.
Alembic migration startup guard when `DATABASE_URL` is absent.

### `AGENT.md` (root)
Contains: Explicit co-location philosophy for `.md` governance files.
Root `AGENT.md` lightweight index philosophy.
Detailed workflow orchestration rules from root `AGENT.md`.
Full root `AGENT.md` index template.

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
| Feature Flag Strategy | `docs/FEATURE-FLAGS.md` | MVP 2 |
| Outbound Scraping Rate Limiting Strategy | `docs/SCRAPING-RATE-LIMITS.md` | MVP 2 |
| Anti-Bot, Proxy, and Fingerprinting Disclaimer | `docs/ANTI-BOT.md` | MVP 1 |
| Disaster Recovery and Backup Restore | `infrastructure/DISASTER-RECOVERY.md` | MVP 3 |
| Domain Model Definitions | `backend/models/DOMAIN-MODELS.md` | MVP 2 |
| AI Ranking Execution Model | `backend/agents/ranking/AGENT.md` | MVP 2 |
| Data Ownership and Portability | `docs/DATA-OWNERSHIP.md` | MVP 3 |
| Local LLM Runtime Support | `infrastructure/LOCAL-LLM.md` | MVP 2 |

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
| MVP 1 | Local development deployment model (Docker Compose with full stack) |
| MVP 2 | Production deployment distinction (Azure Container Apps / ECS Fargate) - Independent scaling of production service types |
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
OPENROUTER_API_KEY=

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
