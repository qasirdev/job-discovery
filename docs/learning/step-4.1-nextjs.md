# Learning: Step 4.1 - Next.js Static Export

## Learning Objectives
- Learn the limitations and benefits of Next.js static exports.
- Understand how `next.config.ts` controls the build output.

## Technical Details
- **`output: "export"`**: By default, Next.js spins up a Node.js server to dynamically render pages. However, to simplify our MVP architecture, we configure Next.js to produce a completely static bundle of HTML, JS, and CSS files. This allows us to serve the entire frontend using `Nginx`, which is incredibly fast and secure, alongside our Python backend in a single Docker container.
- **Trade-offs**: Because we export statically, we cannot use React Server Actions or API Route Handlers on the frontend. We must fetch data entirely on the client-side (`useEffect`, `SWR`, or `React Query`) by hitting the FastAPI endpoints.
