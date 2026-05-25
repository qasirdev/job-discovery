#!/bin/bash
# Local LLM Runtime support script for Mac

echo "Starting AI-Powered Job Discovery Platform on Mac..."
echo "Initializing local LLM runtime support..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
fi

docker-compose up -d --build
echo "Platform started. Dashboard accessible at http://localhost"
