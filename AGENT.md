# AGENT.md — Job Discovery Platform

## What this file is

This is the root index for the AI-Powered Job Discovery Platform.
All engineering standards, agent specs, and prompt rules live in
co-located AGENT.md files alongside the code they govern.

## Workflow Rules (read at every session start)

| Rule | Behaviour |
|---|---|
| Plan mode | Required for any task with 3+ steps or architectural decisions |
| Task log | Write plan to `tasks/todo.md` before any implementation |
| Verify plan | Check in before starting — do not build on an unconfirmed plan |
| Subagents | Offload research, exploration, parallel analysis to subagents |
| Lessons review | Read `tasks/lessons.md` at session start before touching code |
| Correction loop | After any user correction: update `tasks/lessons.md` immediately |
| Done gate | Never mark complete without proving it works (tests, logs, diff) |
| Elegance check | For non-trivial changes: pause and ask "is there a more elegant way?" |
| Bug reports | Fix autonomously — point at logs/errors and resolve without hand-holding |

## Where to look

| Concern | File | MVP |
|---|---|---|
| Architecture and objectives | docs/ARCHITECTURE.md | MVP 1 |
| Engineering standards (FE/BE/DB) | frontend/AGENT.md, backend/AGENT.md | MVP 1 |
| Twelve-Factor compliance | docs/ENGINEERING-STANDARDS.md | MVP 1–3 |
| Structured JSON logger | backend/logging_config.py | MVP 1 |
| Env var validation | backend/settings.py | MVP 1 |
| asyncpg connection pool | backend/db.py | MVP 2 |
| Admin processes | backend/admin/ | MVP 1 |
| Alembic migrations | backend/migrations/ | MVP 2 |
| Security, OWASP, injection defense | docs/SECURITY.md | MVP 2–3 |
| Observability | docs/OBSERVABILITY.md | MVP 3 |
| Reliability, DIFA, ReAct | docs/RELIABILITY.md | MVP 1 |
| Real-time architecture | docs/REAL-TIME.md | MVP 2 |
| Analytics | docs/ANALYTICS.md | MVP 2 |
| Adtech domain context | docs/ADTECH-CONTEXT.md | MVP 2 |
| Final execution rules | docs/EXECUTION-RULES.md | MVP 1 |
| Active task plan | tasks/todo.md | MVP 1 |
| Self-improvement log | tasks/lessons.md | MVP 1 |
| Extensible scraper registry | backend/agents/base.py, backend/agents/registry.py | MVP 1 |
| Multi-agent rules (applies to all agents) | backend/agents/AGENT.md | MVP 1 |
| LinkedIn agent | backend/agents/linkedin/AGENT.md | MVP 1 |
| JobServe agent | backend/agents/jobserve/AGENT.md | MVP 1 |
| Ranking agent | backend/agents/ranking/AGENT.md | MVP 2 |
| RAG agent | backend/agents/rag/AGENT.md | MVP 2 |
| Cover letter agent | backend/agents/cover-letter/AGENT.md | MVP 2 |
| Question answer agent | backend/agents/question-answer/AGENT.md | MVP 2 |
| Security agent | backend/agents/security/AGENT.md | MVP 2 |
| Observability agent | backend/agents/observability/AGENT.md | MVP 3 |
| Orchestrator agent | backend/agents/orchestrator/AGENT.md | MVP 2 |
| Application assistant agent (optional) | backend/agents/application-assistant/AGENT.md | Optional |
| Interview prep agent (optional) | backend/agents/interview-prep/AGENT.md | Optional |
| Prompt engineering standards | prompts/AGENT.md | MVP 1.1 |
| All prompt files and versioning | prompts/ | MVP 1.1 |
| Infrastructure — Azure | infrastructure/terraform/azure/ | MVP 2 |
| Infrastructure — AWS | infrastructure/terraform/aws/ | MVP 2 |
| CI/CD | infrastructure/AGENT.md | MVP 1 |
| Docker multi-stage build | Dockerfile, nginx.conf, supervisord.conf | MVP 1 |
