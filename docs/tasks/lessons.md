# Self-Improvement & Lessons Log

This file acts as the AI Agent's memory for corrections and best practices.

## Entries

| Date | Issue/Mistake | Root Cause | Rule to Prevent Recurrence |
|------|---------------|------------|-----------------------------|
| 2026-05-18 | `ImportError: attempted relative import with no known parent package` when starting Uvicorn | Running `uvicorn main:app` directly from the `backend/` directory causes `main.py` to be loaded as a top-level script, which breaks its package-relative imports. | Run uvicorn from the monorepo root using `uv run --project backend uvicorn backend.main:app --app-dir .` to ensure the parent package is correctly resolved. |
