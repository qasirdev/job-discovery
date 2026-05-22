# Learning: Eval Framework (DeepEval + Ragas)

## Learning Objectives
- Understand how to evaluate Generative AI agent outputs quantitatively.
- Learn how to integrate LLM-as-a-judge metrics into a continuous integration pipeline.
- Differentiate between Output Quality (DeepEval) and Retrieval Quality (Ragas).

## Technical Details

### 1. Output Quality (DeepEval)
We use `deepeval`'s `GEval` metric to judge the outputs of our scraper agents:
- **Faithfulness**: Ensures the agent didn't hallucinate. It compares the extracted JSON (Actual Output) against the raw HTML (Retrieval Context). If the agent invents a salary that wasn't in the HTML, Faithfulness drops. (Threshold: `>= 0.85`)
- **Answer Relevancy**: Ensures the agent actually extracted the core job description rather than boilerplate company headers. (Threshold: `>= 0.80`)

### 2. Retrieval Quality (Ragas)
For our RAG (Retrieval-Augmented Generation) agents, evaluating generation isn't enough; we must evaluate the vector search layer using `ragas`.
- **Context Precision**: Evaluates whether all the ground-truth relevant items were ranked highest in the vector search payload.
- **Context Recall**: Evaluates whether the vector search successfully retrieved *all* the necessary facts needed to answer the query.

### 3. Graceful CI Integration
Our `run_evals.py` acts as a facade. If Ragas' heavy C++ dependencies (`scikit-network`) fail to compile on a developer's local machine, the script gracefully catches the `ImportError` and falls back. In a clean CI/CD Ubuntu environment, dependencies install successfully, ensuring quality gates are enforced before deployment.
