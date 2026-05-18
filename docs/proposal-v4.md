# Project Proposal

# AI-Powered Job Discovery and Application Intelligence Platform

**Version:** 1.2.0
**Status:** Proposed
**Author:** Qasir Mehmood — Senior Full-Stack Engineer and Azure AI Solutions Consultant
**Date:** May 2026
**Changes from v1.1.0:** MVP 1.1 added for advanced prompt engineering infrastructure (`job-discovery/prompts`).

---

## Executive Summary

This proposal defines the architecture, structure, delivery approach, and engineering standards for a production-grade AI-powered personal job intelligence platform. The platform continuously discovers job listings from LinkedIn, JobServe, and any future job board added via a pluggable scraper registry, ranks them using AI relevance scoring, personalises recommendations through RAG pipelines, generates tailored cover letters, and supports application workflow assistance — all within a single deployable Docker container with a modular multi-agent backend.

The platform is designed from first principles to be extensible: adding a new job board requires only writing a new agent module and registering it — no changes to the orchestrator, router, or database layer. The architecture complies fully with the Twelve-Factor App methodology and scalable API design standards.

---

## Problem Statement

Senior engineers and AI consultants operating in a competitive contract market face three compounding problems.

First, job discovery is fragmented across multiple boards with no unified relevance filtering. Most listings returned by keyword search are noise — wrong seniority level, mismatched stack, or recycled postings.

Second, application effort is high and repetitive. Writing a tailored cover letter, researching the recruiter, and preparing for a technical interview each require significant manual effort that does not compound over time.

Third, there is no feedback loop. Without structured tracking of applications, responses, and interview outcomes, it is impossible to improve the outreach strategy or identify which roles and recruiters convert.

This platform solves all three problems through AI-assisted discovery, personalisation, and workflow automation, while keeping the engineer in full control of every submission.

---

## Objectives

**Job discovery:** continuously scrape LinkedIn, JobServe, and registered future job boards for relevant UK-based senior engineering and AI roles, filter by skill match, and surface only high-relevance listings ranked by AI scoring.

**Extensibility:** any new job board can be added by writing one agent module and registering it in the scraper registry — zero changes to the orchestrator, API, or database.

**Personalisation:** use RAG pipelines grounded in the user's CV, application history, and recruiter interactions to personalise recommendations, cover letters, and interview preparation.

**Cover letter generation:** produce ATS-optimised, recruiter-focused cover letters tailored to each role using a structured generation playbook.

**Interview preparation:** generate a personalised preparation pack for any saved role including technical question sets, system design topics, behavioural questions, salary benchmarks, and company intelligence.

**Workflow assistance:** semi-automated application assistance that autofills forms and uploads documents — but never auto-submits without explicit user confirmation.

**Observability:** full agent execution traces, token usage dashboards, retrieval quality metrics, and hallucination monitoring exposed to the developer dashboard.

**Twelve-Factor compliance:** all twelve factors addressed explicitly in architecture and delivery.

**Scalable APIs:** versioned, paginated, rate-limited, and gateway-backed APIs from MVP2 onwards.

---

## Scope

### In Scope — MVP1

- LinkedIn scraper agent
- JobServe scraper agent
- Extensible scraper registry supporting future job board agents
- In-memory fake database (replaced by Supabase in MVP2)
- FastAPI backend with full OpenAPI spec
- Next.js 16 frontend dashboard
- Next.js 16 latest hooks like use, useOptimistic, useActionState etc...
- Single Docker container (Nginx + FastAPI + static export)
- GitHub Actions CI skeleton

### In Scope — MVP 1.1

- Advanced prompt engineering infrastructure (`job-discovery/prompts`)
- Initial system prompt versioning and evaluation framework
- Prompt-based relevance filtering (pre-pgvector ranking)
- Contract and Changelog management for AI agents

### In Scope — MVP2 and Beyond

- AI ranking and relevance scoring agent (pgvector, embeddings, reranking)
- RAG personalisation agent (Ragas, DeepEval evaluation)
- Cover letter generation agent
- Question answer agent
- Security and prompt injection defence agent
- Observability agent and Grafana dashboards
- Workflow orchestrator agent (Temporal)
- Optional: Application Assistant Agent
- Optional: Interview Preparation Intelligence Agent
- Supabase PostgreSQL replacing fake database
- API versioning (`/api/v1/`), pagination, connection pooling
- Azure Container Apps deployment via Terraform
- Full Twelve-Factor compliance including structured logging and admin process strategy

### Deployment Targets

| Target | Priority |
|---|---|
| Local Docker (docker-compose) | MVP1 |
| Azure Container Apps (Terraform) | MVP2 |
| AWS ECS Fargate | MVP3 |


### Out of Scope

- Auto-submission of job applications under any circumstance
- LinkedIn authenticated scraping or API access
- CAPTCHA bypassing of any kind
- SaaS mode
- Mobile native applications

---

## Twelve-Factor Compliance

The Twelve-Factor App methodology builds software-as-a-service apps that use declarative formats for setup automation, have a clean contract with the underlying OS for maximum portability, are suitable for deployment on modern cloud platforms, minimise divergence between development and production, and can scale up without significant changes to tooling or architecture.

Every factor is addressed explicitly below. Factors that were gaps in v1.0.0 are marked **[Gap addressed]**.

### Factor I — Codebase
One codebase tracked in Git. One monorepo: `job-discovery/`. Multiple deploy environments (local, Azure, AWS) share the same codebase with environment-specific configuration injected via env vars. No per-environment code branches.

### Factor II — Dependencies
Backend: all dependencies declared in `pyproject.toml`, locked via `uv.lock`. No implicit system-level dependencies. `uv sync` reproduces the exact environment on any machine.
Frontend: all dependencies declared in `package.json`, locked via `package-lock.json`. `npm ci` reproduces the exact environment.
Playwright Chromium is installed explicitly via `uv run playwright install chromium` — not assumed to be present.

### Factor III — Config
All configuration that varies between environments is stored in environment variables. No config is hardcoded. No config files are committed to version control. `.env.example` documents every required variable with an empty value. Secrets are injected at runtime via `--env-file` locally and via Azure Key Vault references in production. Docker images contain zero secrets.

