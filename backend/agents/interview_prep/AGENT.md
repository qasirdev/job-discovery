# Interview Preparation Intelligence Agent

## Role
Generate RAG-grounded preparation pack: technical questions, behavioural questions, system design topics, salary guidance, company intelligence.

## Input
- `job_structured`: Scraped job data (JSON).
- `cv`: CV embedding/document reference.
- `company_research`: Company Research JSONB.

## Output
- A personalised preparation pack.

## Execution Flow
- Check for `CompanyResearch` record.
- If missing or >7 days old, orchestrator calls company-research endpoint.
- If `job.company_slug` missing, skip research.

## Execution Model
- **Temporal Worker**: Execution occurs asynchronously via `InterviewPrepWorkflow` to prevent HTTP 504 timeouts.
- **Queue**: Routes tasks to the `interview-tasks` queue.
- **State Tracking**: Writes `generating` state to database instantly, updates to `ready` or `failed` upon completion.
