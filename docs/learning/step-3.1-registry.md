# Learning: Step 3.1 - Scraper Registry

## Learning Objectives
- Understand the Object-Oriented concept of Abstract Base Classes (ABC).
- Learn the Registry design pattern for dynamic plugin loading.

## Technical Details
- **Abstract Base Class (`base.py`)**: `BaseScrapeAgent` forces any new scraper (e.g., LinkedIn, Indeed) to look and behave the same way. They must define a `source_id` and implement the `run()` method returning a `ScrapeResult`. If they don't, Python will throw an error at runtime.
- **Registry Pattern (`registry.py`)**: Instead of having a massive `if/else` block to decide which scraper to run, we use a `@register` decorator. When a new scraper file is loaded, it automatically adds itself to the `_AGENTS` dictionary. This makes adding new scrapers a "plug-and-play" experience without modifying core orchestration logic.