### Factor IV — Backing Services
Supabase PostgreSQL, Redis, Temporal, and LiteLLM are all treated as attached resources. Each is referenced by a URL stored in an environment variable. Swapping any backing service (e.g. replacing Redis with another queue) requires only an env var change — no code changes.

### Factor V — Build / Release / Run
The multi-stage Dockerfile strictly separates:
- **Build:** `node:22-alpine` stage runs `npm ci` + `next build` producing an immutable `/out` artefact
- **Release:** GitHub Actions CI combines the built image with environment-specific config (env vars) to produce a tagged, immutable release. Each release is tagged with the Git commit SHA — e.g. `job-discovery:abc1234`
- **Run:** Supervisor starts nginx and uvicorn from the immutable release image. No build steps run at runtime.

Rollback: redeploy the previous commit SHA image. No database migrations roll back automatically — see Factor XII.

### Factor VI — Processes
**[Gap addressed]**
FastAPI is stateless. No session state, no in-memory cache between requests. All shared state lives in Supabase or Redis.

Scraper agents are long-running and must NOT run inside the uvicorn HTTP process pool. They run as a separate Temporal worker process. The process model is:

| Process type | Runs as | Scales independently |
|---|---|---|
| HTTP API | uvicorn (2 workers) | Yes — add uvicorn replicas |
| Scraper / agent workers | Temporal worker process | Yes — add Temporal worker replicas |
| Scheduled triggers | Temporal cron workflow | Yes — runs in Temporal cluster |

The fake database in MVP1 (in-process dict) is an explicit MVP1 exception — it is replaced by Supabase before any production deployment.

### Factor VII — Port Binding
FastAPI binds to `127.0.0.1:8000` and exports its HTTP service via that port. Nginx binds to port 80 and proxies inbound requests. The application is fully self-contained — no external web server is required to make it routable. In production on Azure Container Apps, the container exports port 80 and the platform routes traffic to it.

### Factor VIII — Concurrency
**[Gap addressed]**
The concurrency model is defined explicitly as three independent process types that scale separately:

- **uvicorn workers** handle HTTP request concurrency — scaled by increasing `--workers` or adding container replicas
- **Temporal workers** handle agent execution concurrency — scaled by adding worker replicas pointing at the same Temporal namespace
- **Redis** handles job queue concurrency — scaled by Redis Cluster if needed

Scraper agents are CPU and I/O bound (Playwright). They must not share the uvicorn process. Running them in the Temporal worker process pool means they can be scaled out independently of the HTTP tier without modifying application code.

### Factor IX — Disposability
**[Gap addressed]**
Processes must start fast and shut down gracefully.

- uvicorn handles SIGTERM by draining in-flight HTTP requests before exit
- Temporal workers checkpoint after each activity — a worker killed mid-run will have its workflow resumed by another worker automatically
- Playwright scraper sessions register a SIGTERM handler that closes the browser context cleanly before exit:

```python
import signal, asyncio

async def shutdown(browser):
    await browser.close()

signal.signal(signal.SIGTERM, lambda s, f: asyncio.ensure_future(shutdown(browser)))
```

- Supervisor is configured with `stopwaitsecs=30` — allows 30 seconds for graceful drain before SIGKILL

### Factor X — Dev / Prod Parity
The same Docker image runs locally via docker-compose and in production on Azure Container Apps. No dev-only dependencies exist. `.env.example` documents the exact same variable set used in all environments. `uv sync` and `npm ci` produce bit-identical dependency trees across machines.

### Factor XI — Logs
**[Gap addressed]**
All `print()` statements in scraper agents are replaced with a structured JSON logger. A shared logging module is imported by all agents:

```python
# backend/logging_config.py
import logging, json, sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "agent": record.name,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record),
        })

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
```

Logs are written to stdout as a structured event stream. The platform (Docker, Supervisor, Azure Container Apps) captures stdout and routes it to the log aggregator (Loki). No log files are written to disk. No log rotation is configured — the platform handles it.

### Factor XII — Admin Processes
**[Gap addressed]**
One-off admin tasks run as isolated processes in the same Docker image and with the same environment as the production app. They are never run from a separate environment.

Defined admin processes:

| Task | Command |
|---|---|
| Database migration | `uv run alembic upgrade head` |
| Rollback migration | `uv run alembic downgrade -1` |
| Seed keyword list | `uv run python admin/seed_keywords.py` |
| Replay DLQ item | `uv run python admin/replay_dlq.py --id {id}` |
| Run prompt regression eval | `uv run python evals/run_evals.py --agent {name}` |
| Clear fake database (dev only) | `uv run python admin/clear_db.py` |

All admin scripts live in `backend/admin/` and are tracked in version control. Alembic migration runs automatically as a container startup hook before uvicorn starts — configured in supervisord:

```ini
[program:migrate]
command=uv run alembic upgrade head
directory=/app/backend
autostart=true
autorestart=false
startsecs=0
priority=1
```

uvicorn and nginx are given higher `priority` numbers so they start after migration completes.

---

## Scalable API Design

All gaps identified in the v1.0.0 review are addressed here.

### API Versioning

All routes are prefixed with `/api/v1/`. The version is part of the URL, not a header, for maximum compatibility with proxies, gateways, and cached clients.

```
GET  /api/v1/jobs
GET  /api/v1/jobs/{id}
POST /api/v1/scrape
POST /api/v1/cover-letter/{job_id}
POST /api/v1/interview-prep/{job_id}
POST /api/v1/cv
GET  /api/v1/admin/dlq
GET  /api/v1/admin/schedule
```

**Versioning policy:**
- Minor changes (new optional fields, new endpoints) do not increment the version
- Breaking changes (removed fields, changed field types, changed semantics) increment to `/api/v2/`
- `/api/v1/` remains supported for a minimum of 6 months after `/api/v2/` is published
- Deprecation is signalled via a `Deprecation` response header on all `/api/v1/` routes

### Pagination

`GET /api/v1/jobs` supports cursor-based pagination:

```python
class JobListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    has_next: bool
    next_cursor: str | None
    linkedin_count: int
    jobserve_count: int
    jobs: list[Job]
```

