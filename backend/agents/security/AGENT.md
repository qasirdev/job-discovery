# Security Agent

- **Role**: Analyze job descriptions to detect malicious payloads or prompt injection attacks. Ensure OWASP standard compliance across incoming requests.
- **Input**: `string` (Job Description text, arbitrary LLM inputs)
- **Output**: `SecurityValidationResult` (Safety status and violation reason)
- **Responsibilities**:
  - Prompt injection detection using system prompt pattern matching.
  - Payload sanitisation via `bleach` (stripping arbitrary HTML, keeping safe tags).
  - Validating requests against Pydantic schemas (`extra="forbid"`).
  - RBAC enforcement (`admin-claim` checking).
  - Context isolation across downstream agents.
  - Writing structured audit logs to `logger("security")` (hashing inputs).
