#!/bin/bash
# Local LLM Runtime support script for Linux
# JD-98: Implement llama.cpp-compatible runtime support with GGUF quantized models

MODEL_DIR="./models"
MODEL_NAME="gpt-oss-120b-q4_k_m.gguf"
PORT=8080

echo "Starting AI-Powered Job Discovery Platform Local LLM on Linux..."

if [ -n "$OPENROUTER_API_KEY" ]; then
    echo "OPENROUTER_API_KEY is configured. Using OpenRouter integration via LiteLLM."
    docker run -d --name litellm-proxy -p $PORT:4000 -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY ghcr.io/berriai/litellm:main-latest --model openrouter/auto
    echo "OpenRouter integration started on port $PORT"
    exit 0
fi

echo "Initializing llama.cpp-compatible runtime support with GGUF quantized models..."

mkdir -p $MODEL_DIR

if [ ! -f "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "Model $MODEL_NAME not found. Please download it to $MODEL_DIR/$MODEL_NAME"
fi

if command -v llama-server >/dev/null 2>&1; then
    echo "Starting llama-server with GPU acceleration (CUDA/ROCm) and KV cache reuse..."
    llama-server -m $MODEL_DIR/$MODEL_NAME --port $PORT --ctx-size 4096 -ngl 99 > llama-server.log 2>&1 &
    echo $! > llama-server.pid
    echo "llama-server started on port $PORT (PID: $(cat llama-server.pid))"
    echo "OpenAI-compatible local inference API available at http://localhost:$PORT/v1"
else
    echo "Error: llama-server not found. Please install llama.cpp."
    exit 1
fi
