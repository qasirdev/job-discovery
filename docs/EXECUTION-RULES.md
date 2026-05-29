# FINAL EXECUTION RULES

This document serves as the absolute source of truth for execution standards and workflow discipline. It supersedes any generalized instructions.

## 1. Production-Ready Code Requirements
- **No Pseudo-code**: All implementations must be fully functioning code. Comments like `// add logic here` are strictly forbidden unless part of a defined scaffolding step.
- **No Auto-apply Magic**: Developers and agents must verify code before committing.
- **No Fabricated Metrics**: If tracking a metric (e.g., token usage, latency), it must be wired to actual telemetry (like OpenTelemetry), not hardcoded mock values.
- **No Monolithic Agents**: All agents must adhere to the `BaseScrapeAgent` or similar abstract base class, fulfilling a single isolated purpose.
- **No Untyped APIs**: All API inputs and outputs must be strictly typed using Pydantic v2 (Backend) and Zod/TypeScript (Frontend).

## 2. Workflow Execution Rules (The "ReAct" Loop for Coding)

### MUST Do:
1. **Plan Mode**: Any task with 3 or more steps, or involving architectural decisions, must begin with a written plan.
2. **Task Logging**: The plan must be written to `docs/tasks/todo.md` before any implementation code is touched.
3. **Verification Gate**: Do not proceed to the next step on `docs/tasks/todo.md` until the current step is proven to work via tests, linters, or logs.
4. **Lessons Review**: At the start of every session, read `docs/tasks/lessons.md` to avoid repeating past mistakes.
5. **Correction Loop**: If a mistake is made or corrected by a user, immediately update `docs/tasks/lessons.md` with the root cause and a new rule.
6. **Done Gate**: Never mark a task as complete without providing proof (e.g., test output, build success logs, diffs).
7. **Elegance Check**: Before finalizing a complex change, pause and ask: *"Is there a more elegant, standard way to do this?"*
8. **Bug Fix Autonomy**: When encountering a bug during development, analyze the stack trace or logs and fix it autonomously without requiring human hand-holding.
9. **Reference Standards**: Always consult `docs/example-code/` for reference implementations and best practices before writing new code.
10. **Edge Case Implementation**: When implementing an epic or task, you MUST read the `Description` column of the relevant `.json` file in `docs/jira-tickets-json/` and explicitly implement any edge cases, fail-safes, or fallbacks mentioned.

### MUST NOT Do:
- Implement before plan confirmed
- Mark done without evidence
- Apply hacky fixes
- Edit out-of-scope files
- Repeat documented mistakes

## 3. YOLO Mode Exceptions & Rules
Even when the user explicitly triggers "YOLO mode" (authorizing high-velocity, low-ceremony implementation without pre-approval gates), the fundamental system rules **still apply**:
1. **Never Skip the Logs**: You must STILL update `docs/tasks/todo.md` to reflect the work done. YOLO means "skip the pre-approval", not "skip the documentation".
2. **Never Forget Lessons**: You must STILL read and append to `docs/tasks/lessons.md`.
3. **No Broken Windows**: YOLO mode allows faster implementation across multiple files, but it does NOT authorize submitting broken, unverified, or pseudo-code.
4. **Immediate Sync**: After completing a YOLO burst, immediately synchronize the state back into the `todo.md` and `lessons.md` trackers.

## 4. Tech Stack Best Practices
- **Production Grade 2026**: Always reference the official 2026 documentation for Next.js, Python/FastAPI with docstring for functions and method, Docker, and GitHub Actions. Utilize modern features (e.g., reusable GitHub Actions workflows).
- **FastAPI Constants**: ALWAYS use `fastapi.status` constants (e.g. `status.HTTP_404_NOT_FOUND`) for HTTP status codes rather than raw integers.
