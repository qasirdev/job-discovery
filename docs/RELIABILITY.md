# Reliability & Architecture Specification (AI Job Discovery Platform)

This document defines the system architecture, operational reliability patterns, and disaster recovery strategy for a production-grade AI-driven job discovery platform using LLM agents, scraping pipelines, and workflow orchestration.

---

# 1. System Architecture Principles

The platform follows two foundational layers:

## 1.1 Platform Reliability Layer (Twelve-Factor + Cloud Native)

Ensures the system is scalable, maintainable, and deployment-safe.

## 1.2 Agent Reliability Layer (AI + Runtime Resilience)

Ensures LLM agents, scrapers, and tool chains behave safely under failure conditions.

---

# 2. Twelve-Factor App Compliance

The system strictly follows Twelve-Factor principles:

## I. Codebase

Single codebase tracked in Git, deployed via CI/CD (GitHub Actions, Terraform).

## II. Dependencies

Strict dependency management:

* Python: `uv` (`pyproject.toml`, `uv.lock`)
* Node: `npm`

## III. Config

Environment-based configuration only:

* Managed via Pydantic `BaseSettings`
* No secrets in code

## IV. Backing Services

All services treated as attachable resources:

* PostgreSQL (primary datastore)
* Redis (caching + ephemeral state)
* Temporal (workflow engine)

## V. Build, Release, Run

Separation enforced via CI/CD pipelines:

* Build → Artifact creation
* Release → Configuration binding
* Run → Stateless execution

## VI. Processes

All services are stateless:

* FastAPI API layer
* Temporal workers
* Session state stored in Redis

## VII. Port Binding

FastAPI exposes HTTP natively (port 8000+)

## VIII. Concurrency

Horizontal scaling via:

* ECS Fargate / Azure Container Apps
* Stateless workers

## IX. Disposability

* Fast startup
* Graceful shutdown (SIGTERM handling)
* Safe crash recovery

## X. Dev/Prod Parity

* Docker Compose mirrors production
* Same services locally and in cloud

## XI. Logs

* Structured JSON logs only
* Output via stdout
* Aggregation: Promtail → Loki (or equivalent)

## XII. Admin Processes

One-off tasks executed via:

* `backend/admin/` scripts
* Controlled operational tooling

---

# 3. Workflow Orchestration & Reliability

## 3.1 Temporal Workflow Engine

All unstable operations are encapsulated in Temporal workflows:

* Web scraping
* LLM calls
* External API requests
* Data enrichment pipelines

## 3.2 Retry Policies

* Exponential backoff
* Jitter applied
* Configurable max retries (default 3–5)

## 3.3 Dead Letter Queue (DLQ)

Failures are never lost:

* Stored in PostgreSQL DLQ tables
* Includes payload, error context, retry metadata
* Supports manual replay

## 3.4 Poison Pill Protection

Repeatedly failing inputs:

* Routed to DLQ
* Prevents infinite retry loops

---

# 4. Agent Reliability Engineering (AI Runtime Layer)

## 4.1 Failure Modes & Defenses

### Rate Limits (HTTP 429)

* Exponential backoff + jitter
* Request throttling per provider

### Scraping Failures

* Selector break detection
* Fallback extraction methods
* Graceful degradation (skip field)

### LLM Failures / Hallucinations

* Pydantic schema validation
* Retry-on-parse-failure loops
* Structured output enforcement

---

## 4.2 DIFA Framework (Detect, Isolate, Fallback, Alert)

### Detect

Identify exact failure type:

* Timeout
* API error
* Parse failure

### Isolate

Prevent cascade failures in batch jobs

### Fallback

* Alternative data source
* Default values
* Partial completion

### Alert

* Structured logs for observability pipeline
* Tagged with workflow + agent metadata

---

## 4.3 Circuit Breaker Pattern

* Monitors external dependency failure rates
* If >50% failures in 5-minute window:

  * Circuit opens
  * Requests paused
* Auto-recovery after cooldown

---

## 4.4 Idempotency

* Safe retries
* No duplicate records
* Deterministic state transitions

---

## 4.5 ReAct Agent Loop

Agents follow:

1. Reason
2. Act
3. Observe
4. Repeat

Ensures:

* Traceability
* Debuggability
* Controlled tool usage

---

# 5. Observability & Logging

## 5.1 Logging

* JSON structured logs only
* Includes trace_id, workflow_id, agent_id

## 5.2 Metrics

* LLM failure rate
* Scraping success rate
* Retry counts
* Circuit breaker state
* DLQ volume

## 5.3 Tracing

End-to-end request tracing:
API → Workflow → Agent → Tool calls

---

# 6. Disaster Recovery (DR)

## 6.1 Database Recovery

* PostgreSQL PITR enabled
* Managed failover supported

## 6.2 DLQ Replay System

* Admin tool: replay_dlq.py
* Safe reprocessing with validation

## 6.3 Worker Recovery

* Stateless workers
* Auto-restart on failure

---

# 7. Infrastructure & Scaling

## 7.1 Containerization

* Docker-based deployment

## 7.2 Orchestration

* AWS ECS Fargate / Azure Container Apps
* Fully automated CI/CD

## 7.3 Scaling Model

* Horizontal scaling only
* Stateless compute nodes

---

# 8. Security & Safety

* No secrets in codebase
* Schema-validated LLM outputs
* Tool execution sandboxed via workflows
* Admin scripts isolated from runtime system

---

# 9. System Summary

This platform is:

> A stateless, horizontally scalable cloud system (Twelve-Factor)
> running workflow-orchestrated AI agents (Temporal)
> with multi-layer failure recovery (DIFA + DLQ + circuit breakers)
> and strict LLM output control (schema + ReAct loop)
