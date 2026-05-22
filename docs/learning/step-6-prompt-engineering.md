# Learning: Step 6 - Prompt Engineering Infrastructure

## Learning Objectives
- Learn the benefits of XML-structured prompts for deterministic agent behavior.
- Understand how to enforce the ReAct (Reason + Act) loop at the system level.

## Technical Details
- **XML Structure**: We store our system instructions in `.xml` files instead of Python strings. Modern frontier models (like Claude 3 and GPT-4) parse XML exceptionally well. It cleanly separates the `<identity>` rules from the `<constraints>` and `<examples>`.
- **ReAct Loop Enforcement**: By writing `<thought>...</thought>` in our few-shot examples, we are "priming" the LLM to ALWAYS output its internal reasoning before it outputs the final JSON payload. This drastically reduces hallucinations because the model generates its rationale token-by-token before committing to an answer.
- **Robust Scraper Prompts**: Web scrapers facing dynamic DOMs (like LinkedIn) require resilient instructions. In our `skills.md`, we explicitly map *fallback selectors* (e.g. `.topcard__title`, `h1.t-24`) so the agent knows what to try if primary CSS classes change. 
- **Session-Based Pagination**: For sites with strict unauthenticated limits (10-25 results), our system prompts document the explicit requirement to supply valid session cookies (e.g., `li_at`) to bypass headless browser pagination walls.
