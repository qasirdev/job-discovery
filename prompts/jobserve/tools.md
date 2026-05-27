<tools>
  <tool>
    <name>extract_job_details</name>
    <description>Parses target HTML structure and extracts structured metadata.</description>
  </tool>
  <tool>
    <name>normalize_field</name>
    <description>Standardizes string inputs such as location, posted date format, or company name suffix.</description>
  </tool>
</tools>

<tool_guardrails>
  - The agent is strictly prohibited from invoking any generic terminal execution tools.
  - Outbound network requests are limited exclusively to `https://www.jobserve.com/` domain and authenticated proxy targets.
  - Local system file-access operations are limited to reading config assets.
</tool_guardrails>
