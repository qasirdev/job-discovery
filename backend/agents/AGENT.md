# AGENT.md — Multi-Agent Architecture

## Cross-Agent Rules
1. **No Monoliths**: Agents must be small and specialized. Do not write "God" classes.
2. **Inheritance**: All scraper agents must extend `BaseScrapeAgent`.
3. **DIFA Compliance**: All network calls must implement Detect, Isolate, Fallback, Alert.
4. **ReAct Loop**: Agents must reason about their state before acting.
5. **OWASP Validation**: All inputs and outputs must be sanitized.
6. **Logging**: All agents must import `get_logger` from `backend.logging_config`. Do not use `print()`.
7. **TOON**: All agents if possible use Token-Oriented Object Notation (TOON) where possible to reduce token usage.
8. **Pydantic**: All agents must use Pydantic models for data validation on request and response.
9. **Agent Documentation**: Every agent directory MUST contain an `AGENT.md` file that strictly documents its purpose. It must follow this exact format:
   ```markdown
   # [Agent Name]

   - **Role**: [Brief description of what the agent does]
   - **Input**: `[Type]` ([Description of input])
   - **Output**: `[Type]` ([Description of output])
   ```


## Subagent Execution Rules
- **One Task**: Offload discrete logic to subagents.
- **Context Window Discipline**: Only pass necessary data to avoid exceeding LLM context limits.
- **Result Summarization**: Subagents return structured summary JSON, not raw logs.
- **Escalation**: If a subagent fails, it escalates to the orchestrator instead of silent failure.
