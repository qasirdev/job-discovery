#!/usr/bin/env bash
# start-server-linux.sh
# Local LLM Runtime support script for Linux
# Features: llama.cpp GGUF models (openai/gpt-oss-120b), NVIDIA/AMD GPU acceleration, KV cache reuse
# Hybrid routing via LiteLLM, OpenRouter integration.
# Python dependencies managed by 'uv' inside the container.

set -e

echo "Starting AI-Powered Job Discovery Platform - Local LLM (Linux)"

cd "$(dirname "$0")/.."

if [[ -z "${OPENROUTER_API_KEY}" ]]; then
  echo "Notice: OPENROUTER_API_KEY is not set. OpenRouter integration will be disabled. Processing will be privacy-friendly and offline."
else
  echo "OpenRouter integration enabled for hybrid local/cloud routing via LiteLLM."
fi

echo "Building job-discovery-local-llm container..."
# The Dockerfile should use 'uv' for python packaging.
docker build -t job-discovery-local-llm -f Dockerfile.local-llm .

echo "Starting container with NVIDIA GPU acceleration (--gpus all)..."
# Assuming NVIDIA GPU is available
docker run -d --name job-discovery-local-llm \
  --gpus all \
  --restart unless-stopped \
  -p 4000:4000 \
  -p 8080:8080 \
  -e OPENROUTER_API_KEY="${OPENROUTER_API_KEY}" \
  -e LOCAL_MODEL="openai/gpt-oss-120b" \
  -e KV_CACHE_REUSE="true" \
  job-discovery-local-llm

echo "Local LLM server started successfully."
