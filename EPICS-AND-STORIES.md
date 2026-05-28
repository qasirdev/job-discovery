# Epics, Stories and Tasks — AI-Powered Job Discovery Platform

**Proposal:** 004-01-saas-job-search-proposal-v4.md (v1.2.0)
**Total Epics:** 37 | **Total Tasks:** 152

---

## Cross-MVP — Architectural Patterns & Feedback Loops

### E25 — Presenter Role — Progressive Pattern

- **25.1** `MVP 1 Inline Presenter for Doer Agents` — ensure each Doer agent formats its own output directly as a Pydantic model (zero-refactor future composition).
- **25.2** `MVP 2 Orchestrator-as-Presenter` — aggregate multi-agent outputs into a unified response envelope via Orchestrator.
- **25.3** `Post-MVP 3 Dedicated Presenter (Application Assistant)` — implement application_assistant agent to synthesize cover letter, interview prep, and company research into a compound package.

### E26 — Learner Feedback Loops

- **26.1** `Wire RAG Agent feedback to downstream agents` — pass cv_embeddings context from RAG to Cover Letter, Q&A, Ranking, and Interview Prep via Orchestrator using the 4-step Feedback Protocol.
- **26.2** `Wire Interview Prep research to Presenter` — pass CompanyResearch record to Application Assistant (Presenter).
- **26.3** `Expose retrieval precision scores to Quality Critic and Observability` — expose RAG Agent retrieval precision scores to Quality Critic and Observability, logged to Prometheus and eval_metrics, and alert if < 0.80.
- **26.4** `Connect Interview Prep question bank to Q&A agent` — route interview questions to Q&A agent for follow-up answers.

### E27 — Agent Activation Timeline

- **27.1** `Implement feature-flag-gated agent activation framework` — use FEATURE_* env vars in settings.py to control agent activation.
- **27.2** `Configure graceful degradation for missing MVP 3+ agents` — ensure MVP 2 agents gracefully degrade if MVP 3+ agents are unavailable.
- **27.3** `Enforce Agent Dependency and Scaling Constraints` — enforce explicit scaling rules ensuring MVP 1 agents do not depend on MVP 2+ agents, and agent count does not exceed 15 (each new agent must justify its existence in the 7-role framework).

---

## MVP 1 — Scraper Foundation & In-Memory Store

### E1 — Project Scaffold & Docker Setup

