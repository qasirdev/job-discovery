@echo off
REM Stop script for PC local LLM

docker stop local-llm >nul 2>&1
docker rm local-llm >nul 2>&1
echo Local LLM container stopped.
