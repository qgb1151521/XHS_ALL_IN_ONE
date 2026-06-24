@echo off
title XHS_ALL_IN_ONE Launcher

set "PROJECT_ROOT=%~dp0"

echo Step 1: Kill existing processes
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo Step 2: Start backend
cd /d "%PROJECT_ROOT%"
start cmd /c "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8002"

echo Step 3: Wait for backend
timeout /t 8 /nobreak >nul

echo Step 4: Start frontend
cd /d "%PROJECT_ROOT%frontend"
start cmd /c "npm run dev"

echo Step 5: Done
echo Frontend: http://127.0.0.1:5173
echo Backend: http://127.0.0.1:8002
timeout /t 3 /nobreak >nul