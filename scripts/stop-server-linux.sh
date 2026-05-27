#!/usr/bin/env bash
# stop-server-linux.sh

set -e

echo "Stopping Local LLM Server (Linux)..."

if docker ps -a --format '{{.Names}}' | grep -q "^job-discovery-local-llm$"; then
  docker stop job-discovery-local-llm
  docker rm job-discovery-local-llm
  echo "Local LLM server stopped and removed."
else
  echo "Local LLM server is not running."
fi