- **1.1** `Monorepo init` — create the job-discovery/ root directory with required base files.
- **1.2** `Nginx reverse proxy` — create nginx.conf routing / to Next.js Node server on port 3000 and /api/* to FastAPI on port 8000.
- **1.3** `docker-compose.yml` — create docker-compose.yml for local development orchestration.
- **1.4** `next.config.ts standalone output` — configure next.config.ts with output: standalone so Next.js produces a self-contained Node.js server.

### E2 — Backend Core

- **2.1** `FastAPI entrypoint` — create backend/main.py as the FastAPI application entrypoint with agent auto-discovery and router mounting.
- **2.2** `Pydantic Settings` — create backend/settings.py with Pydantic BaseSettings class for typed, validated environment variables.
- **2.3** `Structured JSON logger` — create backend/logging_config.py with shared structured JSON logger satisfying Twelve-Factor XI.
- **2.4** `Domain models` — create backend/models/ with Pydantic v2 domain models covering all MVP 1 entities and MVP 2 shapes.
- **2.5** `Keyword filter` — create backend/filters.py with keyword-based relevance pre-filtering; supports UserProfile merge in MVP 1.1.
- **2.6** `File-backed fake DB` — implement fake_db.json file-backed store in backend/fake_db.py as the explicit MVP 1 persistence layer.

### E3 — Extensible Scraper Registry

- **3.1** `BaseScrapeAgent ABC` — create backend/agents/base.py defining the abstract base class all scraper agents must implement.
- **3.2** `Registry module` — create backend/agents/registry.py with @register decorator and agent discovery functions.
- **3.3** `LinkedIn scraper agent` — create backend/agents/linkedin/linkedin_agent.py implementing BaseScrapeAgent for UK senior job scraping.
- **3.4** `JobServe scraper agent` — create backend/agents/jobserve/jobserve_agent.py implementing BaseScrapeAgent for UK contract job scraping.
- **3.5** `Scrape router with concurrency guard` — create backend/routers/v1/scrape.py with registry-driven POST /api/v1/scrape endpoint and asyncio.Lock concurrency guard.

### E4 — Next.js Frontend Dashboard

- **4.1** `Next.js 16 scaffold` — scaffold frontend/ with Next.js 16, React 19, TypeScript, Tailwind CSS 4, MUI 7, TanStack Query v5, Zustand, and Zod.
- **4.2** `App router page structure` — create all MVP 1 app/ pages and route layout following the proposal file tree.
- **4.3** `OnboardingBanner component` — create frontend/components/OnboardingBanner.tsx that guides users through profile + CV setup using shared query keys.
- **4.4** `ProfileForm and CVUploadPanel components` — create frontend/components/ProfileForm.tsx and frontend/components/CVUploadPanel.tsx for user onboarding and profile editing.
- **4.5** `SavedJobsList and ApplicationBoard components` — create frontend/components/SavedJobsList.tsx and frontend/components/ApplicationBoard.tsx.
- **4.6** `RecruiterCard and AdminPanel components` — create frontend/components/RecruiterCard.tsx and frontend/components/AdminPanel.tsx.
- **4.7** `JobCard component` — create frontend/components/JobCard.tsx displaying job details with Save toggle and job detail navigation.
- **4.8** `FilterBar component` — create frontend/components/FilterBar.tsx with source and keyword client-side filters backed by Zustand.
- **4.9** `ScrapeButton component` — create frontend/components/ScrapeButton.tsx triggering POST /api/v1/scrape with in-progress and result states.
- **4.10** `Refine OnboardingBanner states` — update frontend/components/OnboardingBanner.tsx to implement the exact 5 states and query key contracts as specified in proposal v1.5.0.
- **4.11** `Refine Profile page logic` — update frontend/app/profile/page.tsx to pass appropriate handlers based on GET response.

### E5 — Versioned API & CI Skeleton

- **5.1** `Jobs router` — create backend/routers/v1/jobs.py with paginated job listing, job detail, save/unsave, and saved jobs list endpoints.
- **5.2** `Profile and CV endpoints` — create backend/routers/v1/profile.py and backend/routers/v1/cv.py for user profile management and CV upload.
- **5.3** `OpenAPI spec completeness` — ensure all routes are fully typed with Pydantic request/response models and RFC 7807 error shapes.
- **5.4** `Admin process scripts` — create backend/admin/ directory with seed_keywords.py, clear_db.py, and stubs for replay_dlq.py and run_evals.py.
- **5.5** `GitHub Actions CI skeleton` — create .github/workflows/ci.yml using reusable workflow patterns with linting, type checking, tests, and Docker build.
- **5.6** `Applications endpoint` — create backend/routers/v1/applications.py for logging and tracking applications.
- **5.7** `Application GET and PATCH endpoints` — create backend endpoints to support ApplicationBoard and ApplicationDetail components.

### E16 — Workflow Orchestration Infrastructure

- **16.1** `Active Task Plan (todo.md)` — create docs/tasks/todo.md with the correct structure for AI-agent task tracking.
- **16.2** `Lessons Log (lessons.md)` — create docs/tasks/lessons.md for self-improvement logging after every user correction.
- **16.3** `Root AGENT.md Workflow Rules` — update root AGENT.md to include Workflow Rules table and expanded Where-to-look index.
- **16.4** `EXECUTION-RULES.md Workflow Section` — create docs/EXECUTION-RULES.md with Final Execution Rules and Workflow Execution Rules.
- **16.5** `Backend Agents AGENT.md Subagent Rules` — create backend/agents/AGENT.md with cross-agent rules and Subagent Execution Rules section.
- **16.6** `CI Workflow Docs Enforcement` — add check-workflow-docs step to .github/workflows/ci.yml that fails if docs/tasks/todo.md or docs/tasks/lessons.md is missing or empty.

### E17 — MVP 1 Documentation Additions

- **17.1** `Create docs/ANTI-BOT.md` — create docs/ANTI-BOT.md to document the anti-bot, proxy, and fingerprinting disclaimer details.

---

## MVP 1.1 — Advanced Prompt Engineering Infrastructure

### E7 — Eval Framework (DeepEval + Ragas)

- **7.1** `Eval runner script` — implement backend/admin/run_evals.py (replacing the stub from JD-30) for per-agent eval set execution with field-level output comparison.
- **7.2** `DeepEval and Ragas integration` — wire DeepEval faithfulness and relevance metrics plus Ragas retrieval metrics into the eval runner.
- **7.3** `CI prompt regression step` — add eval-regression job to .github/workflows/ci.yml to block deploy if agent output quality drops below threshold.

---

## MVP 1.4b

### E6 — Prompts Directory & Versioning Framework

- **6.1** `Prompts root scaffold` — create prompts/AGENT.md with XML prompt structure standard, reasoning effort matrix, versioning convention, and authoring rules.
- **6.2** `LinkedIn agent prompts` — create prompts/linkedin-agent/ directory with all six required prompt files.
- **6.3** `JobServe agent prompts` — create prompts/jobserve-agent/ directory with the same six-file structure as the LinkedIn agent.
- **6.4** `CONTRACT.md template` — define the reusable CONTRACT.md template in prompts/AGENT.md with all required fields and a filled example.
- **6.5** `Prompt-based relevance filtering` — activate the filters.py MVP 1.1 profile merge hook and create per-agent filtering prompt files.
- **6.6** `require_rag_ready FastAPI dependency` — create backend/routers/dependencies.py with the require_rag_ready FastAPI dependency for enforcing CV + profile prerequisites.

---

## MVP 2 — AI Ranking, Persistence & Cloud Infrastructure

### E8 — Supabase PostgreSQL & Alembic

- **8.1** `Replace fake_db with Supabase` — migrate all data storage from the file-backed in-memory fake_db.json to Supabase PostgreSQL with pgvector extension.
- **8.2** `asyncpg connection pool` — create backend/db.py with SQLAlchemy 2 async engine and explicitly tuned asyncpg connection pool as specified in backend/AGENT.md.
- **8.3** `Full domain models` — expand backend/models/ with all MVP 2 domain models using SQLAlchemy 2 mapped_column syntax and Pydantic v2 schemas in backend/schemas/.
- **8.4** `Create backend/models/DOMAIN-MODELS.md` — create backend/models/DOMAIN-MODELS.md to document domain model definitions explicitly as specified in proposal v1.5.0, including new fields like Job company_name_slug and optional recruiter_id foreign key, and all other entities like SavedJob, InteractionEvent, interview_questions, eval_metrics, and cv_embeddings.
- **8.5** `Create recruiters.py router` — create backend/routers/v1/recruiters.py for MVP 2 recruiter endpoints including GET list, upsert with linkedin_url deduplication, notes updates, and interaction logging.
- **8.6** `Create company_research.py router` — create backend/routers/v1/company_research.py with idempotent GET endpoint for company research data.
- **8.7** `Create interview.py router` — create backend/routers/v1/interview.py for MVP 2 interview prep endpoint returning 503 until fully active.

### E9 — AI Ranking & RAG Agents

- **9.1** `Ranking agent` — build backend/agents/ranking/ranking_agent.py with the 8-step AI relevance scoring pipeline as specified in backend/agents/ranking/AGENT.md.
- **9.2** `RAG agent` — build backend/agents/rag/rag_agent.py with contextual retrieval from CV, applications, recruiter data, and saved jobs as specified in backend/agents/rag/AGENT.md.
- **9.3** `Cover letter agent` — build backend/agents/cover-letter/cover_letter_agent.py with ATS-optimised generation following the 6-section playbook in backend/agents/cover-letter/AGENT.md.
- **9.4** `Question answer agent` — build backend/agents/question-answer/question_answer_agent.py for RAG-grounded Q&A on specific job listings as specified in backend/agents/question-answer/AGENT.md.
- **9.5** `Ragas eval in CI` — add Ragas retrieval precision and context recall metrics to the CI eval pipeline, blocking deployment if thresholds are not met.
- **9.6** `require_rag_ready FastAPI dependency` — implement the require_rag_ready dependency in backend/routers/dependencies.py to enforce CV + profile prerequisites at the API layer before any RAG-dependent endpoint executes.

### E10 — Security & Orchestration Agents

- **10.1** `Security agent` — build backend/agents/security/security_agent.py with comprehensive input validation, prompt injection defence, and OWASP middleware as specified in backend/agents/security/AGENT.md and docs/SECURITY.md.
- **10.2** `Workflow orchestrator` — build backend/agents/orchestrator/orchestrator_agent.py using Temporal for reliable multi-agent workflow coordination (including AgentResultEnvelope parsing, Critic Revision Protocol, and Learner Feedback Loops) as specified in backend/agents/orchestrator/AGENT.md.
- **10.3** `Circuit breakers` — implement per-agent circuit breakers with configurable failure thresholds, state logging, token budget enforcement (2x alert_threshold), and exponential backoff, wrapping each agent.run() call in the orchestrator.
- **10.4** `Admin DLQ routes` — create admin API routes for DLQ inspection, retry, and discard, plus the replay_dlq.py admin script, and the frontend/app/admin/page.tsx admin panel wired to these routes.

### E11 — Terraform & Multi-Cloud Deployment

- **11.1** `Azure Container Apps Terraform` — create infrastructure/terraform/azure/ with main.tf, variables.tf, and outputs.tf for Azure Container Apps deployment as specified in infrastructure/AGENT.md.
- **11.2** `AWS ECS Fargate Terraform` — create infrastructure/terraform/aws/ with main.tf, variables.tf, and outputs.tf for AWS ECS Fargate deployment as specified in infrastructure/AGENT.md.
- **11.3** `Terraform CI steps` — add Terraform validate, plan, and apply steps to .github/workflows/ci.yml for both azure/ and aws/ modules, with manual approval gate before apply.
- **11.4** `Docker image signing` — configure GitHub Actions to build, tag, sign, and push Docker images to ACR and ECR on merge to main, using cosign keyless signing via GitHub OIDC.
- **11.5** `Helm chart scaffold` — create infrastructure/helm/job-discovery/ with Chart.yaml and values.yaml as the Helm deployment scaffold for MVP 2+ Kubernetes targets.

### E12 — MVP 2 Prompts for AI Agents

- **12.1** `Ranking agent prompts` — create prompts/ranking-agent/ with CONTRACT.md, CHANGELOG.md, system.md, scoring.md, reranking.md, and filtering.md.
- **12.2** `RAG agent prompts` — create prompts/rag-agent/ with CONTRACT.md, CHANGELOG.md, system.md, retrieval.md, embeddings.md, and personalization.md.
- **12.3** `Cover letter agent prompts` — create prompts/cover-letter-agent/ with CONTRACT.md, CHANGELOG.md, system.md, tone.md, generation.md, and templates.md.
- **12.4** `Question answer & security agent prompts` — create prompts/question-answer-agent/ and prompts/security-agent/ with all required prompt files.
- **12.5** `Orchestrator prompts` — create prompts/orchestrator/ with CONTRACT.md, CHANGELOG.md, system.md, skills.md, tools.md, and guardrails.md (including Critic Revision Protocol, Token Budget Enforcement, and Learner Feedback Loops) at xhigh reasoning effort for long-horizon multi-step workflow coordination.
- **12.6** `Quality Critic agent prompts` — create prompts/quality-critic-agent/ with all required prompt files.

### E18 — MVP 2 Infrastructure & Rate Limiting Docs

- **18.1** `Create docs/FEATURE-FLAGS.md` — create docs/FEATURE-FLAGS.md to define the Feature Flag Strategy.
- **18.2** `Create docs/SCRAPING-RATE-LIMITS.md` — create docs/SCRAPING-RATE-LIMITS.md for outbound scraping rate limiting strategy.
- **18.3** `Create infrastructure/LOCAL-LLM.md` — create infrastructure/LOCAL-LLM.md for local LLM runtime support details, including privacy-friendly workflows, the use of "uv", and Docker container packaging.
- **18.4** `Create Local LLM Start Scripts` — create start/stop server scripts for Mac, PC, and Linux in the scripts/ directory, implementing llama.cpp-compatible runtime support with GGUF quantized models (openai/gpt-oss-120b), including OpenAI-compatible local inference APIs, OpenRouter integration with OPENROUTER_API_KEY, KV cache reuse, GPU acceleration, hybrid local/cloud routing via LiteLLM, privacy-friendly processing, offline-capable AI workflows, using 'uv' as the package manager for Python inside the Docker container, and everything packaged into a Docker container.

### E22 — API Gateway & Rate Limiting Infrastructure

- **22.1** `Implement Per-Endpoint Rate Limiting` — implement per-endpoint rate limits enforced at the API Gateway level or via FastAPI middleware as specified in proposal v1.5.0 Rate Limiting Strategy.
- **22.2** `Configure API Gateway Plugins` — configure API Gateway concern layer with the five specified plugins as documented in infrastructure/AGENT.md.
- **22.3** `Implement Proxy Abstraction Layer` — build the proxy abstraction layer for outbound scraping requests with residential proxy support as specified in docs/ANTI-BOT.md and proposal v1.5.0.

### E23 — Serverless AI Ranking & Deployment Enhancements

- **23.1** `Serverless AI Ranking Support` — configure the AI ranking pipeline for serverless/burst execution to enable cost-efficient scaling of expensive AI workloads.
- **23.2** `Release Tagging & Rollback Strategy` — implement Git SHA-based release tagging and document the rollback deployment strategy as specified in infrastructure/AGENT.md proposal v1.5.0.
- **23.3** `Update Deployment Topology Documentation` — update infrastructure/AGENT.md with production services that scale independently and the API Gateway concern table as specified in proposal v1.5.0.

### E24 — Frontend Component Refinements

- **24.1** `Refine CoverLetterViewer error handling` — update frontend/components/CoverLetterViewer.tsx to implement exact export fallback handling.
- **24.2** `Refine Application tracking logic` — update frontend/app/applications/page.tsx logic for handling existing applications.
- **24.3** `Refine Job Detail Interview Prep states` — update frontend/app/jobs/[id]/page.tsx to implement exact CompanyResearch states for the Interview Prep feature.

---

## MVP2

### E28 — Agent Communication Protocol

- **28.1** `Define AgentResultEnvelope schema` — create Pydantic implementation in backend/schemas/agent_envelope.py.
- **28.2** `Refactor BaseScrapeAgent to return AgentResultEnvelope` — update BaseScrapeAgent.run() and all existing agents to return the new envelope.
- **28.3** `Create BaseAgent ABC for non-scraper agents` — create backend/agents/base.py BaseAgent ABC enforcing AgentResultEnvelope return type for all non-scraper agents.

### E29 — Critic Revision Protocol

- **29.1** `Implement bounded retry loop with max_revision_cycles=2` — orchestrator logic to retry Doer agents with critic feedback appended to context.
- **29.2** `Implement Security Agent override and DLQ escalation` — security Critic failures are never retried. Immediate escalation to DLQ.
- **29.3** `Log revision metrics for observability` — log each revision cycle, critic score, and rejection reasons.

### E30 — Token Budget Enforcement

- **30.1** `Implement token tracking and thresholds in Orchestrator` — track tokens_used against expected budget per agent role.
- **30.2** `Add circuit-breaking and DLQ routing on threshold breach` — circuit-break agent if usage > 2x alert threshold and escalate to DLQ.

### E31 — Model Selection Matrix

- **31.1** `Configure LiteLLM routing rules and models` — set primary and fallback models per agent based on reasoning complexity.
- **31.2** `Add support for MODEL_OVERRIDE env vars` — implement MODEL_OVERRIDE_{AGENT_ID} environment variables for hot-swapping models.

### E32 — EVAL COVERAGE MATRIX (MVP 2)

- **32.1** `Create eval sets for MVP 2 agents` — create evals for Ranking, Cover Letter, Q&A, Security, Quality Critic, Orchestrator.

### E33 — Quality Critic Agent

- **33.1** `Create Quality Critic agent directory and implementation` — create backend/agents/quality_critic/ directory with AGENT.md, __init__.py, quality_critic_agent.py.

### E34 — Orchestrator Planner

- **34.1** `Create planner.py for Orchestrator` — create backend/agents/orchestrator/planner.py to decompose goals and validate schemas.


---

## MVP 3 — Full Twelve-Factor Compliance, Observability & Auth

### E13 — Observability Stack

- **13.1** `OpenTelemetry integration` — integrate OpenTelemetry distributed tracing and metrics across all FastAPI routers and agent run() methods as specified in docs/OBSERVABILITY.md.
- **13.2** `Grafana dashboards` — create five Grafana dashboards as versioned JSON files in infrastructure/grafana/, covering API latency, AI agent performance, RAG quality, ranking, and infrastructure health.
- **13.3** `Prometheus & Loki` — configure Prometheus scraping and Loki log aggregation from structured JSON stdout.
- **13.4** `Sentry & Microsoft Clarity` — integrate Sentry for backend and frontend error tracking, and Microsoft Clarity for frontend session replay and UX analytics.
- **13.5** `Observability agent` — build backend/agents/observability/observability_agent.py for AI-specific reliability monitoring running as a periodic background task, as specified in backend/agents/observability/AGENT.md and docs/OBSERVABILITY.md.
- **13.6** `Create docs/OBSERVABILITY.md` — create docs/OBSERVABILITY.md as the single source of truth for all observability standards, tracked metrics, alerting thresholds, and Loki query examples for the platform.
- **13.7** `Create backend/agents/observability/AGENT.md` — create backend/agents/observability/AGENT.md to define the responsibilities, input/output schemas, and metric thresholds for the Observability agent as per proposal-v4-structure.md.
- **13.8** `Implement ObservabilityPanel.tsx` — implement frontend/components/ObservabilityPanel.tsx to display agent traces and token usage.

### E14 — Auth, RBAC, Row-Level Security & Agentic Consent

- **14.1** `Supabase Auth & JWT` — implement JWT validation middleware in FastAPI with RBAC enforced via JWT claims, as specified in docs/SECURITY.md.
- **14.2** `Row-Level Security` — configure Supabase RLS policies on all user-scoped tables so users can only read and write their own rows, with service role bypass for scraper agents.
- **14.3** `OWASP Top 10 hardening` — run Trivy container image scanning, Bandit static analysis, and Docker image signing in CI, configure SSRF allowlist, and wire Azure Key Vault secret references as specified in docs/SECURITY.md.
- **14.4** `GDPR compliance` — implement data export, deletion, and audit logging endpoints for GDPR compliance, as documented in docs/SECURITY.md data flow section.
- **14.5** `Create docs/SECURITY.md` — create docs/SECURITY.md as the single source of truth for all security standards, covering Supabase Auth, JWT, RBAC, RLS, OWASP Top 10 compliance, Identity-Centric Governance, prompt injection defence, and GDPR data flow documentation.
- **14.6** `Create docs/AGENTIC-CONSENT.md` — create docs/AGENTIC-CONSENT.md to document the Agentic Consent model as a dynamic, living contract.
- **14.7** `Implement ConsentPromptModal.tsx` — create frontend/components/ConsentPromptModal.tsx for JIT prompting when an agent requires human-in-the-loop approval.
- **14.8** `Implement Consent Dashboard` — create frontend/app/settings/consent/page.tsx as a Consent dashboard to manage and revoke active 'living contracts'.

### E15 — Twelve-Factor Completion & Admin Tooling

- **15.1** `Twelve-Factor audit` — audit all 12 Twelve-Factor App factors against the production Azure Container Apps deployment, close all identified gaps, and update docs/ENGINEERING-STANDARDS.md with final compliance status.
- **15.2** `Graceful shutdown` — implement SIGTERM handlers in all long-running processes: uvicorn drain, Temporal worker checkpoint, and Playwright browser session close, as documented in docs/RELIABILITY.md.
- **15.3** `Structured admin tooling` — fully implement replay_dlq.py and run_evals.py CLI scripts with complete flag support; wire schedule pause/resume admin API routes.
- **15.4** `Disaster recovery validation` — execute a documented backup restore drill for PostgreSQL WAL (Supabase PITR) and Redis AOF, validate RTO <= 1 hour and RPO <= 15 minutes, and update infrastructure/DISASTER-RECOVERY.md with results and exact restore commands.
- **15.5** `Create docs/ENGINEERING-STANDARDS.md` — create docs/ENGINEERING-STANDARDS.md as the authoritative reference for all frontend, backend, and database stack standards, and full Twelve-Factor compliance notes for all 12 factors.
- **15.6** `Create docs/RELIABILITY.md` — create docs/RELIABILITY.md documenting all reliability engineering standards including failure mode catalogue, DIFA framework, ReAct loop pattern, and circuit breaker configuration.

### E19 — MVP 3 Data Ownership & Disaster Recovery Docs

- **19.1** `Create docs/DATA-OWNERSHIP.md` — create docs/DATA-OWNERSHIP.md to detail data ownership and portability, including consent revocability, transparency of data flows, and fine-grained personalization.
- **19.2** `Create infrastructure/DISASTER-RECOVERY.md` — create infrastructure/DISASTER-RECOVERY.md to document full disaster recovery and backup restore details.

---

## MVP3

### E36 — EVAL COVERAGE MATRIX (MVP 3)

- **36.1** `Create eval set for Observability` — create evals/observability/eval-set-v1.json using DeepEval + Ragas metrics, ensure CONTRACT.md Eval Set Reference points to it, and runs successfully via CI.
- **36.2** `Create missing prompt directory for observability/` — create prompts/observability/ with all 6 required XML prompt files (CONTRACT.md, CHANGELOG.md, system.md, skills.md, tools.md, guardrails.md).

---

## Post-MVP 3 — Advanced Agents & Continuous Learning

### E37 — EVAL COVERAGE MATRIX (Post-MVP 3)

- **37.1** `Create evals/interview_prep/eval-set-v1.json` — create evals/interview_prep/eval-set-v1.json using DeepEval + Ragas metrics, ensure CONTRACT.md Eval Set Reference points to it, and runs successfully via CI.

---

## MVP 4

### E20 — Application Workflow & Interview Preparation

- **20.1** `Application Assistant Docs` — create backend/agents/application_assistant/AGENT.md and associated prompts/application_assistant/ structure.
- **20.2** `Interview Prep Agent Docs` — create backend/agents/interview_prep/AGENT.md and associated prompts/interview_prep/ structure.
- **20.3** `Build Application Assistant Agent` — implement the Autonomous Job Application Assistant Agent in Python.
- **20.4** `Build Interview Prep Agent` — implement the Interview Preparation Intelligence Agent.
- **20.5** `Enable Interview Prep Button` — finalize the frontend logic for the Interview Prep feature on the Job Detail page.
- **20.6** `Create Interview Prep Viewer UI` — create frontend/app/interview-prep/[id]/page.tsx to render generated interview intelligence with export fallback.
- **20.7** `Application Assistant UI Integration` — update frontend/app/applications/[id]/page.tsx to display synthesised application package.
- **20.8** `Eval Sets for MVP 4 Agents` — create DeepEval+Ragas eval sets for Application Assistant and Interview Prep agents.
- **20.9** `Wire MVP 4 Patterns` — implement cross-cutting patterns: Dedicated Presenter, Interview Prep research wiring, and question bank routing.

---

## MVP 5

### E21 — Security Hardening and Production Polish

- **21.1** `Finalize Production Deployment Topology` — review and finalize the highly available deployment architecture for production launch.
- **21.2** `Comprehensive Security Audit` — conduct a final security audit of all Prompt Injection Defenses, RBAC rules, RLS policies, and OWASP mitigations.
- **21.3** `UI/UX Production Polish` — polish all frontend views to ensure a premium, production-ready user experience.

