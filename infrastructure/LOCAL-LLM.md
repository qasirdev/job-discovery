# Local LLM Runtime Support

The platform supports running AI models locally to provide privacy-friendly processing and offline-capable AI workflows without relying on external APIs.

## Capabilities
- **llama.cpp-compatible runtime**: Native support for running GGUF quantized models on commodity hardware.
- **Hardware Acceleration**: Automatic GPU acceleration (Metal on Mac, CUDA on PC) and KV cache reuse for optimal inference speed.
- **OpenAI-compatible APIs**: Local inference exposes standard OpenAI API endpoints, allowing zero-code swapping in the backend.
- **OpenRouter integration**: Fallback and hybrid routing support via `OPENROUTER_API_KEY` through LiteLLM.
- **Recommended Model**: `openai/gpt-oss-120b` (or equivalent open-source reasoning model) specified for complex reasoning tasks.

## Containerization and Tooling
- All local LLM dependencies are packaged into a single Docker container.
- `uv` is enforced as the package manager for Python within the container to ensure fast, reproducible builds.

## Management Scripts
Dedicated start/stop server scripts are provided in the `scripts/` directory for seamless developer experience:
- `scripts/start-server-mac.sh`
- `scripts/start-server-pc.bat`
- `scripts/start-server-linux.sh`
