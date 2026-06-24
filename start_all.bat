@echo off
cd /d "e:\linewell\program\qgb1151521\XHS_ALL_IN_ONE"

echo 停止现有进程...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo 启动后端服务...
start "后端服务" python main.py --host 0.0.0.0 --port 8002

echo 等待后端启动...
timeout /t 5 /nobreak >nul

echo 启动前端服务...
start "前端服务" "C:\Users\Timor\.workbuddy\binaries\node\versions\22.22.2\node.exe" frontend\node_modules\vite\bin\vite.js --host 127.0.0.1 --port 5173 --strictPort

echo 服务启动中...
echo 请在浏览器中访问: http://127.0.0.1:5173
timeout /t 5 /nobreak >nul