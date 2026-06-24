@echo off
cd /d "e:\linewell\program\qgb1151521\XHS_ALL_IN_ONE"

echo 启动后端服务...
start "后端服务" python main.py --host 0.0.0.0 --port 8002

timeout /t 3 /nobreak >nul

echo 启动前端服务...
start "前端服务" "C:\Users\Timor\.workbuddy\binaries\node\versions\22.22.2\node.exe" frontend\node_modules\vite\bin\vite.js --host 0.0.0.0 --port 5173

echo 服务已启动!
echo 前端页面: http://127.0.0.1:5173
echo 后端 API: http://127.0.0.1:8002
timeout /t 3 /nobreak >nul