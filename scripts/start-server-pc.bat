@echo off
REM start-server-pc.bat
REM Local LLM Runtime support script for PC (Windows)
REM Features: llama.cpp GGUF models (openai/gpt-oss-120b), CUDA GPU acceleration, KV cache reuse
REM Hybrid routing via LiteLLM, OpenRouter integration.
REM Python dependencies managed by 'uv' inside the container.

echo Starting AI-Powered Job Discovery Platform - Local LLM (PC)

cd %~dp0\..

if "%OPENROUTER_API_KEY%"=="" (
  echo Notice: OPENROUTER_API_KEY is not set. OpenRouter integration will be disabled. Processing will be privacy-friendly and offline.
) else (
  echo OpenRouter integration enabled for hybrid local/cloud routing via LiteLLM.
)

echo Building job-discovery-local-llm container...
REM The Dockerfile should use 'uv' for python packaging.
docker build -t job-discovery-local-llm -f Dockerfile.local-llm .

echo Starting container with CUDA GPU acceleration (--gpus all)...
REM Assuming NVIDIA GPU and CUDA are available via WSL2/Docker Desktop for Windows
docker run -d --name job-discovery-local-llm ^
  --gpus all ^
  --restart unless-stopped ^
  -p 4000:4000 ^
  -p 8080:8080 ^
  -e OPENROUTER_API_KEY="%OPENROUTER_API_KEY%" ^
  -e LOCAL_MODEL="openai/gpt-oss-120b" ^
  -e KV_CACHE_REUSE="true" ^
  job-discovery-local-llm

echo Local LLM server started successfully.
