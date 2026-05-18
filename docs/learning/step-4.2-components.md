# Learning: Step 4.2 - React Components

## Learning Objectives
- Learn how to structure atomic React components.
- Understand how to connect a frontend button to a backend API.

## Technical Details
- **Atomic Components**: By splitting the UI into `JobCard`, `FilterBar`, and `ScrapeButton`, the codebase becomes highly reusable and testable.
- **Client vs Server Components**: In Next.js, files run on the server by default. The `ScrapeButton` has an interactive `onClick` handler and uses React state (`useState`). Therefore, it requires the `"use client"` directive at the top of the file so Next.js knows to hydrate it with JavaScript in the browser.
- **API Fetching**: The `ScrapeButton` makes a `POST` request to `/api/v1/scrape/`. Because we use Nginx as a reverse proxy, the frontend doesn't need to know that the backend is actually running on `localhost:8000`. It just sends the request to the same domain.
