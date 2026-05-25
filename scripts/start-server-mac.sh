#!/bin/bash
# Local LLM Runtime support script for Mac
# JD-98: Implement llama.cpp-compatible runtime support with GGUF quantized models packaged via Docker & uv

MODEL_DIR="$(pwd)/models"
MODEL_NAME="gpt-oss-120b-q4_k_m.gguf"
PORT=8080

echo "Starting AI-Powered Job Discovery Platform Local LLM on Mac via Docker..."

mkdir -p $MODEL_DIR

if [ ! -f "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "Model $MODEL_NAME not found."
    echo "Please download the GGUF model manually to $MODEL_DIR/$MODEL_NAME"
fi

# Build the local LLM container (which uses uv for python deps)
docker build -t job-discovery-local-llm -f infrastructure/Dockerfile.local-llm .

if [ -n "$OPENROUTER_API_KEY" ]; then
    echo "OPENROUTER_API_KEY is configured. Using OpenRouter integration via LiteLLM."
    docker run -d --name local-llm -p 4000:4000 -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY job-discovery-local-llm
    echo "OpenRouter integration started on port 4000"
else
    echo "Starting llama-server with GPU acceleration and KV cache reuse..."
    docker run -d --name local-llm -p $PORT:8080 -v $MODEL_DIR:/models job-discovery-local-llm
    echo "llama-server started on port $PORT"
    echo "OpenAI-compatible local inference API available at http://localhost:$PORT/v1"
fi
