@echo off
setlocal

set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend"
set "FRONTEND=%ROOT%frontend"
set "BACKEND_URL=http://localhost:8001/api"

set "PYTHON_EXE="
where python >nul 2>nul
if %errorlevel%==0 set "PYTHON_EXE=python"

if "%PYTHON_EXE%"=="" (
  if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    set "PYTHON_EXE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
  )
)

if "%PYTHON_EXE%"=="" (
  echo Python was not found. Install Python 3.11+ or run from Codex with the bundled runtime.
  pause
  exit /b 1
)

where npm.cmd >nul 2>nul
if not %errorlevel%==0 (
  echo npm.cmd was not found. Install Node.js 18+ and run npm install inside frontend.
  pause
  exit /b 1
)

echo Starting API Documentation Generator backend on http://localhost:8001
start "API Docs Backend" cmd /k "cd /d ""%BACKEND%"" && ""%PYTHON_EXE%"" run_dev_server.py"

echo Starting frontend on http://localhost:3001
start "API Docs Frontend" cmd /k "cd /d ""%FRONTEND%"" && set NEXT_PUBLIC_API_URL=%BACKEND_URL%&& npm.cmd run dev -- -p 3001"

echo.
echo Open the app: http://localhost:3001
echo Backend docs: http://localhost:8001/docs
echo Health check: http://localhost:8001/health
echo.
pause
