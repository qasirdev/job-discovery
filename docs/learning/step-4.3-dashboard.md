# Learning: Step 4.3 - Dashboard Layout

## Learning Objectives
- Learn how to compose a full page from atomic components.
- Understand the role of mock data during early-stage prototyping.

## Technical Details
- **Composition**: `page.tsx` is the root layout for the main URL (`/`). It acts as a container, managing the spacing (using Tailwind's `max-w-6xl` and `space-y-6`) and importing the `FilterBar`, `ScrapeButton`, and multiple `JobCard` components.
- **Prototyping Strategy**: Because the backend database (Supabase) isn't ready in MVP 1, we use a `mockJobs` array. This allows the frontend developer to iterate on design, layout, and responsiveness immediately without being blocked by backend engineering progress.
