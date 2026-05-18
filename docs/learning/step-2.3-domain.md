# Learning: Step 2.3 - Domain Logic

## Learning Objectives
- Learn to model core domain entities using Pydantic.
- Understand the concept of progressive enhancement from rule-based to AI-based logic.

## Technical Details
- **Pydantic Models**: The `models.py` file uses Pydantic's `BaseModel` to strictly define the shape of `Job` and `ScrapeResult` objects. This prevents bad data from ever entering the system. For instance, `Field(default_factory=utc_now)` guarantees a timezone-aware timestamp for when a job is scraped without manual intervention.
- **Progressive Enhancement**: In `filters.py`, we implement a rudimentary, hardcoded keyword filter. The architecture plan outlines that this will be swapped for a robust AI ranking agent in MVP 2. Structuring it in a standalone `filters.py` file allows us to swap the implementation later without refactoring the entire codebase.
