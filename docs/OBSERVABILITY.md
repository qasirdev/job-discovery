# Observability

- **OpenTelemetry**: Integrated into FastAPI to provide distributed tracing across scraper agents, orchestrator, and external LLM calls.
- **Metrics**: Token usage and scraping duration are actively tracked.
- **Logs**: JSON structured logs are sent to standard out for easy scraping by Datadog or ELK stack.
