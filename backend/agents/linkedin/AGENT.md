# LinkedIn Agent

- **Role**: Scrape job postings from LinkedIn respecting anti-bot measures by randomizing delays and rotating user agents.
- **Input**: `JobRepository`, `int` (The database repository to upsert jobs and max_jobs limit)
- **Output**: `ScrapeResult` (Summary of the scrape execution including jobs found, saved, and errors)

## Additional Rules
- **Anti-bot Strategy**: Randomize delays (3-7s), rotate user agents via Playwright stealth.
- **Execution Interval**: Run every 3–5 hours.
- **Randomization Rules**: Paginate randomly. Do not scrape perfectly sequentially.
- **Deduplication**: Match by job title and company string to prevent duplicates.
- **Source ID**: `linkedin`
