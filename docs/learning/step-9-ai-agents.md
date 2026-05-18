# Learning: Step 9 - AI Agents (Ranking, RAG, Cover Letter)

## Learning Objectives
- Understand the role of specialized LLM agents in a micro-agent architecture.
- Learn how to structure and orchestrate interactions between different AI agents.

## Technical Details
- **Specialization**: Instead of one "God Agent" doing everything, we split tasks:
  - `RankingAgent`: Focuses entirely on matching a Job schema to a profile using deterministic logic.
  - `RAGAgent`: Focuses on semantic search and context retrieval to augment the context window without exceeding token limits.
  - `CoverLetterAgent`: Focuses on generative creativity, using the RAG context and the Job Description to draft highly targeted outreach.
- **Pydantic Validation**: Notice how `RankingAgent` forces the LLM to return data that matches the `RankingResult` Pydantic model. This guarantees our backend logic won't crash when trying to read the LLM's output.
