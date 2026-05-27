# Learning: Ragas Evaluation in CI Pipeline

## Context
As part of MVP 2.1 (JD-48), we integrated Ragas for evaluating our RAG pipeline, specifically targeting `ContextPrecision` and `ContextRecall` to ensure our retriever is surfacing relevant resume chunks and job descriptions.

## Implementation Decisions

### Graceful Degradation
Ragas utilizes `scikit-network` as a transitive dependency, which compiles C++ extensions during installation. On some local development environments (e.g. macOS ARM64 without `-stdlib=libc++` flags), this compilation can fail. 
To adhere to the Twelve-Factor App principles and ensure developers without full C++ toolchains can still run basic evaluations, `run_evals.py` gracefully degrades:
- It attempts to import `ragas`.
- If missing, it logs a warning and falls back to **fast mode (schema-only checking)**.
- This ensures CI (running on Ubuntu runners with pre-built binary wheels) can run the heavy Ragas checks while local development remains unblocked.

### Dataset Adaptation
`ragas.evaluate()` strictly requires a HuggingFace `Dataset` object. We transform our JSON fixtures into this format on-the-fly, ensuring our single `eval-set-v1.json` standard format is portable across different evaluation frameworks (DeepEval, Ragas, or manual checks).

### Hard Thresholds
- `ContextPrecision >= 0.80`
- `ContextRecall >= 0.75`

Any evaluation case that drops below these thresholds triggers an immediate `ERROR` level log and forces a non-zero exit code, effectively blocking broken retrieval logic from being merged.
