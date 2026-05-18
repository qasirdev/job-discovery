# AGENT.md — Frontend Standards

## Frontend Stack
- **Framework**: Next.js 16 (React 19)
- **Styling**: Tailwind CSS 4
- **Language**: TypeScript (strict mode)
- **Data Fetching**: Static generation or client-side fetch (due to `output: "export"`)

## Dashboard Features (MVP 1)
- List aggregated jobs from memory/DB.
- Trigger scraper APIs manually.

## Architectural Constraints
- **Static Export**: We are using `output: "export"` to compile the frontend to static HTML/JS. This is served by Nginx inside our Docker container.
- **No Server Actions**: Because of the static export, React Server Components cannot run dynamic code (like querying a DB) at request time. All dynamic data fetching must happen client-side against the FastAPI `/api/` layer.
