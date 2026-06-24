import subprocess
import sys
import time
import os

current_pid = os.getpid()
print(f"当前进程 PID: {current_pid}")

# 1. 停止所有相关进程（排除当前进程）
print("停止现有进程...")
subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], capture_output=True)

result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'], capture_output=True, text=True)
for line in result.stdout.strip().split('\n')[1:]:
    parts = line.strip().strip('"').split('","')
    if len(parts) >= 2:
        try:
            pid = int(parts[1])
            if pid != current_pid:
                print(f"停止 Python 进程: {pid}")
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
        except ValueError:
            pass
time.sleep(2)

# 2. 启动后端服务
print("\n启动后端服务...")
backend_proc = subprocess.Popen(
    [sys.executable, 'main.py', '--host', '0.0.0.0', '--port', '8002'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"后端服务 PID: {backend_proc.pid}")

# 3. 等待后端启动
for i in range(10):
    time.sleep(1)
    try:
        import urllib.request
        req = urllib.request.Request('http://127.0.0.1:8002/api/health')
        with urllib.request.urlopen(req, timeout=2) as response:
            print("后端服务启动成功!")
            break
    except:
        if i == 9:
            print("后端服务启动失败")
            sys.exit(1)

# 4. 启动前端服务
print("\n启动前端服务...")
node_path = "C:\\Users\\Timor\\.workbuddy\\binaries\\node\\versions\\22.22.2\\node.exe"
vite_path = os.path.abspath("frontend/node_modules/vite/bin/vite.js")
frontend_proc = subprocess.Popen(
    [node_path, vite_path, "--host", "127.0.0.1", "--port", "5173", "--strictPort"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"前端服务 PID: {frontend_proc.pid}")

# 5. 等待前端启动
for i in range(10):
    time.sleep(1)
    try:
        import urllib.request
        req = urllib.request.Request('http://127.0.0.1:5173/')
        with urllib.request.urlopen(req, timeout=2) as response:
            print("前端服务启动成功!")
            break
    except:
        if i == 9:
            print("前端服务启动失败")
            sys.exit(1)

print("\n" + "="*50)
print("服务已启动！")
print("后端 API: http://127.0.0.1:8002")
print("前端页面: http://127.0.0.1:5173")
print("="*50)
print("\n请在浏览器中独立打开 http://127.0.0.1:5173")
print("不要在 IDE 内嵌预览或 Chrome 错误页面中打开")
print("否则会触发浏览器安全限制")