# TOOLS — RAG Agent

This file outlines permitted tools for the RAG Agent.

## Permitted Tools
1. **`retrieve_context`**: Query local profiles and return top matches.
2. **`query_embeddings`**: Get embedding vectors for incoming queries.

## Guardrails & Safeties
- The agent has zero system file-access permissions.
- Database access is strictly read-only for candidate profile information.
