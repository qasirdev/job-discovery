# Learning: Step 2.2 - Core Config

## Learning Objectives
- Learn how to strictly validate environment variables using Pydantic Settings.
- Understand the importance of structured JSON logging for observability.

## Technical Details
- **Pydantic Settings**: By defining a `Settings` class inherited from `BaseSettings`, the application strictly types its environment variables. If a required variable is missing or formatted incorrectly, the app crashes immediately on startup ("fail fast"). This prevents confusing runtime errors later in execution.
- **Structured JSON Logging**: Traditional `print()` or plain text logs are hard to parse at scale. The `logging_config.py` overrides Python's default formatter to emit single-line JSON strings containing `timestamp`, `level`, `name`, and `message`. This adheres to Twelve-Factor App principles (Factor XI: Logs as event streams) and allows log aggregators (like Datadog or Loki) to query logs structurally (e.g., finding all errors by searching `level="ERROR"`).
