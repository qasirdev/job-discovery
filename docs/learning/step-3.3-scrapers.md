# Learning: Step 3.2 & 3.3 - Agent Implementation

## Learning Objectives
- Learn how to implement a specific sub-agent using an abstract base class.
- Understand the role of specific `AGENT.md` files for sub-agents.

## Technical Details
- **Base Class Implementation**: The `LinkedInAgent` extends `BaseScrapeAgent` and implements the asynchronous `run()` method. Because it uses the `@register` decorator, it's automatically loaded into the application's memory without needing to be manually imported into the orchestrator.
- **Sub-Agent `AGENT.md`**: Each agent directory (like `backend/agents/linkedin/`) has its own `AGENT.md`. This holds the highly specific "prompts" or rules for that exact module (e.g., "paginating randomly", "using a 3-7s delay"). An AI coding assistant will only read this when modifying the LinkedIn scraper, keeping context windows small and focused.
