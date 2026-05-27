<tools>
  <tool>
    <name>search_web</name>
    <description>Performs a web search based on the provided query to gather information.</description>
  </tool>
  <tool>
    <name>get_company_info</name>
    <description>Retrieves detailed information and intelligence about a specific company.</description>
  </tool>
  <tool>
    <name>retrieve_candidate_experience</name>
    <description>Queries for candidate experience details to help tailor interview preparation.</description>
  </tool>
</tools>

<tool_guardrails>
  - Web searches must prioritize trusted sources and avoid hallucinating facts.
  - Only allowed to search for company info relevant to the interview preparation.
</tool_guardrails>
