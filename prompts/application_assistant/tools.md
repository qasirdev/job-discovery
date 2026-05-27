<tools>
  <tool>
    <name>get_application_status</name>
    <description>Retrieves the current status of a job application using the job_id.</description>
  </tool>
  <tool>
    <name>update_application_status</name>
    <description>Updates the status of a job application for the given job_id.</description>
  </tool>
  <tool>
    <name>draft_email</name>
    <description>Drafts an email based on the specified intent and context.</description>
  </tool>
</tools>

<tool_guardrails>
  - Email drafting must not send the email automatically; it only generates the draft.
  - Status updates must be restricted to valid state transitions.
</tool_guardrails>
