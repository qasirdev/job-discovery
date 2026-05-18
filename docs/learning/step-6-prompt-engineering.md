# Learning: Step 6 - Prompt Engineering Infrastructure

## Learning Objectives
- Learn the benefits of XML-structured prompts for deterministic agent behavior.
- Understand how to enforce the ReAct (Reason + Act) loop at the system level.

## Technical Details
- **XML Structure**: We store our system instructions in `.xml` files instead of Python strings. Modern frontier models (like Claude 3 and GPT-4) parse XML exceptionally well. It cleanly separates the `<identity>` rules from the `<constraints>` and `<examples>`.
- **ReAct Loop Enforcement**: By writing `<thought>...</thought>` in our few-shot examples, we are "priming" the LLM to ALWAYS output its internal reasoning before it outputs the final JSON payload. This drastically reduces hallucinations because the model generates its rationale token-by-token before committing to an answer.