Query parameters: `page_size` (default 20, max 100), `cursor` (opaque string from previous response). This avoids `OFFSET` pagination performance degradation at large dataset sizes.

### API Gateway

| Concern | Implementation |
|---|---|
| Rate limiting | `rate-limiting` — 100 req/min per authenticated user |
| Authentication enforcement | `jwt` — validates JWT before requests reach FastAPI |
| Request logging | `file-log` → stdout → Loki |
| CORS | `cors` plugin |
| Request transformation | `request-transformer` — strips internal headers |


### Connection Pooling

asyncpg connection pool is configured explicitly in `backend/db.py`:

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    url=settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
```

Pool size is tuned to the uvicorn worker count. Each worker gets its own pool. Total max connections to Supabase: `workers × (pool_size + max_overflow)`.

### Request Throttling for Scrape Trigger

`POST /api/v1/scrape` is rate-limited to 1 concurrent execution globally using a Redis distributed lock:

```python
async def trigger_scrape():
    lock = redis.lock("scrape:global", timeout=3600)
    if not await lock.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Scrape already in progress")
    try:
        ...
    finally:
        await lock.release()
```

This prevents Playwright resource exhaustion when multiple clients trigger scrapes simultaneously.

---

## Extensible Scraper Registry

This is the core architectural decision that makes the platform open to future job boards without modifying the orchestrator, router, or database.

### Design

Every job board scraper is a Python module that implements the `BaseScrapeAgent` abstract base class. The orchestrator discovers and runs all registered agents dynamically — it has no hardcoded references to LinkedIn or JobServe.

```python
# backend/agents/base.py

from abc import ABC, abstractmethod
from models import Job

