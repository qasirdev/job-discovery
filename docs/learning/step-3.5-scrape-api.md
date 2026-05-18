# Learning: Step 3.4 & 3.5 - Scrape API and Orchestration

## Learning Objectives
- Learn how to build a dynamic API endpoint that leverages the Factory/Registry pattern.
- Understand the benefits of decoupling API routing from agent logic.

## Technical Details
- **Dynamic API Routing**: The `/scrape` endpoint does not hardcode `LinkedInAgent().run()`. Instead, it checks the incoming `source_id`. If `None`, it iterates over all agents returned by `get_all_agents()`. This means that when a new developer adds a `GithubAgent` in the future, the `/scrape` API automatically knows how to run it without a single line of code changing in `routers/scrape.py`.
- **Fault Tolerance**: The API loops through agents using a `try/except` block. If the JobServe agent crashes due to a website change, it logs the exception and returns an error payload for that specific agent, but allows the LinkedIn agent to continue running successfully. This prevents cascading failures.
