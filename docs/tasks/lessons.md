# Self-Improvement & Lessons Log

This file acts as the AI Agent's memory for corrections and best practices.

## Entries

| Date | Issue/Mistake | Root Cause | Rule to Prevent Recurrence |
|------|---------------|------------|-----------------------------|
| 2026-05-18 | `ImportError: attempted relative import with no known parent package` when starting Uvicorn | Running `uvicorn main:app` directly from the `backend/` directory causes `main.py` to be loaded as a top-level script, which breaks its package-relative imports. | Run uvicorn from the monorepo root using `uv run --project backend uvicorn backend.main:app --app-dir .` to ensure the parent package is correctly resolved. |
| 2026-05-18 | Next.js API fetches returning 404 HTML (Unexpected token '<' is not valid JSON) in dev mode | Fetching relative path `/api/...` in Next.js dev mode queries port 3000 instead of port 8000, failing to route to FastAPI. | Add development-only rewrites to `next.config.ts` to proxy all `/api/` paths directly to the backend API origin. |

| 2026-05-22 | New QA Agent implementation lacked full XML prompt directory architecture | The AI implemented `QA Agent` rapidly but bypassed the mandatory 6-file prompt architecture rules (`CONTRACT.md`, `system.md`, etc.). | Always strictly follow `prompts/AGENT.md` rules when bootstrapping a new agent. No exceptions for speed. |
| 2026-05-22 | Missing `AGENT.md` docs inside `backend/agents/` subdirectories | When scaffolding new agents (e.g. observability, security), documentation inside the folder was omitted. | Always create an `AGENT.md` detailing Role, Input, and Output inside every `backend/agents/<name>/` directory upon creation. |
| 2026-05-22 | JobServe scraper extracting volatile session links that broke after minutes | The scraper extracted the `href` attribute which contained a Search Hash ID (`shid`) tied to a temporary web session. | When extracting links from Job boards, ignore query parameters like `shid` and reconstruct permalinks using the DOM element `id` instead. |
