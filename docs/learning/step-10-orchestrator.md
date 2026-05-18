# Learning: Step 10 - Security & Workflow Orchestration

## Learning Objectives
- Learn the role of an Orchestrator in a multi-agent system.
- Understand how to embed security early in the pipeline.

## Technical Details
- **Orchestrator Pattern**: The `OrchestratorAgent` acts as the conductor. It doesn't score jobs or write letters; it coordinates the sequence. If the `SecurityAgent` flags an input, the pipeline stops. If the `RankingAgent` gives a low score, it halts early to save token costs. This demonstrates the DIFA framework (Detect, Isolate, Fallback, Alert).
- **Security Validation**: We assume LLMs are vulnerable to Prompt Injection. By passing all scraped data through `SecurityAgent.validate_for_injection()` *before* handing it to the AI for scoring, we prevent malicious job posters from hijacking our autonomous loop.
