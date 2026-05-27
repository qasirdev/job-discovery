#!/usr/bin/env bash
# scripts/stop-server-mac.sh
# Stops the Local LLM container on Mac

set -e

CONTAINER_NAME="job-discovery-local-llm"

echo "🛑 Stopping Local LLM server..."

if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    docker stop "${CONTAINER_NAME}"
    echo "✅ Container stopped."
else
    echo "⚠️ Container ${CONTAINER_NAME} is not running."
fi

if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🧹 Removing container instance..."
    docker rm "${CONTAINER_NAME}"
    echo "✅ Container removed."
fi

echo "Graceful shutdown complete."
