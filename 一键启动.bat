@echo off
title XHS_ALL_IN_ONE Launcher

set "PROJECT_ROOT=%~dp0"
set "BACKEND_PORT=8002"
set "FRONTEND_PORT=5173"

echo Step 1: Kill old processes
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo Step 2: Start backend
cd /d "%PROJECT_ROOT%"
start cmd /k "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port %BACKEND_PORT%"

echo Step 3: Wait for backend
timeout /t 8 /nobreak >nul

echo Step 4: Start frontend
cd /d "%PROJECT_ROOT%frontend"
start cmd /k "npm run dev"

echo Step 5: Done
echo Frontend: http://127.0.0.1:%FRONTEND_PORT%
echo Backend: http://127.0.0.1:%BACKEND_PORT%
timeout /t 3 /nobreak >nul