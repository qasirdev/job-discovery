# Learning: Step 18 — Infrastructure Documentation

## Learning Objectives
What a beginner developer should learn from the documentation setup introduced in Epic 18 (JD-84, JD-85, JD-86):
1. **Feature Flags**: How feature flags enable progressive delivery and decouple deployment from release.
2. **Rate Limiting**: Why outbound scraping requires sophisticated pacing, adaptive throttling, and circuit breakers.
3. **Local LLMs**: How to set up a private, offline-capable AI environment using `llama.cpp` and `uv` in Docker.

## Technical Details

### Feature Flags
Feature flags are not just configuration—they are dynamic switches that allow you to turn features on or off for specific users or percentages of traffic without deploying new code. In this project, we implement an OpenFeature-compatible API with fallback to a Supabase database table, ensuring vendor neutrality while allowing immediate "kill-switch" capabilities for faulty features.

### Scraping Rate Limits
Web scraping requires careful consideration to avoid overwhelming target servers or triggering anti-bot protections. Our strategy includes:
- **Randomised Pacing**: Adding jitter to delays prevents predictable bot-like access patterns.
- **Circuit Breakers**: Stopping completely if 3 consecutive failures occur, preventing a "thundering herd" problem or getting an IP permanently banned.
- **Session Rotation**: Constantly changing User-Agents and browser contexts to maintain anonymity.

### Local LLM Runtime
Running LLMs locally provides strict data privacy guarantees (no data sent to OpenAI/Anthropic) and operates offline. 
- **GGUF Models**: A quantization format that drastically reduces memory requirements, allowing large models to run on standard consumer hardware.
- **uv Package Manager**: `uv` is used inside our Docker containers because it is significantly faster than standard `pip` for dependency resolution, which speeds up container builds immensely.
