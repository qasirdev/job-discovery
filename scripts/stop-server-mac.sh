#!/bin/bash
# Stop script for Mac local LLM

docker stop local-llm >/dev/null 2>&1
docker rm local-llm >/dev/null 2>&1
echo "Local LLM container stopped."
