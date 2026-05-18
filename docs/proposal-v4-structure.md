
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
- Nginx serves the Next.js static export on port 80 and reverse-proxies `/api` to FastAPI on port 8000
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
├── docker-compose.yml                     # MVP 1: local dev orchestration
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
│   │   ├── jd-mvp1-1.csv
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
├── frontend/                              # Next.js 16 + React 19 — MVP 1
│   ├── AGENT.md                           # ← from: FRONTEND DASHBOARD features + FE stack requirements
│   ├── next.config.ts                     # output: "export" — static export for Nginx
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── .env.local.example
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── components/
│       ├── JobCard.tsx
│       ├── FilterBar.tsx
│       ├── ScrapeButton.tsx
│       └── ObservabilityPanel.tsx         # MVP 2+: agent trace + token usage panel
│
│
├── backend/                               # Python 3.14 + FastAPI + uv
│   ├── AGENT.md                           # ← from: BACKEND STACK + API DESIGN STANDARDS + MCP + PROMPT CACHING
│   ├── pyproject.toml
│   ├── main.py                            # MVP 1: app entrypoint + agent auto-discovery imports
│   ├── models.py                          # MVP 1: Job, ScrapeResult; MVP 2+: full domain models
│   ├── filters.py                         # MVP 1: keyword-based filtering logic
│   ├── logging_config.py                  # MVP 1: Twelve-Factor XI — structured JSON logger (shared by all agents)
│   ├── db.py                              # MVP 2: asyncpg connection pool (pool_size=10, max_overflow=20)
│   ├── settings.py                        # MVP 1: Pydantic Settings — all env vars typed and validated at startup
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
│   │   │   ├── AGENT.md                   # ← from: RAG Agent + RAG PERSONALIZATION (retrieval sources + eval metrics)
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
│   └── routers/
│       ├── jobs.py                        # MVP 1: GET /api/v1/jobs, GET /api/v1/jobs/{id}
│       ├── scrape.py                      # MVP 1: POST /api/v1/scrape (registry-driven)
│       ├── cover_letter.py                # MVP 2: POST /api/v1/cover-letter/{job_id}
│       ├── question_answer.py             # MVP 2: POST /api/v1/question-answer/{job_id}
│       └── interview.py                   # MVP 2+: POST /api/v1/interview-prep/{job_id}
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
│   │   ├── scoring.md
│   │   ├── reranking.md
│   │   └── filtering.md
│   │
│   ├── rag-agent/                         # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── retrieval.md
│   │   ├── embeddings.md
│   │   └── personalization.md
│   │
│   ├── cover-letter-agent/                # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── tone.md
│   │   ├── generation.md
│   │   └── templates.md
│   │
│   ├── question-answer-agent/             # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   └── tools.md
│   │
│   ├── security-agent/                    # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   └── system.md
│   │
│   ├── orchestrator/                      # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   └── system.md
│   │
│   ├── application-assistant/             # Optional (post-MVP 3)
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   └── system.md
│   │
│   └── interview-prep/                    # Optional (post-MVP 3)
│       ├── CONTRACT.md
│       ├── CHANGELOG.md
│       └── system.md
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
| Pydantic Settings (env var validation) | `backend/settings.py` | MVP 1 |
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
| Interview Preparation Intelligence Agent | `backend/agents/interview-prep/AGENT.md` | Optional |
| Scalable API Design (versioning, pagination, gateway, pooling) | `backend/AGENT.md` | MVP 1–2 |
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
| Active task plan | tasks/todo.md | MVP 1 |
| Self-improvement log | tasks/lessons.md | MVP 1 |
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
priority=10  fastapi   → uvicorn on 127.0.0.1:8000

### Request Routing
Browser → port 80 → Nginx
/          → /var/www/html  (Next.js static export)
/api/v1/*  → 127.0.0.1:8000 (FastAPI)
/health    → 127.0.0.1:8000/health

### Dockerfile

```dockerfile
# ─── Stage 1: Build Next.js static export ───────────────────────────────────
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build
# Produces /app/frontend/out — fully static HTML/JS/CSS


# ─── Stage 2: Backend runtime + Nginx + static frontend ─────────────────────
FROM python:3.14-slim AS runtime

# System packages: nginx + supervisor (process manager)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Backend dependencies via uv
WORKDIR /app/backend
COPY backend/pyproject.toml ./
RUN uv sync --no-dev

# Backend source
COPY backend/ .

# Install Playwright Chromium (required for scraper agents)
RUN uv run playwright install chromium --with-deps

# Copy built frontend into nginx web root
COPY --from=frontend-builder /app/frontend/out /var/www/html

# Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Supervisor config
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

        # Serve Next.js static export
        location / {
            root   /var/www/html;
            index  index.html;
            try_files $uri $uri/ $uri.html /index.html;
        }

        # Reverse-proxy all /api/* requests to FastAPI
        location /api/ {
            proxy_pass         http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_read_timeout 120s;
        }

        # Health check endpoint
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
command=uv run alembic upgrade head
directory=/app/backend
autostart=true
autorestart=false
startsecs=0
priority=1
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
command=uv run uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2
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
```

---

## next.config.ts UPDATE REQUIRED

For the static export to work inside the single container, Next.js must be configured with `output: "export"`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",       // Produces /out — served by Nginx
  reactStrictMode: true,
  trailingSlash: true,    // Required for try_files to resolve routes
};

export default nextConfig;
```

Note: `output: "export"` means Server Actions and Route Handlers are not available. All dynamic data must go through the FastAPI backend via `/api/*`. React Server Components that fetch data must use static generation or client-side fetching.

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
Backend stack (Python 3.14, FastAPI, uv, Pydantic v2, SQLAlchemy 2, pgvector, Redis, LiteLLM, OpenTelemetry).
Database stack (Supabase PostgreSQL, pgvector, RLS, partitioning, JSONB, WAL).
Full Twelve-Factor compliance notes (all 12 factors explicitly addressed).

### `docs/SECURITY.md` — MVP 2–3
Supabase Auth, JWT, RBAC, RLS. OWASP Top 10 checklist. Prompt injection defense. Required protections.

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

### `frontend/AGENT.md` — MVP 1
Frontend stack spec. Dashboard feature list: AI relevance scoring, RAG insights, recruiter intelligence, cover letter generation, observability dashboards, token usage dashboards, agent traces, prompt debugging, saved jobs, filtering, dark/light mode.

### `backend/AGENT.md` — MVP 1
Backend stack spec. API design standards: typed request/response objects, OpenAPI specs, schema-first design, Pydantic v2, versioned routes (`/api/v1/`), cursor-based pagination, connection pooling. MCP integration rules. Prompt caching strategy.

### `backend/logging_config.py` — MVP 1
Shared structured JSON logger (`get_logger(name)`). Twelve-Factor XI compliance. All agents and routers import from this module — no `print()` calls anywhere.

### `backend/settings.py` — MVP 1
Pydantic Settings class. All environment variables typed and validated at startup. Fails fast if any required var is missing.

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
Full spec from the optional Interview Preparation Agent: trigger syntax, responsibilities, RAG context sources (job description, company blogs, recruiter profile, CV, historical interviews, GitHub repositories, tech stack signals), AI output requirements, recommended technologies.

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