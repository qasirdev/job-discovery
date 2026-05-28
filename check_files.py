import os
import re

tree_text = """
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
│   ├── tasks/                             # MVP 1: Workflow management — process-level, not architecture-level
│   │   ├── todo.md                        # Active task plan with checkable items; written before any implementation
│   │   └── lessons.md                     # Self-improvement log; updated after every user correction (episodic memory of agent), other memories are 1-working,2-semantic(AGNT.md),3-procedural(SKILLS.md)
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
│   ├── DATA-OWNERSHIP.md                  # ← Data Ownership and Portability
│   └── AGENTIC-CONSENT.md                 # ← from: Agentic Consent model for LLM Evaluation
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
│   │   ├── layout.tsx                         # Global layout — renders OnboardingBanner + global nav (Dashboard, Saved, Applications, Recruiters, Admin)
│   │   ├── page.tsx                           # Dashboard — job feed with pagination, filter, scrape
│   │   ├── globals.css
│   │   ├── onboarding/
│   │   │   └── page.tsx                       # Onboarding flow: ProfileForm → CVUploadPanel → status
│   │   ├── profile/
│   │   │   └── page.tsx                       # Edit existing UserProfile and replace CV
│   │   ├── jobs/
│   │   │   └── [id]/
│   │   │       └── page.tsx                   # Job detail: Save button, Generate Cover Letter button, Ask Question button (scrolls to panel), Generate Interview Prep button, Log Application button
│   │   ├── cover-letter/
│   │   │   └── [id]/
│   │   │       └── page.tsx                   # Cover Letter viewer — renders CoverLetterViewer.tsx
│   │   ├── interview-prep/
│   │   │   └── [id]/
│   │   │       └── page.tsx                   # Interview Prep viewer — renders generated interview intelligence with export and back navigation. Must implement export fallback handling matching Cover Letter Viewer.
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
│   │   ├── settings/
│   │   │   └── consent/
│   │   │       └── page.tsx                   # Consent dashboard to manage and revoke active "living contracts"
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
│       ├── QuestionAnswerPanel.tsx             # Inline Q&A panel on job detail page — calls POST /api/v1/question-answer/{job_id}
│       ├── CVUploadPanel.tsx
│       ├── ProfileForm.tsx
│       ├── OnboardingBanner.tsx
│       └── ConsentPromptModal.tsx             # JIT prompting when an agent requires human-in-the-loop approval
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
│   │   ├── cover_letter/                  # MVP 2
│   │   │   ├── AGENT.md                   # ← from: Cover Letter Agent + COVER LETTER PLAYBOOK
│   │   │   └── cover_letter_agent.py
│   │   │
│   │   ├── question_answer/               # MVP 2
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
│   │   │   ├── planner.py                 # MVP 2: Goal → step decomposition; validates plans against tool schemas
│   │   │   └── orchestrator_agent.py
│   │   │
│   │   ├── quality_critic/                # MVP 2
│   │   │   ├── AGENT.md                   # ← from: Quality Critic Agent responsibilities (hallucination, factual, schema checks)
│   │   │   └── quality_critic_agent.py
│   │   │
│   │   ├── application_assistant/         # Optional (post-MVP 3)
│   │   │   ├── AGENT.md                   # ← from: Autonomous Job Application Assistant Agent
│   │   │   └── application_agent.py
│   │   │
│   │   └── interview_prep/                # Optional (post-MVP 3)
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
│       │   ├── jobs.py                    # MVP 1: GET /api/v1/jobs, GET /api/v1/jobs/{id}, GET /api/v1/jobs/saved, POST|DELETE /api/v1/jobs/{id}/save
│       │   ├── scrape.py                  # MVP 1: POST /api/v1/scrape (registry-driven)
│       │   ├── cover_letter.py            # MVP 2: POST /api/v1/cover-letter/{job_id}, GET /api/v1/cover-letter/{job_id}, GET /api/v1/cover-letter/{job_id}/export
│       │   ├── question_answer.py         # MVP 2: POST /api/v1/question-answer/{job_id}
│       │   ├── interview.py               # MVP 2+: POST /api/v1/interview-prep/{job_id}
│       │   ├── profile.py                 # MVP 1: GET, POST, PATCH /api/v1/profile
│       │   ├── cv.py                      # MVP 1: GET, POST /api/v1/cv, GET /api/v1/cv/status
│       │   ├── feature_flags.py           # MVP 2: GET /api/v1/feature-flags (env-driven static flag model)
│       │   ├── recruiters.py              # MVP 2: GET, POST, PATCH /api/v1/recruiters, POST /api/v1/recruiters/{id}/interaction
│       │   ├── applications.py            # MVP 2: GET (supports ?job_id= filter), POST, PATCH /api/v1/applications
│       │   ├── company_research.py        # MVP 2: GET /api/v1/company-research
│       │   └── admin.py                   # MVP 2: GET /api/v1/admin/dlq, POST /api/v1/admin/dlq/{id}/retry, DELETE /api/v1/admin/dlq/{id}/discard, GET /api/v1/admin/schedule, POST /api/v1/admin/schedule/{workflow_id}/pause, POST /api/v1/admin/schedule/{workflow_id}/resume
│       └── dependencies.py                # MVP 1.1+: require_rag_ready FastAPI dependency
│
├── prompts/                               # MVP 1.1: All LLM prompt files — versioned by agent
│   ├── AGENT.md                           # ← from: MULTI-AGENT PROMPT STRUCTURE + PROMPT VERSIONING + AI PROMPT ENGINEERING STANDARDS
│   │
│   ├── linkedin/                    # MVP 1.1
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── jobserve/                    # MVP 1.1
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── ranking/                     # MVP 2
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
│   ├── rag/                         # MVP 2
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
│   ├── cover_letter/                # MVP 2
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
│   ├── question_answer/             # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── security/                    # MVP 2
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
│   ├── quality_critic/                    # MVP 2
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   ├── application_assistant/             # Optional (post-MVP 3)
│   │   ├── CONTRACT.md
│   │   ├── CHANGELOG.md
│   │   ├── system.md
│   │   ├── skills.md
│   │   ├── tools.md
│   │   └── guardrails.md
│   │
│   └── interview_prep/                    # Optional (post-MVP 3)
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
"""

lines = tree_text.strip().split('\n')
paths = []
current_path = []

for line in lines:
    if '── ' in line:
        depth = line.find('── ') // 4
        name = line.split('── ')[1].split(' ')[0]
        if len(current_path) > depth:
            current_path = current_path[:depth]
        current_path.append(name)
        paths.append(os.path.join(*current_path))

missing_files = []
for p in paths:
    # Handle files vs directories heuristically based on trailing slashes or extensions
    full_path = os.path.join('/Users/qasirmehmood/Projects/qasir-proflle-2026/job-discovery', p)
    if p.endswith('/') or '.' not in p.split('/')[-1] and not p.endswith('.csv'):
        if not os.path.isdir(full_path):
            missing_files.append(p + "/")
    else:
        if not os.path.isfile(full_path):
            missing_files.append(p)

for f in missing_files:
    print(f"MISSING: {f}")
