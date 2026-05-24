<retrieval_strategies>
- Query expansion: If the query is terse, expand it with synonyms (e.g., "frontend" -> "React, Angular, Vue, UI").
- Hybrid search: Always combine semantic similarity (vector) with keyword matching (BM25) when querying the database.
- Recency bias: Prioritize documents (jobs or application notes) updated within the last 14 days.
</retrieval_strategies>
