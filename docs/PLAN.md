# Auto-Mode Implementation Plan: AI-Powered Job Discovery Platform

## 🤖 System Prompt for AI Agent (Cursor, Windsurf, Antigravity, Claude, GPT, etc.)

You are operating in an autonomous "Auto/YOLO" mode to implement the **AI-Powered Job Discovery Platform**.
Your source of truth for the architecture, project structure, and requirements are the following files in the project root:
- `docs/proposal-v4-structure.md`
- `docs/tasks/todo.md`
- `docs/tasks/lessons.md`
- `docs/jira-tickets/*.csv`


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
- [ ] **Step 1.1:** Monorepo init. Create the job-discovery/ root directory with required base files.
- [ ] **Step 1.2:** Nginx reverse proxy. Create nginx.conf routing / to Next.js Node server on port 3000 and /api/* to FastAPI on port 8000.
- [ ] **Step 1.3:** docker-compose.yml. Create docker-compose.yml for local development orchestration.
- [ ] **Step 1.4:** next.config.ts standalone output. Configure next.config.ts with output: standalone so Next.js produces a self-contained Node.js server.

### Epic 2: Backend Core
- [ ] **Step 2.1:** FastAPI entrypoint. Create backend/main.py as the FastAPI application entrypoint with agent auto-discovery and router mounting.
- [ ] **Step 2.2:** Pydantic Settings. Create backend/settings.py with Pydantic BaseSettings class for typed, validated environment variables.
- [ ] **Step 2.3:** Structured JSON logger. Create backend/logging_config.py with shared structured JSON logger satisfying Twelve-Factor XI.
- [ ] **Step 2.4:** Domain models. Create backend/models/ with Pydantic v2 domain models covering all MVP 1 entities and MVP 2 shapes.
- [ ] **Step 2.5:** Keyword filter. Create backend/filters.py with keyword-based relevance pre-filtering; supports UserProfile merge in MVP 1.1.
- [ ] **Step 2.6:** File-backed fake DB. Implement fake_db.json file-backed store in backend/fake_db.py as the explicit MVP 1 persistence layer.

### Epic 3: Extensible Scraper Registry
- [ ] **Step 3.1:** BaseScrapeAgent ABC. Create backend/agents/base.py defining the abstract base class all scraper agents must implement.
- [ ] **Step 3.2:** Registry module. Create backend/agents/registry.py with @register decorator and agent discovery functions.
- [ ] **Step 3.3:** LinkedIn scraper agent. Create backend/agents/linkedin/linkedin_agent.py implementing BaseScrapeAgent for UK senior job scraping.
- [ ] **Step 3.4:** JobServe scraper agent. Create backend/agents/jobserve/jobserve_agent.py implementing BaseScrapeAgent for UK contract job scraping.
- [ ] **Step 3.5:** Scrape router with concurrency guard. Create backend/routers/v1/scrape.py with registry-driven POST /api/v1/scrape endpoint and asyncio.Lock concurrency guard.

### Epic 4: Next.js Frontend Dashboard
- [ ] **Step 4.1:** Next.js 16 scaffold. Scaffold frontend/ with Next.js 16, React 19, TypeScript, Tailwind CSS 4, MUI 7, TanStack Query v5, Zustand, and Zod.
- [ ] **Step 4.2:** App router page structure. Create all MVP 1 app/ pages and route layout following the proposal file tree.
- [ ] **Step 4.3:** OnboardingBanner component. Create frontend/components/OnboardingBanner.tsx that guides users through profile + CV setup using shared query keys.
- [ ] **Step 4.4:** ProfileForm and CVUploadPanel components. Create frontend/components/ProfileForm.tsx and frontend/components/CVUploadPanel.tsx for user onboarding and profile editing.
- [ ] **Step 4.5:** SavedJobsList and ApplicationBoard components. Create frontend/components/SavedJobsList.tsx and frontend/components/ApplicationBoard.tsx.
- [ ] **Step 4.6:** RecruiterCard and AdminPanel components. Create frontend/components/RecruiterCard.tsx and frontend/components/AdminPanel.tsx.
- [ ] **Step 4.7:** JobCard component. Create frontend/components/JobCard.tsx displaying job details with Save toggle and job detail navigation.
- [ ] **Step 4.8:** FilterBar component. Create frontend/components/FilterBar.tsx with source and keyword client-side filters backed by Zustand.
- [ ] **Step 4.9:** ScrapeButton component. Create frontend/components/ScrapeButton.tsx triggering POST /api/v1/scrape with in-progress and result states.
- [ ] **Step 4.10:** Refine OnboardingBanner states. Update frontend/components/OnboardingBanner.tsx to implement the exact 5 states and query key contracts as specified in proposal v1.5.0.
- [ ] **Step 4.11:** Refine Profile page logic. Update frontend/app/profile/page.tsx to pass appropriate handlers based on GET response.

### Epic 5: Versioned API & CI Skeleton
- [ ] **Step 5.1:** Jobs router. Create backend/routers/v1/jobs.py with paginated job listing, job detail, save/unsave, and saved jobs list endpoints.
- [ ] **Step 5.2:** Profile and CV endpoints. Create backend/routers/v1/profile.py and backend/routers/v1/cv.py for user profile management and CV upload.
- [ ] **Step 5.3:** OpenAPI spec completeness. Ensure all routes are fully typed with Pydantic request/response models and RFC 7807 error shapes.
- [ ] **Step 5.4:** Admin process scripts. Create backend/admin/ directory with seed_keywords.py, clear_db.py, and stubs for replay_dlq.py and run_evals.py.
- [ ] **Step 5.5:** GitHub Actions CI skeleton. Create .github/workflows/ci.yml using reusable workflow patterns with linting, type checking, tests, and Docker build.
- [ ] **Step 5.6:** Applications endpoint. Create backend/routers/v1/applications.py for logging and tracking applications.
- [ ] **Step 5.7:** Application GET and PATCH endpoints. Create backend endpoints to support ApplicationBoard and ApplicationDetail components.

### Epic 16: Workflow Orchestration Infrastructure
- [ ] **Step 16.1:** Active Task Plan (todo.md). Create docs/tasks/todo.md with the correct structure for AI-agent task tracking.
- [ ] **Step 16.2:** Lessons Log (lessons.md). Create docs/tasks/lessons.md for self-improvement logging after every user correction.
- [ ] **Step 16.3:** Root AGENT.md Workflow Rules. Update root AGENT.md to include Workflow Rules table and expanded Where-to-look index.
- [ ] **Step 16.4:** EXECUTION-RULES.md Workflow Section. Create docs/EXECUTION-RULES.md with Final Execution Rules and Workflow Execution Rules.
- [ ] **Step 16.5:** Backend Agents AGENT.md Subagent Rules. Create backend/agents/AGENT.md with cross-agent rules and Subagent Execution Rules section.
- [ ] **Step 16.6:** CI Workflow Docs Enforcement. Add check-workflow-docs step to .github/workflows/ci.yml that fails if docs/tasks/todo.md or docs/tasks/lessons.md is missing or empty.

### Epic 17: MVP 1 Documentation Additions
- [ ] **Step 17.1:** Create docs/ANTI-BOT.md. Create docs/ANTI-BOT.md to document the anti-bot, proxy, and fingerprinting disclaimer details.

## 🚀 Phase 2: MVP 1.1 — Prompt Engineering Infrastructure

### Epic 7: Eval Framework (DeepEval + Ragas)
- [ ] **Step 7.1:** Eval runner script. Implement backend/admin/run_evals.py (replacing the stub from JD-30) for per-agent eval set execution with field-level output comparison.
- [ ] **Step 7.2:** DeepEval and Ragas integration. Wire DeepEval faithfulness and relevance metrics plus Ragas retrieval metrics into the eval runner.
- [ ] **Step 7.3:** CI prompt regression step. Add eval-regression job to .github/workflows/ci.yml to block deploy if agent output quality drops below threshold.


### Epic 6: Prompts Directory & Versioning Framework
- [ ] **Step 6.1:** Prompts root scaffold. Create prompts/AGENT.md with XML prompt structure standard, reasoning effort matrix, versioning convention, and authoring rules.
- [ ] **Step 6.2:** LinkedIn agent prompts. Create prompts/linkedin-agent/ directory with all six required prompt files.
- [ ] **Step 6.3:** JobServe agent prompts. Create prompts/jobserve-agent/ directory with the same six-file structure as the LinkedIn agent.
- [ ] **Step 6.4:** CONTRACT.md template. Define the reusable CONTRACT.md template in prompts/AGENT.md with all required fields and a filled example.
- [ ] **Step 6.5:** Prompt-based relevance filtering. Activate the filters.py MVP 1.1 profile merge hook and create per-agent filtering prompt files.
- [ ] **Step 6.6:** require_rag_ready FastAPI dependency. Create backend/routers/dependencies.py with the require_rag_ready FastAPI dependency for enforcing CV + profile prerequisites.

## 🚀 Phase 3: MVP 2 — Supabase, AI Ranking & Terraform

### Epic 8: Supabase PostgreSQL & Alembic
- [ ] **Step 8.1:** Replace fake_db with Supabase. Migrate all data storage from the file-backed in-memory fake_db.json to Supabase PostgreSQL with pgvector extension.
- [ ] **Step 8.2:** asyncpg connection pool. Create backend/db.py with SQLAlchemy 2 async engine and explicitly tuned asyncpg connection pool as specified in backend/AGENT.md.
- [ ] **Step 8.3:** Full domain models. Expand backend/models/ with all MVP 2 domain models using SQLAlchemy 2 mapped_column syntax and Pydantic v2 schemas in backend/schemas/.
- [ ] **Step 8.4:** Create backend/models/DOMAIN-MODELS.md. Create backend/models/DOMAIN-MODELS.md to document domain model definitions explicitly as specified in proposal v1.5.0.

### Epic 9: AI Ranking & RAG Agents
- [ ] **Step 9.1:** Ranking agent. Build backend/agents/ranking/ranking_agent.py with the 8-step AI relevance scoring pipeline as specified in backend/agents/ranking/AGENT.md.
- [ ] **Step 9.2:** RAG agent. Build backend/agents/rag/rag_agent.py with contextual retrieval from CV, applications, recruiter data, and saved jobs as specified in backend/agents/rag/AGENT.md.
- [ ] **Step 9.3:** Cover letter agent. Build backend/agents/cover-letter/cover_letter_agent.py with ATS-optimised generation following the 6-section playbook in backend/agents/cover-letter/AGENT.md.
- [ ] **Step 9.4:** Question answer agent. Build backend/agents/question-answer/question_answer_agent.py for RAG-grounded Q&A on specific job listings as specified in backend/agents/question-answer/AGENT.md.
- [ ] **Step 9.5:** Ragas eval in CI. Add Ragas retrieval precision and context recall metrics to the CI eval pipeline, blocking deployment if thresholds are not met.
- [ ] **Step 9.6:** require_rag_ready FastAPI dependency. Implement the require_rag_ready dependency in backend/routers/dependencies.py to enforce CV + profile prerequisites at the API layer before any RAG-dependent endpoint executes.

### Epic 10: Security & Orchestration Agents
- [ ] **Step 10.1:** Security agent. Build backend/agents/security/security_agent.py with comprehensive input validation, prompt injection defence, and OWASP middleware as specified in backend/agents/security/AGENT.md and docs/SECURITY.md.
- [ ] **Step 10.2:** Workflow orchestrator. Build backend/agents/orchestrator/orchestrator_agent.py using Temporal for reliable multi-agent workflow coordination (including AgentResultEnvelope parsing, Critic Revision Protocol, and Learner Feedback Loops) as specified in backend/agents/orchestrator/AGENT.md.
- [ ] **Step 10.3:** Circuit breakers. Implement per-agent circuit breakers with configurable failure thresholds, state logging, token budget enforcement (2x alert_threshold), and exponential backoff, wrapping each agent.run() call in the orchestrator.
- [ ] **Step 10.4:** Admin DLQ routes. Create admin API routes for DLQ inspection, retry, and discard, plus the replay_dlq.py admin script, and the frontend/app/admin/page.tsx admin panel wired to these routes.

### Epic 11: Terraform & Multi-Cloud Deployment
- [ ] **Step 11.1:** Azure Container Apps Terraform. Create infrastructure/terraform/azure/ with main.tf, variables.tf, and outputs.tf for Azure Container Apps deployment as specified in infrastructure/AGENT.md.
- [ ] **Step 11.2:** AWS ECS Fargate Terraform. Create infrastructure/terraform/aws/ with main.tf, variables.tf, and outputs.tf for AWS ECS Fargate deployment as specified in infrastructure/AGENT.md.
- [ ] **Step 11.3:** Terraform CI steps. Add Terraform validate, plan, and apply steps to .github/workflows/ci.yml for both azure/ and aws/ modules, with manual approval gate before apply.
- [ ] **Step 11.4:** Docker image signing. Configure GitHub Actions to build, tag, sign, and push Docker images to ACR and ECR on merge to main, using cosign keyless signing via GitHub OIDC.
- [ ] **Step 11.5:** Helm chart scaffold. Create infrastructure/helm/job-discovery/ with Chart.yaml and values.yaml as the Helm deployment scaffold for MVP 2+ Kubernetes targets.

### Epic 12: MVP 2 Prompts for AI Agents
- [ ] **Step 12.1:** Ranking agent prompts. Create prompts/ranking-agent/ with CONTRACT.md, CHANGELOG.md, system.md, scoring.md, reranking.md, and filtering.md.
- [ ] **Step 12.2:** RAG agent prompts. Create prompts/rag-agent/ with CONTRACT.md, CHANGELOG.md, system.md, retrieval.md, embeddings.md, and personalization.md.
- [ ] **Step 12.3:** Cover letter agent prompts. Create prompts/cover-letter-agent/ with CONTRACT.md, CHANGELOG.md, system.md, tone.md, generation.md, and templates.md.
- [ ] **Step 12.4:** Question answer & security agent prompts. Create prompts/question-answer-agent/ and prompts/security-agent/ with all required prompt files.
- [ ] **Step 12.5:** Orchestrator prompts. Create prompts/orchestrator/ with CONTRACT.md, CHANGELOG.md, system.md, skills.md, tools.md, and guardrails.md (including Critic Revision Protocol, Token Budget Enforcement, and Learner Feedback Loops) at xhigh reasoning effort for long-horizon multi-step workflow coordination.
- [ ] **Step 12.6:** Quality Critic agent prompts. Create prompts/quality-critic-agent/ with all required prompt files.

### Epic 18: MVP 2 Infrastructure & Rate Limiting Docs
- [ ] **Step 18.1:** Create docs/FEATURE-FLAGS.md. Create docs/FEATURE-FLAGS.md to define the Feature Flag Strategy.
- [ ] **Step 18.2:** Create docs/SCRAPING-RATE-LIMITS.md. Create docs/SCRAPING-RATE-LIMITS.md for outbound scraping rate limiting strategy.
- [ ] **Step 18.3:** Create infrastructure/LOCAL-LLM.md. Create infrastructure/LOCAL-LLM.md for local LLM runtime support details.
- [ ] **Step 18.4:** Create Local LLM Start Scripts. Create start/stop server scripts for Mac, PC, and Linux in the scripts/ directory.

### Epic 22: API Gateway & Rate Limiting Infrastructure
- [ ] **Step 22.1:** Implement Per-Endpoint Rate Limiting. Implement per-endpoint rate limits enforced at the API Gateway level or via FastAPI middleware as specified in proposal v1.5.0 Rate Limiting Strategy.
- [ ] **Step 22.2:** Configure API Gateway Plugins. Configure API Gateway concern layer with the five specified plugins as documented in infrastructure/AGENT.md.
- [ ] **Step 22.3:** Implement Proxy Abstraction Layer. Build the proxy abstraction layer for outbound scraping requests with residential proxy support as specified in docs/ANTI-BOT.md and proposal v1.5.0.

### Epic 23: Serverless AI Ranking & Deployment Enhancements
- [ ] **Step 23.1:** Serverless AI Ranking Support. Configure the AI ranking pipeline for serverless/burst execution to enable cost-efficient scaling of expensive AI workloads.
- [ ] **Step 23.2:** Release Tagging & Rollback Strategy. Implement Git SHA-based release tagging and document the rollback deployment strategy as specified in infrastructure/AGENT.md proposal v1.5.0.
- [ ] **Step 23.3:** Update Deployment Topology Documentation. Update infrastructure/AGENT.md with production services that scale independently and the API Gateway concern table as specified in proposal v1.5.0.

### Epic 24: Frontend Component Refinements
- [ ] **Step 24.1:** Refine CoverLetterViewer error handling. Update frontend/components/CoverLetterViewer.tsx to implement exact export fallback handling.
- [ ] **Step 24.2:** Refine Application tracking logic. Update frontend/app/applications/page.tsx logic for handling existing applications.
- [ ] **Step 24.3:** Refine Job Detail Interview Prep states. Update frontend/app/jobs/[id]/page.tsx to implement exact CompanyResearch states for the Interview Prep feature.


### Epic 28: Agent Communication Protocol
- [ ] **Step 28.1:** Define AgentResultEnvelope schema. 
- [ ] **Step 28.2:** Refactor BaseScrapeAgent to return AgentResultEnvelope. 

### Epic 29: Critic Revision Protocol
- [ ] **Step 29.1:** Implement bounded retry loop with max_revision_cycles=2. 
- [ ] **Step 29.2:** Implement Security Agent override and DLQ escalation. 
- [ ] **Step 29.3:** Log revision metrics for observability. 

### Epic 30: Token Budget Enforcement
- [ ] **Step 30.1:** Implement token tracking and thresholds in Orchestrator. 
- [ ] **Step 30.2:** Add circuit-breaking and DLQ routing on threshold breach. 

### Epic 31: Model Selection Matrix
- [ ] **Step 31.1:** Configure LiteLLM routing rules and models. 
- [ ] **Step 31.2:** Add support for MODEL_OVERRIDE env vars. 

### Epic 32: EVAL COVERAGE MATRIX (MVP 2)
- [ ] **Step 32.1:** Create eval sets for MVP 2 agents. 

### Epic 33: Quality Critic Agent
- [ ] **Step 33.1:** Create Quality Critic agent directory and implementation. 

### Epic 34: Orchestrator Planner
- [ ] **Step 34.1:** Create planner.py for Orchestrator. 

### Epic 35: Missing Prompt Directories
- [ ] **Step 35.1:** Create missing prompt directory for quality_critic/. 

## 🚀 Phase 4: MVP 3 — Twelve-Factor & Observability

### Epic 13: Observability Stack
- [ ] **Step 13.1:** OpenTelemetry integration. Integrate OpenTelemetry distributed tracing and metrics across all FastAPI routers and agent run() methods as specified in docs/OBSERVABILITY.md.
- [ ] **Step 13.2:** Grafana dashboards. Create five Grafana dashboards as versioned JSON files in infrastructure/grafana/, covering API latency, AI agent performance, RAG quality, ranking, and infrastructure health.
- [ ] **Step 13.3:** Sentry & Microsoft Clarity. Integrate Sentry for backend and frontend error tracking, and Microsoft Clarity for frontend session replay and UX analytics.
- [ ] **Step 13.4:** Observability agent. Build backend/agents/observability/observability_agent.py for AI-specific reliability monitoring running as a periodic background task, as specified in backend/agents/observability/AGENT.md and docs/OBSERVABILITY.md.
- [ ] **Step 13.5:** Create docs/OBSERVABILITY.md. Create docs/OBSERVABILITY.md as the single source of truth for all observability standards, tracked metrics, alerting thresholds, and Loki query examples for the platform.
- [ ] **Step 13.6:** Create backend/agents/observability/AGENT.md. Create backend/agents/observability/AGENT.md to define the responsibilities, input/output schemas, and metric thresholds for the Observability agent as per proposal-v4-structure.md.
- [ ] **Step 13.7:** Implement ObservabilityPanel.tsx. Implement frontend/components/ObservabilityPanel.tsx to display agent traces and token usage.

### Epic 14: Auth, RBAC & Row-Level Security
- [ ] **Step 14.1:** Supabase Auth & JWT. Implement JWT validation middleware in FastAPI with RBAC enforced via JWT claims, as specified in docs/SECURITY.md.
- [ ] **Step 14.2:** Row-Level Security. Configure Supabase RLS policies on all user-scoped tables so users can only read and write their own rows, with service role bypass for scraper agents.
- [ ] **Step 14.3:** OWASP Top 10 hardening. Run Trivy container image scanning and Bandit static analysis in CI, configure SSRF allowlist, and wire Azure Key Vault secret references as specified in docs/SECURITY.md.
- [ ] **Step 14.4:** GDPR compliance. Implement data export, deletion, and audit logging endpoints for GDPR compliance, as documented in docs/SECURITY.md data flow section.
- [ ] **Step 14.5:** Create docs/SECURITY.md. Create docs/SECURITY.md as the single source of truth for all security standards, covering Supabase Auth, JWT, RBAC, RLS, OWASP Top 10 compliance, prompt injection defence, and GDPR data flow documentation.

### Epic 15: Twelve-Factor Completion & Admin Tooling
- [ ] **Step 15.1:** Twelve-Factor audit. Audit all 12 Twelve-Factor App factors against the production Azure Container Apps deployment, close all identified gaps, and update docs/ENGINEERING-STANDARDS.md with final compliance status.
- [ ] **Step 15.2:** Graceful shutdown. Implement SIGTERM handlers in all long-running processes: uvicorn drain, Temporal worker checkpoint, and Playwright browser session close, as documented in docs/RELIABILITY.md.
- [ ] **Step 15.3:** Structured admin tooling. Fully implement replay_dlq.py and run_evals.py CLI scripts with complete flag support; wire schedule pause/resume admin API routes.
- [ ] **Step 15.4:** Disaster recovery validation. Execute a documented backup restore drill for PostgreSQL WAL (Supabase PITR) and Redis AOF, validate RTO <= 1 hour and RPO <= 15 minutes, and update docs/RELIABILITY.md with results and exact restore commands.
- [ ] **Step 15.5:** Create docs/ENGINEERING-STANDARDS.md. Create docs/ENGINEERING-STANDARDS.md as the authoritative reference for all frontend, backend, and database stack standards, and full Twelve-Factor compliance notes for all 12 factors.
- [ ] **Step 15.6:** Create docs/RELIABILITY.md. Create docs/RELIABILITY.md documenting all reliability engineering standards including failure mode catalogue, DIFA framework, ReAct loop pattern, circuit breaker configuration, disaster recovery procedures, and DR drill schedule.

### Epic 19: MVP 3 Data Ownership & Disaster Recovery Docs
- [ ] **Step 19.1:** Create docs/DATA-OWNERSHIP.md. Create docs/DATA-OWNERSHIP.md to detail data ownership and portability.
- [ ] **Step 19.2:** Create infrastructure/DISASTER-RECOVERY.md. Create infrastructure/DISASTER-RECOVERY.md to document full disaster recovery and backup restore details.


### Epic 36: EVAL COVERAGE MATRIX (MVP 3)
- [ ] **Step 36.1:** Create eval set for Observability. 
- [ ] **Step 36.2:** Create missing prompt directory for observability/. 

### Epic 37: EVAL COVERAGE MATRIX (Post-MVP 3)
- [ ] **Step 37.1:** Create eval set for Interview Prep. 

## 🚀 Phase 5: MVP 4 — Application Workflow and Interview Preparation

### Epic 20: Application Workflow & Interview Preparation
- [ ] **Step 20.1:** Application Assistant Docs. Create backend/agents/application-assistant/AGENT.md and associated prompts/application-assistant/ structure.
- [ ] **Step 20.2:** Interview Prep Agent Docs. Create backend/agents/interview-prep/AGENT.md and associated prompts/interview-prep/ structure.
- [ ] **Step 20.3:** Build Application Assistant Agent. Implement the Autonomous Job Application Assistant Agent in Python.
- [ ] **Step 20.4:** Build Interview Prep Agent. Implement the Interview Preparation Intelligence Agent.
- [ ] **Step 20.5:** Enable Interview Prep Button. Finalize the frontend logic for the Interview Prep feature on the Job Detail page.

## 🚀 Phase 6: MVP 5 — Security Hardening and Production Polish

### Epic 21: Security Hardening and Production Polish
- [ ] **Step 21.1:** Finalize Production Deployment Topology. Review and finalize the highly available deployment architecture for production launch.
- [ ] **Step 21.2:** Comprehensive Security Audit. Conduct a final security audit of all Prompt Injection Defenses, RBAC rules, RLS policies, and OWASP mitigations.
- [ ] **Step 21.3:** UI/UX Production Polish. Polish all frontend views to ensure a premium, production-ready user experience.

## 🌐 Cross-MVP / Progressive Features

### Epic 25: Presenter Role — Progressive Pattern
- [ ] **Step 25.1:** MVP 1 Inline Presenter for Doer Agents. 
- [ ] **Step 25.2:** MVP 2 Orchestrator-as-Presenter. 
- [ ] **Step 25.3:** Post-MVP 3 Dedicated Presenter (Application Assistant). 

### Epic 26: Learner Feedback Loops
- [ ] **Step 26.1:** Wire RAG Agent feedback to downstream agents. 
- [ ] **Step 26.2:** Wire Interview Prep research to Presenter. 
- [ ] **Step 26.3:** Expose retrieval precision scores to Quality Critic. 
- [ ] **Step 26.4:** Connect Interview Prep question bank to Q&A agent. 

### Epic 27: Agent Activation Timeline
- [ ] **Step 27.1:** Implement feature-flag-gated agent activation framework. 
- [ ] **Step 27.2:** Configure graceful degradation for missing MVP 3+ agents. 


---
## 🎯 AI Agent: Start Execution
When you are ready to begin, start with **Phase 1, Epic 1, Step 1.1**. Follow the Execution Loop precisely.
