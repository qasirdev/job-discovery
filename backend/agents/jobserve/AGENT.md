# JobServe Agent

- **Role**: Scrape IT job postings from JobServe using randomized search patterns and pagination to avoid detection.
- **Input**: `JobRepository`, `int` (The database repository to upsert jobs and max_jobs limit)
- **Output**: `ScrapeResult` (Summary of the scrape execution including jobs found, saved, and errors)

## Additional Rules
- **Search Patterns**: Randomize search patterns and keywords to avoid triggering rate limits.
- **Pagination Randomization**: Do not scrape pages perfectly sequentially (e.g. 1, 2, 4, 3, 5).
- **Data Normalization**: Extract raw HTML blocks into the clean `Job` Pydantic schema.
- **Anti-Detection**: Ensure headless browsers have randomized fingerprints.
- **Source ID**: `jobserve`
