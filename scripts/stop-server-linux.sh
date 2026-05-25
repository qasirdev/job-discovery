#!/bin/bash
# Stop script for Linux local LLM

if [ -f "llama-server.pid" ]; then
    kill $(cat llama-server.pid)
    rm llama-server.pid
    echo "llama-server stopped."
else
    echo "llama-server PID file not found."
fi

if docker ps -q -f name=litellm-proxy >/dev/null 2>&1; then
    docker stop litellm-proxy
    docker rm litellm-proxy
    echo "LiteLLM proxy stopped."
fi
