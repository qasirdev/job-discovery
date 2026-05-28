## Implementation Priority List

### Source: `jd-mvp3.0.csv`

- **JD-E13**: Observability Stack (Epic)
  - [JD-77] Create docs/OBSERVABILITY.md
  - [JD-62] OpenTelemetry integration
  - [JD-63] Grafana dashboards
  - [JD-64] Prometheus & Loki
  - [JD-65] Sentry & Microsoft Clarity
  - [JD-66] Observability agent
  - [JD-81] Create backend/agents/observability/AGENT.md
  - [JD-82] Implement ObservabilityPanel.tsx
- **JD-E14**: Auth, RBAC, Row-Level Security & Agentic Consent (Epic)
  - [JD-78] Create docs/SECURITY.md
  - [JD-67] Supabase Auth & JWT
  - [JD-68] Row-Level Security
  - [JD-69] OWASP Top 10 hardening
  - [JD-70] GDPR compliance
  - [JD-138] Create docs/AGENTIC-CONSENT.md
  - [JD-139] Implement ConsentPromptModal.tsx
  - [JD-140] Implement Consent Dashboard
- **JD-E15**: Twelve-Factor Completion & Admin Tooling (Epic)
  - [JD-79] Create docs/ENGINEERING-STANDARDS.md
  - [JD-80] Create docs/RELIABILITY.md
  - [JD-71] Twelve-Factor audit
  - [JD-72] Graceful shutdown
  - [JD-73] Structured admin tooling
  - [JD-74] Disaster recovery validation
- **Standalone Tasks**

### Source: `jd-mvp3.1.csv`

- **JD-E19**: MVP 3 Data Ownership & Disaster Recovery Docs (Epic)
  - [JD-87] Create docs/DATA-OWNERSHIP.md (including Consent & Personalization)
  - [JD-88] Create infrastructure/DISASTER-RECOVERY.md

### Source: `jd-mvp3.2.csv`

- **JD-E36**: EVAL COVERAGE MATRIX (MVP 3) (Epic)
  - [JD-135] Create evals/observability/eval-set-v1.json and update CONTRACT.md
  - [JD-136] Create prompts/observability/ with all 6 required XML files

### Source: `jd-mvp-cross.csv`

- **JD-E25**: Presenter Role — Progressive Pattern (Epic)
  - [JD-113] MVP 1 Inline Presenter for Doer Agents
  - [JD-114] MVP 2 Orchestrator-as-Presenter
  - [JD-115] Post-MVP 3 Dedicated Presenter (Application Assistant)
- **JD-E26**: Learner Feedback Loops (Epic)
  - [JD-116] Wire RAG Agent feedback to downstream agents
  - [JD-117] Wire Interview Prep research to Presenter
  - [JD-118] Expose retrieval precision scores to Quality Critic and Observability
  - [JD-119] Connect Interview Prep question bank to Q&A agent
- **JD-E27**: Agent Activation Timeline (Epic)
  - [JD-120] Implement feature-flag-gated agent activation framework
  - [JD-121] Configure graceful degradation for missing MVP 3+ agents
  - [JD-145] Enforce Agent Dependency and Scaling Constraints

### Source: `jd-mvp-post3.csv`

- **JD-E37**: EVAL COVERAGE MATRIX (Post-MVP 3) (Epic)
  - [JD-137] Create evals/interview_prep/eval-set-v1.json

### Source: `jd-mvp4.csv`

- **JD-E20**: Application Workflow & Interview Preparation (Epic)
  - [JD-89] Application Assistant Docs
  - [JD-90] Interview Prep Agent Docs
  - [JD-91] Build Application Assistant Agent
  - [JD-92] Build Interview Prep Agent
  - [JD-93] Enable Interview Prep Button
  - [JD-141] Create Interview Prep Viewer UI
  - [JD-142] Application Assistant UI Integration
  - [JD-143] Eval Sets for MVP 4 Agents
  - [JD-144] Wire MVP 4 Patterns

### Source: `jd-mvp5.csv`

- **JD-E21**: Security Hardening and Production Polish (Epic)
  - [JD-94] Finalize Production Deployment Topology
  - [JD-95] Comprehensive Security Audit
  - [JD-96] UI/UX Production Polish

