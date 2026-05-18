# AGENT.md — LinkedIn Agent

- **Responsibilities**: Scrape job postings from LinkedIn respecting anti-bot measures.
- **Anti-bot Strategy**: Randomize delays (3-7s), rotate user agents via Playwright stealth.
- **Execution Interval**: Run every 3–5 hours.
- **Randomization Rules**: Paginate randomly. Do not scrape perfectly sequentially.
- **Deduplication**: Match by job title and company string to prevent duplicates.
- **Source ID**: `linkedin`
