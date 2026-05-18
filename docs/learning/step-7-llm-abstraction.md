# Learning: Step 7 - LLM Abstraction Layer

## Learning Objectives
- Learn how to decouple the core application from specific LLM vendors.
- Understand how to enforce deterministic JSON outputs.

## Technical Details
- **LiteLLM**: The platform uses `litellm` (configured in `client.py`) instead of the official OpenAI or Anthropic SDKs. This allows the orchestrator to dynamically swap between models (e.g., Claude 3 Haiku for initial scoring, GPT-4 for complex reasoning) simply by changing the `DEFAULT_MODEL` string in the `.env` file, without rewriting any integration code.
- **Observability**: `logging.py` implements a transaction logger. Every API call records the exact number of tokens used and the total cost. This is critical in production to prevent runaway loops from bankrupting the project.
