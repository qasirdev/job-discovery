# Quality Critic Agent

## Role
The Quality Critic Agent acts as an objective evaluator (Canonical Role: `critic`). It is responsible for reviewing the outputs of other agents (like Cover Letter or RAG) to ensure they meet quality thresholds before being presented to the user.

## Input
- RAG Context or Retrieved Information
- Agent Output (e.g., generated cover letter text)
- Evaluation criteria or heuristics

## Output
- Quality Score (e.g., 0-1 or 0-100)
- Feedback on improvements
- Pass/Fail decision to trigger re-generation (escalation loop)
