# Learning: Step 16.1 - Workflow Orchestration

## Learning Objectives
- Understand the importance of structured process tracking for AI-assisted or autonomous development.
- Learn how a `lessons.md` file creates an iterative feedback loop for improvement.

## Technical Details
- **`todo.md`**: Instead of relying purely on memory or scattered Jira tickets, an active markdown-based to-do list provides a deterministic, version-controlled state machine for the project. Autonomous agents use this to know exactly what step they are on and what comes next.
- **`lessons.md`**: Autonomous development requires self-correction. The lessons log acts as an artificial "memory". Every time an error is made, the root cause is documented along with a preventative rule. Agents are instructed to read this at the start of a session, enforcing continuous improvement and preventing repeated mistakes.