class BaseScrapeAgent(ABC):

    @property
    @abstractmethod
    def source_id(self) -> str:
        """
        Unique stable identifier for this job board.
        Used as the 'source' field on every Job record.
        Example: "linkedin", "jobserve", "cwjobs", "reed"
        """

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name shown in the dashboard."""

    @abstractmethod
    async def run(self) -> int:
        """
        Execute the scrape for this job board.
        Returns the count of new jobs inserted.
        All agents are responsible for their own deduplication,
        keyword filtering, and fake_db / Supabase insertion.
        """
```

### Registry

The registry is a module-level dict that maps `source_id` to agent class. Agents self-register on import:

```python
# backend/agents/registry.py

from typing import Type
from agents.base import BaseScrapeAgent

_REGISTRY: dict[str, Type[BaseScrapeAgent]] = {}


def register(agent_cls: Type[BaseScrapeAgent]) -> Type[BaseScrapeAgent]:
    """Decorator — registers an agent class by its source_id."""
    instance = agent_cls()
    _REGISTRY[instance.source_id] = agent_cls
    return agent_cls


def get_all_agents() -> list[BaseScrapeAgent]:
    """Return one instantiated instance of every registered agent."""
    return [cls() for cls in _REGISTRY.values()]


def get_agent(source_id: str) -> BaseScrapeAgent | None:
    cls = _REGISTRY.get(source_id)
    return cls() if cls else None
```

### LinkedIn Agent (registered)

```python
# backend/agents/linkedin/linkedin_agent.py

from agents.registry import register
from agents.base import BaseScrapeAgent

@register
class LinkedInAgent(BaseScrapeAgent):

    @property
    def source_id(self) -> str:
        return "linkedin"

    @property
    def display_name(self) -> str:
        return "LinkedIn"

    async def run(self) -> int:
        # Full Playwright scraping logic here
        ...
```

### JobServe Agent (registered)

```python
# backend/agents/jobserve/jobserve_agent.py

from agents.registry import register
from agents.base import BaseScrapeAgent

@register
class JobServeAgent(BaseScrapeAgent):

    @property
    def source_id(self) -> str:
        return "jobserve"

    @property
    def display_name(self) -> str:
        return "JobServe"

    async def run(self) -> int:
        # Full Playwright scraping logic here
        ...
```

### Adding a New Job Board (example: Reed.co.uk)

To add Reed as a third job board, a developer does exactly three things:

1. Create `backend/agents/reed/` folder
2. Write `backend/agents/reed/reed_agent.py` implementing `BaseScrapeAgent` with `source_id = "reed"`
3. Add `backend/agents/reed/AGENT.md` with the scraping spec

The orchestrator, router, database, and frontend automatically include Reed with zero additional changes.

```python
# backend/agents/reed/reed_agent.py

from agents.registry import register
from agents.base import BaseScrapeAgent

@register
class ReedAgent(BaseScrapeAgent):

    @property
    def source_id(self) -> str:
        return "reed"

    @property
    def display_name(self) -> str:
        return "Reed"

    async def run(self) -> int:
        # Playwright scraping logic for reed.co.uk
        ...
```

### Registry Auto-Discovery

All agent modules are imported at startup so their `@register` decorators fire. A single import block in `main.py` handles this:

```python
# backend/main.py

# Auto-discover and register all scraper agents
import agents.linkedin.linkedin_agent      # noqa: F401
import agents.jobserve.jobserve_agent      # noqa: F401
# New agents: add one import line here — nothing else changes
```

### Orchestrator Uses Registry

The scrape router calls `get_all_agents()` — it has no knowledge of specific job boards:

```python
# backend/routers/scrape.py

from agents.registry import get_all_agents
from models import ScrapeResult
import time

@router.post("/scrape", response_model=ScrapeResult)
async def trigger_scrape() -> ScrapeResult:
    start = time.monotonic()
    results: dict[str, int] = {}

    for agent in get_all_agents():
        results[agent.source_id] = await agent.run()

    return ScrapeResult(
        results=results,
        total_inserted=sum(results.values()),
        duration_seconds=round(time.monotonic() - start, 2),
    )
```

### Updated ScrapeResult Model

```python
class ScrapeResult(BaseModel):
    results: dict[str, int]   # {"linkedin": 12, "jobserve": 4, "reed": 7}
    total_inserted: int
    duration_seconds: float
```

The frontend renders per-source counts dynamically from `results` — no hardcoded source names in the UI.

---

## Project Structure

```
job-discovery/
│
├── AGENT.md                               # Root index — no standards content
├── docker-compose.yml
├── Dockerfile                             # Multi-stage: FE build + BE runtime + Nginx
├── nginx.conf
├── supervisord.conf
├── .env.example
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ENGINEERING-STANDARDS.md
│   ├── SECURITY.md
│   ├── OBSERVABILITY.md
│   ├── RELIABILITY.md
│   ├── REAL-TIME.md
│   ├── ANALYTICS.md
│   ├── ADTECH-CONTEXT.md
│   └── EXECUTION-RULES.md
│
├── frontend/
│   ├── AGENT.md
│   ├── next.config.ts
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
│       └── ObservabilityPanel.tsx
│
├── backend/
│   ├── AGENT.md
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   ├── filters.py
│   ├── logging_config.py              # Twelve-Factor XI: structured JSON logger
│   ├── db.py                          # asyncpg connection pool config
│   ├── settings.py                    # Pydantic Settings — all env vars typed
│   │
│   ├── admin/                         # Twelve-Factor XII: one-off admin processes
│   │   ├── seed_keywords.py
│   │   ├── replay_dlq.py
│   │   ├── clear_db.py
│   │   └── run_evals.py
│   │
│   ├── agents/
│   │   ├── AGENT.md                   # Cross-agent rules
│   │   ├── base.py                    # BaseScrapeAgent ABC
│   │   ├── registry.py                # @register decorator + get_all_agents()
│   │   │
│   │   ├── linkedin/
│   │   │   ├── AGENT.md
│   │   │   └── linkedin_agent.py
│   │   │
│   │   ├── jobserve/
│   │   │   ├── AGENT.md
│   │   │   └── jobserve_agent.py
│   │   │
│   │   ├── ranking/
│   │   │   ├── AGENT.md
│   │   │   └── ranking_agent.py
│   │   │
│   │   ├── rag/
│   │   │   ├── AGENT.md
│   │   │   └── rag_agent.py
│   │   │
│   │   ├── cover-letter/
│   │   │   ├── AGENT.md
│   │   │   └── cover_letter_agent.py
│   │   │
│   │   ├── question-answer/
│   │   │   ├── AGENT.md
│   │   │   └── question_answer_agent.py
│   │   │
│   │   ├── security/
│   │   │   ├── AGENT.md
│   │   │   └── security_agent.py
│   │   │
│   │   ├── observability/
│   │   │   ├── AGENT.md
│   │   │   └── observability_agent.py
│   │   │
│   │   ├── orchestrator/
│   │   │   ├── AGENT.md
│   │   │   └── orchestrator_agent.py
│   │   │
│   │   ├── application-assistant/     # Optional
│   │   │   ├── AGENT.md
│   │   │   └── application_agent.py
│   │   │
│   │   └── interview-prep/            # Optional
│   │       ├── AGENT.md
│   │       └── interview_agent.py
│   │
│   ├── migrations/                    # Alembic migrations (Factor XII)
│   │   ├── env.py
│   │   ├── alembic.ini
│   │   └── versions/
│   │
│   └── routers/
│       ├── jobs.py
│       ├── scrape.py
│       ├── cover_letter.py
│       ├── question_answer.py
│       └── interview.py
│
├── prompts/
│   ├── AGENT.md
│   ├── linkedin-agent/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   ├── jobserve-agent/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   ├── ranking-agent/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── scoring.md
│   │   ├── reranking.md
│   │   └── filtering.md
│   ├── rag-agent/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── retrieval.md
│   │   ├── embeddings.md
│   │   └── personalization.md
│   ├── cover-letter-agent/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── tone.md
│   │   ├── generation.md
│   │   └── templates.md
│   ├── question-answer-agent/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   └── tools.md
│   ├── security-agent/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   └── system.md
│   ├── orchestrator/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   └── system.md
│   ├── application-assistant/
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   └── system.md
│   └── interview-prep/
│       ├── CONTRACT.md
│       ├── CHANGELOG.md
│       └── system.md
│
└── infrastructure/
    ├── AGENT.md
    ├── terraform/
    │   ├── azure/
    │   │   ├── main.tf               # Azure Container Apps (primary)
    │   │   ├── variables.tf
    │   │   └── outputs.tf
    │   └── aws/                      # AWS ECS Fargate (MVP3)
    │       ├── main.tf
    │       ├── variables.tf
    │       └── outputs.tf
    └── helm/
        └── job-discovery/
            ├── Chart.yaml
            └── values.yaml
```

---

## Technology Stack

### Frontend

| Concern | Technology |
|---|---|
| Framework | Next.js 16 |
| UI library | React 19 |
| Language | TypeScript 6+ |
| Styling | Tailwind CSS 4 |
| Component library | Material UI 7 |
| Server state | TanStack Query |
| Client state | Zustand |
| Schema validation | Zod |
| React 19 hooks | use, useTransition, useOptimistic, useActionState |

### Backend

| Concern | Technology |
|---|---|
| Language | Python 3.14+ |
| Framework | FastAPI 0.115+ |
| Package manager | uv |
| Schema validation | Pydantic v2 |
| Settings management | Pydantic Settings (typed env vars) |
| ORM | SQLAlchemy 2 |
| Async database driver | asyncpg (pool_size=10, max_overflow=20) |
| Vector search | pgvector |
| Cache and messaging | Redis |
| Task orchestration | Temporal |
| LLM abstraction | LiteLLM |
| Observability | OpenTelemetry |
| Browser automation | Playwright |
| Migrations | Alembic |

### Database

| Concern | Technology |
|---|---|
| Primary database | Supabase PostgreSQL |
| Vector search extension | pgvector |

Requirements: row-level security, UUID primary keys, JSONB metadata, WAL backups, partitioning, encrypted secrets, audit logging.

### Infrastructure

| Concern | Technology |
|---|---|
| Containerisation | Docker multi-stage |
| Process management | Supervisor |
| Reverse proxy | Nginx |
| Infrastructure as code | Terraform |
| CI/CD | GitHub Actions |

---

## Multi-Agent Architecture

### Cross-Agent Rules

- No monolithic agent. Every agent has a single responsibility.
- All agents follow the DIFA framework: Discover, Interpret, Filter, Act.
- All reasoning agents use the ReAct loop: Reason, Act, Observe, Repeat, Answer.
- All agents import `get_logger` from `backend/logging_config.py` — no `print()` calls.
- All scraper agents extend `BaseScrapeAgent` and self-register via `@register`.
- All agents have their own `AGENT.md` spec, `prompts/` folder, and `CONTRACT.md`.

### Scraper Agents (extensible)

Any job board is supported by implementing `BaseScrapeAgent`. Currently registered:

| Agent | source_id | Status |
|---|---|---|
| LinkedIn Agent | linkedin | MVP1 |
| JobServe Agent | jobserve | MVP1 |
| Reed Agent (example) | reed | Future — add by creating `agents/reed/` |
| CWJobs Agent (example) | cwjobs | Future — add by creating `agents/cwjobs/` |
| Totaljobs Agent (example) | totaljobs | Future — add by creating `agents/totaljobs/` |

### Intelligence Agents

**Ranking Agent** — 8-step scoring pipeline: embeddings, cosine similarity, cross-encoder reranking, sentiment, recruiter quality, compensation normalisation, skill extraction, seniority validation. Stores only jobs scoring >= 75% similarity and above reranker confidence threshold.

**RAG Agent** — contextual retrieval from CV, applications, recruiter messages, saved jobs, preferences, skill graph. Evaluated via Ragas (retrieval precision, context recall) and DeepEval (faithfulness, relevance).

**Cover Letter Agent** — structured playbook: role summary, matching skills, quantified achievements, AI narrative, ATS keyword optimisation, recruiter-focused language. ATS keyword match >= 60% enforced before delivery.

**Question Answer Agent** — RAG-powered Q&A on specific job listings. Answers technical or cultural questions by grounding in job descriptions, company metadata, and user's professional background.

**Security Agent** — prompt injection detection, OWASP validation middleware, RBAC enforcement, HTML/markdown sanitisation, audit logging.

**Observability Agent** — traces, latency p50/p95, token usage, hallucination rate, retrieval quality, reranker confidence — all via OpenTelemetry.

**Workflow Orchestrator** — Temporal workflows for scrape pipeline, retry with exponential backoff and jitter, dead-letter queue, checkpoint recovery, idempotency enforcement.

### Optional Agents

**Application Assistant Agent** — semi-automated form filling and document upload via Playwright. Never auto-submits. Always requires explicit user confirmation. Safety rules enforced in code.

**Interview Preparation Agent** — RAG-grounded preparation pack: technical questions, behavioural questions, system design topics, salary guidance, company intelligence.

---

## Scalable API Reference

### Versioned Base URL

```
http://localhost:8000/api/v1/
```

### Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/jobs` | List jobs — paginated, filterable by source and keyword |
| GET | `/api/v1/jobs/{id}` | Single job by id |
| POST | `/api/v1/scrape` | Trigger all registered agents via registry |
| POST | `/api/v1/cv` | Upload and embed user CV |
| POST | `/api/v1/cover-letter/{job_id}` | Generate tailored cover letter |
| POST | `/api/v1/question-answer/{job_id}` | Answer specific questions about a job listing |
| POST | `/api/v1/interview-prep/{job_id}` | Generate interview preparation pack |
| GET | `/api/v1/admin/dlq` | List dead-letter queue items |
| POST | `/api/v1/admin/dlq/{id}/retry` | Replay failed DLQ item |
| POST | `/api/v1/admin/dlq/{id}/discard` | Remove failed DLQ item |
| GET | `/api/v1/admin/schedule` | Show next scheduled scrape run |
| POST | `/api/v1/admin/schedule/pause` | Pause scheduled scraper |
| POST | `/api/v1/admin/schedule/resume` | Resume scheduled scraper |
| GET | `/health` | Health check (unversioned — used by container probes) |

### Pagination

`GET /api/v1/jobs` query parameters:

| Parameter | Default | Max | Description |
|---|---|---|---|
| page_size | 20 | 100 | Items per page |
| cursor | null | — | Opaque cursor from previous response |
| source | null | — | Filter: linkedin, jobserve, reed, etc. |
| keyword | null | — | Filter: substring match on title |


| Endpoint | Limit |
|---|---|
| `GET /api/v1/jobs` | 300 req/min per user |
| `POST /api/v1/scrape` | 1 concurrent globally (Redis lock) |
| `POST /api/v1/cover-letter/*` | 20 req/min per user |
| `POST /api/v1/question-answer/*` | 30 req/min per user |
| `POST /api/v1/interview-prep/*` | 10 req/min per user |

---

## AI Prompt Engineering Standards

All prompts comply with the following standards sourced from OpenAI Prompt Guidance (GPT-5.x) and Anthropic Claude Prompting Best Practices (Claude Opus 4.x / Sonnet 4.x).

### Mandatory System Prompt Structure

```text
<role>        — precise agent identity, no vague persona definitions           </role>
<context>     — all background knowledge, long documents placed before tasks   </context>
<instructions>— ordered, imperative steps, explicit scope per instruction      </instructions>
<constraints> — every hard prohibition, all contradictions resolved            </constraints>
<output_format>— exact JSON schema or structure, completion criterion defined  </output_format>
<example>     — realistic domain data, matches output_format exactly           </example>
```

### Reasoning Effort per Agent

| Agent | Effort | Rationale |
|---|---|---|
| LinkedIn / JobServe / Reed | low | Execution-only: DOM extraction and keyword matching |
| Ranking | medium | Multi-signal scoring pipeline |
| RAG | high | Retrieval quality requires extended reasoning |
| Cover Letter | medium | Structured generation with fixed playbook |
| Question Answer | high | RAG-grounded retrieval and synthesis |
| Security | high | Adversarial input analysis |
| Orchestrator | xhigh | Long-horizon agentic coordination |
| Interview Prep | xhigh | Research synthesis across multiple sources |

### Prompt Versioning

All prompts use semantic versioning. Every prompt folder contains `CONTRACT.md` (model pin, effort, token budget, permitted tools, eval reference), `CHANGELOG.md`, and `system.md` as the live prompt.

---

## Security Architecture

### Authentication
Supabase Auth with JWT. RBAC enforced at FastAPI route level via JWT claims. Row-Level Security at Supabase database level — users read and write only their own rows.

### OWASP Top 10

| Risk | Mitigation |
|---|---|
| Broken Access Control | RBAC + RLS at every layer |
| Cryptographic Failures | Encrypted secrets via Azure Key Vault, TLS enforced |
| Injection | Pydantic schema validation on all inputs, SQL via SQLAlchemy ORM |
| Insecure Design | Security Agent reviews all agent outputs before storage |
| Security Misconfiguration | Terraform enforces immutable infrastructure |
| Vulnerable Components | Trivy and Bandit scan in every CI run |
| Authentication Failures | Supabase Auth with JWT rotation |
| Software Integrity Failures | Docker image signing in CI via GitHub Actions |
| Logging Failures | Structured JSON logs on all events via OpenTelemetry |
| SSRF | Allowlisted external domains only for all agent outbound calls |

### Prompt Injection Defence
All user-supplied content passes through the Security Agent before LLM inclusion: instruction hierarchy enforcement, schema validation, context isolation, allowlisted tools only, HTML and markdown sanitisation, output validation before storage.

---

## Observability

| Tool | Purpose |
|---|---|
| OpenTelemetry | Distributed tracing and metrics |
| Grafana | Dashboard rendering |
| Prometheus | Metrics scraping |
| Loki | Log aggregation from stdout streams |
| Sentry | Error tracking and alerting |
| Microsoft Clarity | Frontend session replay and UX analytics |

### Metrics and Targets

| Metric | Target |
|---|---|
| Schema conformance rate | >= 99% |
| HTTP latency p50 | < 500ms |
| HTTP latency p95 | < 2s |
| Agent execution latency p95 | < 8s |
| Token usage per agent run | Budgeted in CONTRACT.md |
| Hallucination rate | Monitored — alert if > 1% |
| Retrieval precision | >= 0.80 |
| Reranker confidence | Above configured threshold |

---

## Reliability Engineering

| Pattern | Implementation |
|---|---|
| Circuit breakers | Per agent — opens after 3 consecutive failures |
| Exponential backoff | Base 1s, max 60s, jitter enabled |
| Dead-letter queues | Redis DLQ per agent via Temporal |
| Workflow checkpoints | Temporal activity heartbeat after each step |
| Event replay | Temporal workflow replay on failure |
| Idempotency | Job id = SHA-256 of URL — safe to replay |
| Graceful shutdown | SIGTERM handled in all processes (Factor IX) |

---

## Single Docker Container Deployment

### Strategy

```
Stage 1 — node:22-alpine
  npm ci + next build → /app/frontend/out (static HTML/JS/CSS)

Stage 2 — python:3.14-slim
  Install: nginx, supervisor, curl, uv
  uv sync --no-dev
  playwright install chromium --with-deps
  Copy /out → /var/www/html
  Startup: supervisor → [migrate] → [nginx] → [fastapi]
  Port 80 exposed
```

### Process Startup Order (via Supervisor priority)

```
Priority 1: alembic upgrade head    (runs once, exits)
Priority 2: nginx                   (starts after migrate exits)
Priority 3: uvicorn fastapi         (starts after migrate exits)
```

### Request Routing

```
Browser → port 80 → Nginx
  /          → /var/www/html  (Next.js static export)
  /api/v1/*  → 127.0.0.1:8000 (FastAPI)
  /health    → 127.0.0.1:8000/health
```

### Dockerfile

```dockerfile
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM python:3.14-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx supervisor curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app/backend
COPY backend/pyproject.toml ./
RUN uv sync --no-dev
COPY backend/ .
RUN uv run playwright install chromium --with-deps

COPY --from=frontend-builder /app/frontend/out /var/www/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### nginx.conf

```nginx
events {}
http {
  include /etc/nginx/mime.types;
  default_type application/octet-stream;
  server {
    listen 80;
    location / {
      root /var/www/html;
      index index.html;
      try_files $uri $uri/ $uri.html /index.html;
    }
    location /api/ {
      proxy_pass http://127.0.0.1:8000;
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
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

### docker-compose.yml

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

### next.config.ts

```typescript
import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  output: "export",
  reactStrictMode: true,
  trailingSlash: true,
};
export default nextConfig;
```

Note: `output: "export"` disables Server Actions and Route Handlers. All dynamic data is fetched client-side from FastAPI at `/api/v1/*`.

---

## Environment Variables

```bash
# Supabase
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=postgresql+asyncpg://...

# LLM providers
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
LITELLM_API_BASE=

# Redis
REDIS_URL=redis://localhost:6379

# Temporal
TEMPORAL_SERVER_URL=

# Observability
OTEL_EXPORTER_OTLP_ENDPOINT=
SENTRY_DSN=

# Analytics
NEXT_PUBLIC_CLARITY_PROJECT_ID=

KONG_ADMIN_URL=
KONG_PROXY_URL=

# Frontend
NEXT_PUBLIC_API_URL=/api/v1
```

All variables typed and validated at startup via Pydantic Settings:

```python
# backend/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    database_url: str
    redis_url: str
    otel_exporter_otlp_endpoint: str
    # ... all other vars

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## CI/CD Pipeline

```yaml
steps:
  - Checkout
  - Lint: Ruff (backend) + ESLint (frontend)
  - Type check: mypy (backend) + tsc --noEmit (frontend)
  - Unit tests: pytest + Vitest
  - Security scan: Trivy (image) + Bandit (Python) + OWASP dependency check
  - Docker multi-stage build — tag with commit SHA
  - Terraform validate and plan (Azure)
  - Prompt regression tests: DeepEval per agent — fail if threshold drops
  - Ragas retrieval eval — fail if precision < 0.80
  - Integration tests: FastAPI TestClient + Playwright E2E
  - Docker push to registry — on merge to main
  - Deploy to Azure Container Apps — on merge to main
```

---

## Delivery Milestones

### MVP1 — Scraper and In-Memory Store
LinkedIn and JobServe scraper agents. Extensible `BaseScrapeAgent` registry. Keyword filter. FastAPI with `/api/v1/` prefix. Next.js dashboard. In-memory fake database. Single Docker container. Port 3020 frontend, port 8000 backend locally.

### MVP 1.1 — Advanced Prompt Engineering
Implementation of `job-discovery/prompts` infrastructure. Versioned system prompts with Contract and Changelog management. Initial prompt-based relevance filtering (heuristic-heavy) and evaluation using DeepEval and Ragas.

### MVP2 — AI Ranking, Infrastructure, and Persistence

- Replace fake database with Supabase PostgreSQL and pgvector
- Add Alembic migrations
- Implement AI ranking pipeline with embeddings and reranking
- Add Terraform deployment support
- Azure Container Apps deployment
- AWS ECS Fargate deployment
- Multi-cloud portability via Terraform
- Microsoft Clarity integration
- OWASP security middleware
- Docker image signing
- Circuit breaker implementation
- Retry orchestration
- Serverless AI ranking support
- AWS Lambda / Azure Functions integration
- Advanced domain models
- Backup and recovery validation
- Proxy abstraction layer
- Residential proxy support
- Production concurrency improvements
- Connection pool tuning

### MVP3 — Advanced Observability and Security

- Full Twelve-Factor compliance
- OpenTelemetry integration
- Grafana dashboards
- Prometheus metrics
- Loki log aggregation
- Sentry integration
- RBAC support
- Row-Level Security
- JWT authentication
- Structured admin process tooling
- Enhanced operational monitoring

### MVP4 — Application Workflow and Interview Preparation

### MVP5 — Security Hardening and Production Polish

---

## How to Add a New Job Board

When a new job board needs to be supported (e.g. Reed.co.uk, CWJobs, Totaljobs):

1. Create `backend/agents/{name}/` directory
2. Create `backend/agents/{name}/AGENT.md` — scraping spec, selectors, anti-bot rules
3. Create `backend/agents/{name}/{name}_agent.py` — implement `BaseScrapeAgent`, decorate with `@register`
4. Create `prompts/{name}-agent/` — `CONTRACT.md`, `CHANGELOG.md`, `system.md`
5. Add one import line to `backend/main.py`: `import agents.{name}.{name}_agent  # noqa: F401`
6. Add one entry to `backend/agents/AGENT.md` registered agents table
7. Run CI — all existing tests pass, new agent is included in scrape automatically

Zero changes required to: router, orchestrator, database schema, frontend, Dockerfile, or any other agent.

---

## Execution Rules

### You MUST
- use Python 3.14 with uv as the sole package manager
- use Next.js 16 and React 19 with all four specified hooks
- run the frontend on port 3020 in development
- prefix all API routes with `/api/v1/`
- implement `BaseScrapeAgent` for all scraper agents without exception
- import `get_logger` from `logging_config.py` in all agents — no `print()` calls
- run Alembic migrations before uvicorn starts via Supervisor priority
- write all logs to stdout as structured JSON
- define all admin processes in `backend/admin/` tracked in version control
- implement graceful SIGTERM handling in all long-running processes
- implement cursor-based pagination on all list endpoints
- set asyncpg pool_size, max_overflow, and pool_timeout explicitly
- validate all environment variables at startup via Pydantic Settings

### You MUST NOT
- auto-apply to any job under any circumstance
- bypass CAPTCHA or anti-bot systems
- fabricate metrics, scores, or retrieval results
- expose secrets in any file, log, or image layer
- use `print()` in any module — use the shared JSON logger
- hardcode any scraper source name in the router or orchestrator
- skip Factor VI process isolation — scraper agents run in Temporal workers, not uvicorn
- skip API versioning — all routes must include `/v1/`
- leave connection pool configuration at framework defaults


---

# Appendix — Approved Improvements and Architectural Enhancements

# Project Proposal Updates — Approved Improvements

## Disaster Recovery and Backup Restore

### Recovery Objectives

| Metric | Target |
|---|---|
| Recovery Point Objective (RPO) | <= 15 minutes |
| Recovery Time Objective (RTO) | <= 1 hour |

### Backup Strategy

| Component | Strategy |
|---|---|
| Supabase PostgreSQL | Continuous WAL backups + daily snapshots |
| Redis | AOF persistence + snapshot backups |
| Terraform State | Remote encrypted state storage with versioning |
| Docker Images | Immutable image registry with SHA tagging |
| Prompt Definitions | Git version controlled |

### Restore Workflow

1. Restore latest PostgreSQL snapshot
2. Replay WAL logs to desired recovery point
3. Restore Redis persistence snapshot
4. Redeploy infrastructure via Terraform
5. Deploy latest stable Docker image by commit SHA
6. Run health checks and workflow replay validation
7. Resume Temporal workers and scheduled jobs

### Disaster Recovery Validation

- Quarterly backup restore drills
- Automated infrastructure recovery validation in staging
- Periodic database consistency verification
- Recovery runbooks stored in version control

---

# Feature Flag Strategy

Feature flags are required for controlled rollout of AI agents, experimental workflows, and infrastructure migrations.

## Use Cases

| Feature | Flag Example |
|---|---|
| Ranking Agent | `feature_ranking_agent` |
| Cover Letter Generation | `feature_cover_letter_agent` |
| Question Answer Agent | `feature_question_answer_agent` |
| Interview Preparation | `feature_interview_prep` |
| New Scraper Agent | `feature_scraper_reed` |
| Azure Function Ranking | `feature_serverless_ranking` |

## Architecture

Recommended approaches:

- OpenFeature-compatible provider
- LaunchDarkly integration (optional)
- Database-backed feature flag table for self-hosted mode

Feature flags are evaluated server-side in FastAPI middleware and propagated to frontend feature gates.

## Rollout Strategy

- Internal-only rollout
- Percentage rollout
- Per-user rollout
- Canary deployment validation
- Emergency kill-switch support

---

# Outbound Scraping Rate Limiting Strategy

Inbound API throttling alone is insufficient. Outbound scraping protection is required to avoid resource exhaustion and anti-bot detection.

## Domain-Level Controls

| Control | Strategy |
|---|---|
| Per-domain concurrency | Max 1–3 active sessions per domain |
| Request pacing | Randomized delay between actions |
| Retry policy | Exponential backoff with jitter |
| Failure threshold | Circuit breaker after repeated failures |
| Session rotation | New browser context periodically |

## Adaptive Throttling

The scraper dynamically reduces concurrency when:

- CAPTCHA frequency increases
- HTTP 429 responses increase
- DOM stability decreases
- Response latency spikes

## Queue Management

Temporal workflows enqueue scraping jobs with:

- concurrency caps
- retry ceilings
- dead-letter queue routing
- priority-based scheduling

---

# Anti-Bot, Proxy, and Fingerprinting Disclaimer

The platform explicitly avoids bypassing CAPTCHA systems or violating platform restrictions.

## Operational Constraints

- Respect robots.txt where legally required
- No CAPTCHA solving or bypassing
- No authenticated LinkedIn scraping
- No credential sharing or automation abuse

## Browser Fingerprinting Strategy

The platform may support:

- User-agent rotation
- Viewport randomisation
- Browser context isolation
- Proxy abstraction layer
- Residential proxy support (optional)

These capabilities exist solely to reduce false-positive bot detection and improve browser stability.

## Compliance Disclaimer

Each job board has independent Terms of Service and anti-automation policies. Users are responsible for ensuring lawful usage in their jurisdiction.

---

# Domain Model Definitions

## Core Entities

### Job

Represents a discovered job listing.

| Field | Type |
|---|---|
| id | UUID |
| source | string |
| title | string |
| company | string |
| recruiter_id | UUID nullable |
| description | text |
| url | string |
| salary_range | JSONB |
| created_at | timestamp |
| embedding | vector |

### Recruiter

Represents recruiter metadata and interaction history.

| Field | Type |
|---|---|
| id | UUID |
| name | string |
| company | string |
| linkedin_url | string |
| notes | text |
| interaction_score | float |

### Application

Tracks application workflow state.

| Field | Type |
|---|---|
| id | UUID |
| user_id | UUID |
| job_id | UUID |
| status | enum |
| applied_at | timestamp |
| response_received | boolean |
| interview_stage | string nullable |

### CV

Stores CV metadata and embeddings.

| Field | Type |
|---|---|
| id | UUID |
| user_id | UUID |
| filename | string |
| parsed_text | text |
| embedding | vector |
| uploaded_at | timestamp |

### CoverLetter

Generated cover letter linked to a job.

| Field | Type |
|---|---|
| id | UUID |
| job_id | UUID |
| content | text |
| ats_score | float |
| generated_at | timestamp |

### InterviewPrep

Generated preparation pack.

| Field | Type |
|---|---|
| id | UUID |
| job_id | UUID |
| technical_questions | JSONB |
| behavioural_questions | JSONB |
| company_research | JSONB |
| generated_at | timestamp |

### ScrapeRun

Tracks execution of scraper workflows.

| Field | Type |
|---|---|
| id | UUID |
| source | string |
| status | enum |
| started_at | timestamp |
| completed_at | timestamp |
| jobs_inserted | integer |
| errors | JSONB |

---

# AI Ranking Execution Model

AI ranking and relevance scoring operate asynchronously.

## Architecture

1. Scraper agent inserts raw jobs
2. Temporal workflow emits ranking task
3. Ranking worker processes embeddings and reranking
4. Ranked jobs become searchable only after scoring completes

## Serverless Execution (Optional)

Heavy inference workloads may execute using:

- Azure Functions
- AWS Lambda

This enables:

- burst scaling
- reduced idle compute cost
- isolation of expensive AI workloads
- independent deployment lifecycle

## API Behaviour

`POST /api/v1/scrape` returns immediately after scrape scheduling.

Ranking status is tracked asynchronously:

```json
{
  "scrape_id": "uuid",
  "status": "ranking_in_progress"
}
```

The frontend polls or subscribes to status updates.

---

# Data Ownership and Portability

Users retain full ownership of their uploaded and generated data.

## Supported Export Capabilities

| Resource | Export Format |
|---|---|
| CVs | PDF / DOCX |
| Applications | JSON / CSV |
| Cover Letters | Markdown / PDF |
| Interview Packs | Markdown / PDF |
| Recruiter Interactions | JSON |

## Deletion Capabilities

Users may permanently delete:

- CVs
- embeddings
- recruiter interactions
- generated content
- application history

Deletion propagates through:

- PostgreSQL records
- pgvector embeddings
- Redis caches
- object storage
- observability metadata where legally permitted

## GDPR Compliance

The platform supports:

- right to export
- right to deletion
- consent withdrawal
- retention expiry policies
- audit logging for data access

---

# Docker Deployment Terminology Update

The previous “Single Docker Container Deployment” terminology is replaced with a clearer deployment model distinction.

## Local Development Deployment

Docker Compose is the primary local development environment:

- frontend
- backend
- Redis
- Temporal
- observability stack

This provides reproducible local development and CI parity.

## Production Deployment

Production environments use distributed container-based services:

| Environment | Strategy |
|---|---|
| Azure | Azure Container Apps |
| AWS | ECS Fargate |

Production services scale independently:

- API containers
- Temporal workers
- scraper workers
- ranking workers
- observability services

Docker remains the standard packaging and runtime format across all environments.

# Local LLM Runtime Support

The platform supports optional local open-source LLM inference using llama.cpp-compatible runtimes with GGUF quantized models.

## Capabilities

- Local inference execution for AI agents
- KV cache reuse for faster multi-agent reasoning and RAG chains
- GPU acceleration support
- OpenAI-compatible local inference APIs
- Use OpenRouter for the AI calls. An OPENROUTER_API_KEY is in .env in the project root
- Use openai/gpt-oss-120b as the model
- Start and Stop server scripts for Mac, PC, Linux in scripts/
- Use "uv" as the package manager for python in the Docker container
- Everything packaged into a Docker container
- Hybrid local/cloud model routing through LiteLLM

Benefits include reduced latency, lower token costs, privacy-friendly processing, and offline-capable AI workflows.

**📌 CRITICAL References:**

- MUI Box docs: https://mui.com/material-ui/react-box/
- MUI theme provider docs: https://mui.com/material-ui/customization/theming/
- Microsoft Entra ID (Identity & Access) docs: https://aka.ms/entra-id-docs/
- Google Cloud Identity & OAuth docs: https://cloud.google.com/identity/docs
- OpenAI Prompt Guidance docs: https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.5
- Claude Prompt Engineering Best Practices docs: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

