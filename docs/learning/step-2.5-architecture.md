# Learning: Step 2.5 - Architecture Docs

## Learning Objectives
- Learn the value of recording system-level goals and constraints alongside code.
- Understand modern resilience engineering patterns (DIFA).

## Technical Details
- **Architecture as Code**: By keeping `.md` files like `ARCHITECTURE.md` and `RELIABILITY.md` in the `docs/` folder instead of an external wiki, the reasoning behind the code travels *with* the code. AI agents can read these files to ensure they don't break fundamental design constraints (like "No monolithic agents").
- **DIFA Framework**: This acronym stands for Detect, Isolate, Fallback, Alert. It is a critical heuristic for robust software. When making an external network call (like scraping), you must *detect* failure, *isolate* it so the whole system doesn't crash, attempt a *fallback*, and *alert* the observability layer.
