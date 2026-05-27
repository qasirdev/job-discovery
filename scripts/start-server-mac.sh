#!/usr/bin/env bash
# scripts/start-server-mac.sh
# Local LLM Runtime support script for Mac
# Features: llama.cpp GGUF models (openai/gpt-oss-120b), Metal GPU acceleration, KV cache reuse
# Hybrid routing via LiteLLM, OpenRouter integration.
# Python dependencies managed by 'uv' inside the container.

set -e

# ==========================================
# Configuration & Environment
# ==========================================
CONTAINER_NAME="job-discovery-local-llm"
IMAGE_NAME="job-discovery-local-llm-image"
MODEL_CACHE_DIR="${HOME}/.cache/job-discovery/models"
LITELLM_PORT=4000
BACKEND_PORT=8080

echo "🚀 Starting AI-Powered Job Discovery Platform - Local LLM (Mac)"

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Create persistent model cache directory for offline capability
mkdir -p "${MODEL_CACHE_DIR}"

if [[ -z "${OPENROUTER_API_KEY}" ]]; then
  echo "⚠️  Notice: OPENROUTER_API_KEY is not set."
  echo "   OpenRouter integration will be disabled. Processing will be privacy-friendly and fully offline."
else
  echo "🌐 OpenRouter integration enabled for hybrid local/cloud routing via LiteLLM."
fi

# ==========================================
# Build Phase
# ==========================================
echo "📦 Building ${IMAGE_NAME} container (using 'uv' for python packaging)..."
docker build -t "${IMAGE_NAME}" -f Dockerfile.local-llm .

# ==========================================
# Lifecycle Management
# ==========================================
# Check if container exists and is running
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "🔄 Container is already running. Stopping it first to apply fresh configuration..."
    docker stop "${CONTAINER_NAME}"
fi

# Check if container exists but is stopped
if [ "$(docker ps -aq -f status=exited -f name=${CONTAINER_NAME})" ]; then
    echo "🧹 Removing old container instance..."
    docker rm "${CONTAINER_NAME}"
fi

# ==========================================
# Execution Phase
# ==========================================
echo "⚡ Starting container with Metal GPU optimizations..."
echo "💾 Mounting local model cache at ${MODEL_CACHE_DIR} to support offline workflows..."

# Note: We mount a persistent volume for the models so they aren't re-downloaded
docker run -d --name "${CONTAINER_NAME}" \
  --restart unless-stopped \
  -p ${LITELLM_PORT}:${LITELLM_PORT} \
  -p ${BACKEND_PORT}:${BACKEND_PORT} \
  -v "${MODEL_CACHE_DIR}:/models" \
  -e OPENROUTER_API_KEY="${OPENROUTER_API_KEY}" \
  -e LOCAL_MODEL="openai/gpt-oss-120b" \
  -e KV_CACHE_REUSE="true" \
  -e MODEL_DIR="/models" \
  "${IMAGE_NAME}"

echo "✅ Local LLM server started successfully."
echo "🔍 Monitor logs with: docker logs -f ${CONTAINER_NAME}"
echo "🛑 Stop the server with: docker stop ${CONTAINER_NAME}"
