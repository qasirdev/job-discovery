# Learning: Step 17 - QA Agent, UI Refactoring & JobServe Permalinks

## Learning Objectives
- Understand how to implement grounded Q&A using RAG.
- Understand how to handle cursor-based pagination state in React (Next.js) using TanStack Query.
- Understand the pitfalls of dynamic session URLs in web scraping (JobServe `shid` bug).

## 1. QA Agent Architecture (Grounded RAG)
When building an agent to answer user questions, hallucinations are the primary risk. The QA Agent (`backend/agents/qa/qa_agent.py`) is designed with strict boundaries:
- **XML Context**: The system prompt (`prompts/qa-agent/system.md`) explicitly injects the Job Description and the Candidate Context as bounded reference data.
- **Guardrails**: If the user asks a question about a detail *not* in the job description (e.g. salary when unlisted), the agent is instructed to state that the information is missing rather than inventing it.

## 2. React Cursor Pagination (Next.js UI)
Converting a grid layout to a paginated list view requires careful state management.
- We used **TanStack Query** (`useQuery`) keyed by `[source, keyword, limit, currentCursor]` to ensure caching and automatic refetching when controls change.
- **Cursor History**: Because keyset pagination (unlike offset pagination) doesn't inherently know the "previous" page cursor, we maintain a `cursorHistory` array in React state.
  - When clicking **Next**: push current cursor to history, set new cursor.
  - When clicking **Previous**: pop the last cursor from history, set as current.

## 3. Web Scraping: Volatile Session URLs vs Permalinks (JobServe Bug)
We encountered a bug where JobServe URLs clicked on the frontend showed no job.
- **The Issue**: JobServe's search results anchor tags (`<a href="...shid=...">`) contain a **Search Hash ID** (`shid`). These are temporary session tokens. They expire shortly after the scraper finishes.
- **The Fix**: Instead of extracting the volatile `href` attribute, we inspect the DOM for a stable, unique identifier. JobServe places the permanent Job ID inside the `id` attribute of the `<li>` element.
- **Lesson**: When scraping, *never* trust query parameters that look like session hashes (`sid`, `shid`, `session`, `tok`). Always try to reconstruct the application's clean permalink route (`/job/{id}`) using intrinsic unique IDs found in the DOM.
