import subprocess
import sys
import time
import os

current_pid = os.getpid()
print(f"当前进程 PID: {current_pid}")

print("\n[1/3] 停止现有 node 进程...")
subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], capture_output=True)

# 只停止其他 Python 进程
print("[2/3] 停止其他 Python 进程...")
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'], capture_output=True, text=True)
for line in result.stdout.strip().split('\n')[1:]:
    parts = line.strip().strip('"').split('","')
    if len(parts) >= 2:
        try:
            pid = int(parts[1])
            if pid != current_pid:
                print(f"  停止 PID {pid}")
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
        except ValueError:
            pass
time.sleep(2)

# 启动后端服务
print("\n[3/3] 启动后端服务...")
backend_proc = subprocess.Popen(
    [sys.executable, 'main.py', '--host', '0.0.0.0', '--port', '8002'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"后端服务 PID: {backend_proc.pid}")

time.sleep(3)

# 启动前端服务
print("\n启动前端服务...")
node_path = "C:\\Users\\Timor\\.workbuddy\\binaries\\node\\versions\\22.22.2\\node.exe"
vite_path = os.path.abspath("frontend/node_modules/vite/bin/vite.js")
frontend_proc = subprocess.Popen(
    [node_path, vite_path, "--host", "0.0.0.0", "--port", "5173", "--strictPort"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"前端服务 PID: {frontend_proc.pid}")

print("\n服务启动中，请等待 10 秒后访问...")
print("前端页面: http://127.0.0.1:5173")
print("后端 API: http://127.0.0.1:8002")