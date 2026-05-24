# Step 6.4: Prompt Architecture Alignment & MVP 1.1 Gap Fixes

**Date:** 2026-05-24

## Context
During the MVP 1.1 transition phase, there were discrepancies between the defined Jira Epic JD-E6 tasks and the finalized multi-file architectural proposal (`docs/proposal-v4-structure.md`). Although many prompt infrastructure pieces were constructed, certain global configurations and dependencies were missed.

## What Was Missing
1. **Global Grounding File**: `config/relevance_profile.yaml` was listed in the proposal as the MVP 1.1 grounding substitute but was not physically created on the disk.
2. **Dynamic Filtering Integration**: While `filters.py` was updated, the actual scraper agents (`linkedin_agent.py` and `jobserve_agent.py`) were not fetching the `UserProfile` or merging keywords before calling the filter.
3. **Pre-Flight Prerequisites**: The `require_rag_ready` dependency mandated by `backend/api/dependencies.py` to protect AI endpoints before CVs and profiles are ready was not scaffolded.
4. **Prompt Directory Adherence**: `linkedin-agent` and `jobserve-agent` erroneously contained `filtering.md`, violating the strict 6-file schema dictated by the v4 proposal (where `filtering.md` is strictly reserved for the `ranking-agent`).

## Resolution
- Created the missing `config/relevance_profile.yaml` housing default keys (`seniority_keywords`, `stack_keywords`, `contract_keywords`).
- Implemented `load_relevance_profile` via `pyyaml` inside `backend/filters.py` to seamlessly blend runtime user configuration with the system defaults.
- Updated `linkedin_agent.py` and `jobserve_agent.py` to fetch the `UserProfile` via `profiles_db.get(SINGLE_USER_ID)` and pass the dynamic keywords into `filter_jobs`.
- Removed `filtering.md` from `prompts/linkedin-agent/` and `prompts/jobserve-agent/` to strictly comply with the 6-file prompt architecture rules.
- Added `backend/api/dependencies.py` defining the `require_rag_ready` guard logic.
- Wired the `require_rag_ready` FastAPI dependency directly into `backend/api/v1/jobs.py` for the RAG enabled `/{job_id}/ask` route.

## Workflow Rule Reinforcement
The user initiated the fix via "YOLO mode". It was critical to remember that even in "YOLO mode", structural rules still govern the system. Specifically, any ad-hoc gaps fixed MUST be immediately documented in `docs/tasks/todo.md` and `docs/tasks/lessons.md`. This maintains alignment between the agent’s execution log and the real state of the repository.
