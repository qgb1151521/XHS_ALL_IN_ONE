@echo off
chcp 65001 >nul
title XHS_ALL_IN_ONE 服务管理器

echo ========================================
echo   XHS_ALL_IN_ONE 服务启动
echo ========================================
echo.

REM 清理端口
echo [1/4] 清理占用端口...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8002.*LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173.*LISTENING"') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak >nul

REM 启动后端
echo [2/4] 启动后端服务...
start "后端服务 [8002]" cmd /c "cd /d %~dp0 && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8002"

REM 等待后端启动
echo       等待后端服务启动...
timeout /t 5 /nobreak >nul

REM 检查后端
curl -s http://127.0.0.1:8002/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo       后端服务启动中...
    timeout /t 5 /nobreak >nul
)

REM 启动前端
echo [3/4] 启动前端服务...
start "前端服务 [5173]" cmd /c "cd /d %~dp0frontend && npm run dev"

REM 等待前端启动
echo       等待前端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   服务状态
echo ========================================
echo.

REM 检查服务状态
echo [后端 8002]
netstat -ano | findstr ":8002.*LISTENING" && echo   运行正常! || echo   未运行
echo.
echo [前端 5173]
netstat -ano | findstr ":5173.*LISTENING" && echo   运行正常! || echo   未运行

echo.
echo ========================================
echo   访问地址
echo ========================================
echo.
echo   前端页面: http://127.0.0.1:5173
echo   后端 API:  http://127.0.0.1:8002
echo.
echo   登录账号: admin
echo   登录密码: admin123
echo.
echo ========================================
echo   按任意键退出...
echo ========================================
pause >nul
