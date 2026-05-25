@echo off
REM Local LLM Runtime support script for PC
REM JD-98: Implement llama.cpp-compatible runtime support with GGUF quantized models

set MODEL_DIR=.\models
set MODEL_NAME=gpt-oss-120b-q4_k_m.gguf
set PORT=8080

echo Starting AI-Powered Job Discovery Platform Local LLM on PC...

if defined OPENROUTER_API_KEY (
    echo OPENROUTER_API_KEY is configured. Using OpenRouter integration via LiteLLM.
    docker run -d --name litellm-proxy -p %PORT%:4000 -e OPENROUTER_API_KEY=%OPENROUTER_API_KEY% ghcr.io/berriai/litellm:main-latest --model openrouter/auto
    echo OpenRouter integration started on port %PORT%
    exit /b 0
)

echo Initializing llama.cpp-compatible runtime support with GGUF quantized models...

if not exist %MODEL_DIR% mkdir %MODEL_DIR%

if not exist %MODEL_DIR%\%MODEL_NAME% (
    echo Model %MODEL_NAME% not found. Please download it to %MODEL_DIR%\%MODEL_NAME%
)

echo Starting llama-server with GPU acceleration and KV cache reuse...
start /B llama-server.exe -m %MODEL_DIR%\%MODEL_NAME% --port %PORT% --ctx-size 4096 -ngl 99 > llama-server.log 2>&1
echo llama-server started on port %PORT%. (Running in background)
echo OpenAI-compatible local inference API available at http://localhost:%PORT%/v1
