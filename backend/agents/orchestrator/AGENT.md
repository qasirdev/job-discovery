# Workflow Orchestrator Agent

- **Role**: Coordinate the execution pipeline across all AI agents (Security, Ranking, RAG, Cover Letter).
- **Input**: `Job` (Job database model)
- **Output**: `dict` (Aggregated pipeline results)
- **Responsibilities**:
  - Orchestration rules and activity sequencing.
  - Retry logic (exponential backoff, jitter) wrapping downstream agents.
  - Dead-letter queue routing for failed jobs.
  - Workflow coordination via Temporal (`ScrapeAndRankWorkflow`).
  - Async execution management.
  - Checkpoint recovery via Temporal event history.
  - Idempotency enforcement (e.g., using `sha256(job_url)` as workflow ID).

- **Reasoning Effort**: Extra High (xhigh)
