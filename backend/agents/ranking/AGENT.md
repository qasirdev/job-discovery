# Ranking Agent

- **Role**: Evaluate job relevance against a candidate profile through a deterministic multi-step pipeline.
- **Input**: `Job`
- **Output**: `RankingResult` containing the final AI match score and metadata.

## AI Ranking Execution Model (Serverless AI Ranking Support)
The Ranking Agent executes via dedicated Temporal worker queues rather than the primary HTTP pool.
**Benefits**:
- **Burst scaling**: Workers can scale from 0 to N to handle batch ranking of hundreds of scraped jobs without impacting API latency.
- **Reduced idle compute cost**: Scale-to-zero capabilities in Azure Container Apps ensure we do not pay for heavy AI workload instances when no scrapes are running.
- **Isolation of expensive AI workloads**: Ranking consumes significant CPU and memory. Isolating it prevents HTTP worker starvation.

## Architectural Rule
**"Ranked jobs become searchable only after scoring completes"**
Unscored jobs must remain hidden from the frontend Dashboard until the Ranking Agent successfully completes its evaluation and updates the database.

## Scoring Pipeline (8 Steps)
The Ranking Agent scoring pipeline executes exactly 8 steps:
1. **Embeddings**: Generate dense vectors for the job description using `pgvector`.
2. **Cosine Similarity**: Compare job vectors against the candidate profile embeddings.
3. **Cross-encoder Reranking**: Apply a cross-encoder model for fine-grained relevance scoring.
4. **Sentiment**: Analyze the job posting sentiment (e.g., urgency, red flags).
5. **Recruiter Quality**: Factor in the associated recruiter's interaction score and history.
6. **Compensation Normalisation**: Standardise salary bands to compare against candidate expectations.
7. **Skill Extraction**: Extract and match hard and soft skills.
8. **Seniority Validation**: Enforce strict seniority boundaries (e.g., blocking mid-level roles for staff-level profiles).
