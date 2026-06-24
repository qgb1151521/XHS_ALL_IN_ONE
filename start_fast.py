import subprocess
import sys
import os

print("启动后端服务...")
backend_proc = subprocess.Popen(
    [sys.executable, 'main.py', '--host', '0.0.0.0', '--port', '8002'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"后端服务 PID: {backend_proc.pid}")

print("\n启动前端服务...")
node_path = "C:\\Users\\Timor\\.workbuddy\\binaries\\node\\versions\\22.22.2\\node.exe"
vite_path = os.path.abspath("frontend/node_modules/vite/bin/vite.js")
frontend_proc = subprocess.Popen(
    [node_path, vite_path, "--host", "0.0.0.0", "--port", "5173"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"前端服务 PID: {frontend_proc.pid}")

print("\n服务已启动，请等待 10 秒后访问:")
print("前端页面: http://127.0.0.1:5173")
print("后端 API: http://127.0.0.1:8002")