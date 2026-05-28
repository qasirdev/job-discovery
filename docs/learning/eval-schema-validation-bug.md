# Eval Schema Validation for Utility Agents

**Date**: 2026-05-28
**Context**: Fixing schema validation failures in `run_evals.py` during fast mode (`--fast`).

## Issue
When running `uv run --project backend python -m backend.admin.run_evals --all --fast`, utility agents (like `quality_critic`, `ranking`, `security`, `cover_letter`, `orchestrator`, and `question_answer`) were failing the schema validation check with errors like `Missing required field: 'title'` or `Field 'source' mismatch`.

## Root Cause
The `evaluate_schema_compliance` function in `backend/admin/run_evals.py` was written with an assumption that any agent not explicitly handled (like `rag` or `observability`) was a scraper agent. Scraper agents are expected to return a standard `REQUIRED_FIELDS` schema: `["title", "company", "location", "description", "source"]` and they are expected to have a `source` field matching the agent name. 

However, utility agents have their own specific schemas (e.g., `ranking` returns `["is_relevant", "score"]`) and do not have a `source` field.

## Resolution
1. **Schema Mapping**: Explicitly define the `req_fields` for each utility agent in the `evaluate_schema_compliance` function in `run_evals.py`.
2. **Source Field Bypass**: Add the utility agents to the exclusion list for the `source` field check.

## Lesson
When adding new agent types (utility, orchestrator, critic) to a system originally built for a specific domain (like web scraping), always audit global validation scripts (`run_evals.py`, `filters.py`) to ensure they don't apply domain-specific assumptions (like a `source` field) to domain-agnostic agents.
