# TOOLS — LinkedIn Agent

This file outlines the external tools and API calls the LinkedIn Agent is permitted to execute.

## Permitted Tools
1. **`extract_job_details`**: Parses target HTML structure and extracts structured metadata.
2. **`normalize_field`**: Standardizes string inputs such as location, posted date format, or company name suffix.

## Restrictive Safeguards
- The agent is strictly prohibited from invoking any generic terminal execution tools.
- Outbound network requests are limited exclusively to `https://www.linkedin.com/` domain and authenticated proxy targets.
- Local system file-access operations are limited to reading config assets.
