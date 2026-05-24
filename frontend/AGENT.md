# AGENT.md — Frontend Standards

## Frontend Stack
- **Framework**: Next.js 16 (React 19)
- **Styling**: Tailwind CSS 4
- **Language**: TypeScript (strict mode)
- **Data Fetching**: Static generation or client-side fetch

## Dashboard Features (MVP 1)
AI relevance scoring, RAG insights, recruiter intelligence, cover letter generation, observability dashboards, token usage dashboards, agent traces, prompt debugging, saved jobs, filtering, dark/light mode.

## Architectural Constraints
- **Standalone Node.js Server**: We are using `output: "standalone"` to compile the frontend. Supervisor starts it as `node server.js` on port 3000. Nginx proxies port 80 to it. All dynamic data is fetched client-side from FastAPI at `/api/v1/*`.
- **No Server Actions**: Because of the standalone build, React Server Components cannot run dynamic code (like querying a DB) at request time. All dynamic data fetching must happen client-side against the FastAPI `/api/` layer.
