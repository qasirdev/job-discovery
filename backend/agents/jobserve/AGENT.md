# AGENT.md — JobServe Agent

- **Responsibilities**: Scrape IT job postings from JobServe.
- **Search Patterns**: Randomize search patterns and keywords to avoid triggering rate limits.
- **Pagination Randomization**: Do not scrape pages perfectly sequentially (e.g. 1, 2, 4, 3, 5).
- **Data Normalization**: Extract raw HTML blocks into the clean `Job` Pydantic schema.
- **Anti-Detection**: Ensure headless browsers have randomized fingerprints.
- **Source ID**: `jobserve`
