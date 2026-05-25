@echo off
REM Stop script for PC local LLM

taskkill /F /IM llama-server.exe >nul 2>&1
echo llama-server stopped.

docker stop litellm-proxy >nul 2>&1
docker rm litellm-proxy >nul 2>&1
echo LiteLLM proxy stopped.
