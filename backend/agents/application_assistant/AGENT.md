# Autonomous Job Application Assistant Agent

## Role
Semi-automated form filling and document upload via Playwright for job applications.

## Input
- `job_url`: Target job URL.
- `user_profile`: User Profile data (JSON).
- `cv`: CV embedding/document reference.

## Output
- Form filling actions (never auto-submits).
- Returns status of the form completion and required manual inputs.

## Constraints
- Never auto-submits. Always requires explicit user confirmation.
- Safety rules enforced in code.

## Execution Model
- **Temporal Worker**: Execution occurs asynchronously via `ApplicationAssistantWorkflow` to prevent HTTP 504 timeouts.
- **Queue**: Routes tasks to the `application-tasks` queue.
- **Failures**: Unhandled exceptions are routed to the DLQ by the orchestrator.
