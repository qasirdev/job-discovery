@echo off
REM Local LLM Runtime support script for PC

echo Starting AI-Powered Job Discovery Platform on PC...
echo Initializing local LLM runtime support...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running. Please start Docker and try again.
    exit /b 1
)

docker-compose up -d --build
echo Platform started. Dashboard accessible at http://localhost
