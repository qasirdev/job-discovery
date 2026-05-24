# AGENT.md — Backend API Standards

## Backend Stack
- **Language**: Python 3.14
- **Framework**: FastAPI
- **Package Manager**: uv
- **Validation**: Pydantic v2

## API Design Standards
1. **Typed Objects**: All request and response bodies MUST be strictly typed using Pydantic models.
2. **Schema-First**: Leverage FastAPI's automatic OpenAPI specs.
3. **Versioning**: All routes must be mounted under `/api/v1/`.
4. **Pagination**: Use cursor-based pagination for list endpoints.
5. **Errors**: Use RFC 7807 structured errors.
6. **Connection Pooling**: Use asyncpg pool (`pool_size=10`, `max_overflow=20`) to handle high concurrency.
7. **Architecture**: Enforce a Domain-driven folder layout.

## MCP Integration Rules
- Expose necessary endpoints via Model Context Protocol to allow the orchestrator agent and subagents to discover API capabilities dynamically.

## Prompt Caching Strategy
- Leverage LiteLLM caching with Redis to drastically reduce API costs on repeated evaluation or reasoning steps. Cache keys should include the agent ID, prompt hash, and job context.
