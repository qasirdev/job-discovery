# AGENT.md — Frontend Standards

## Frontend Stack
- **Framework**: Next.js 16
- **React**: React 19 (hooks explicitly used: `use`, `useTransition`, `useOptimistic`, `useActionState`)
- **Styling**: Tailwind CSS 4 & MUI
- **Language**: TypeScript (strict mode)
- **Data Fetching & State**: TanStack Query (server state), Zustand (client state)
- **Validation**: Zod

## Component State & Error Handling
- **Empty States**: Must gracefully handle missing data (e.g., greyed out non-interactive sections with helper text).
- **API Fallbacks**: Use proper HTTP status codes. `409 Conflict` should gracefully swap UI actions (e.g. 'View' instead of 'Create'). `422 Unprocessable` should invalidate cache and show non-retryable toast messages. `500 Server Error` should allow safe retry.
- **Optimistic UI**: Use `useOptimistic` and `useTransition` for instant feedback on mutations.

## Dashboard Features (MVP 1)
AI relevance scoring, RAG insights, recruiter intelligence, cover letter generation, observability dashboards, token usage dashboards, agent traces, prompt debugging, saved jobs, filtering, dark/light mode.

## Architectural Constraints
- **Standalone Node.js Server**: We are using `output: "standalone"` to compile the frontend. Supervisor starts it as `node server.js` on port 3000. Nginx proxies port 80 to it. All dynamic data is fetched client-side from FastAPI at `/api/v1/*`.
- **No Server Actions**: Because of the standalone build, React Server Components cannot run dynamic code (like querying a DB) at request time. All dynamic data fetching must happen client-side against the FastAPI `/api/` layer.
