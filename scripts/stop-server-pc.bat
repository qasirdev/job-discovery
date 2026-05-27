@echo off
REM stop-server-pc.bat

echo Stopping Local LLM Server (PC)...

docker ps -a --format "{{.Names}}" | findstr /R "^job-discovery-local-llm$" >nul
if %errorlevel%==0 (
  docker stop job-discovery-local-llm
  docker rm job-discovery-local-llm
  echo Local LLM server stopped and removed.
) else (
  echo Local LLM server is not running.
)
