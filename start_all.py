import subprocess
import sys
import time
import os

# 清理占用端口的进程
def kill_port(port):
    result = subprocess.run(f'netstat -ano | findstr ":{port}"', shell=True, capture_output=True, text=True)
    for line in result.stdout.strip().split('\n'):
        if 'LISTENING' in line:
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1]
                try:
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    print(f"已终止进程 PID: {pid}")
                except:
                    pass

print("="*50)
print("清理占用端口...")
kill_port(8002)
kill_port(5173)
time.sleep(1)

# 启动后端
print("\n启动后端服务...")
backend_proc = subprocess.Popen(
    [sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--host', '0.0.0.0', '--port', '8002'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print(f"后端服务 PID: {backend_proc.pid}")

# 等待后端启动
backend_ready = False
for i in range(15):
    time.sleep(1)
    try:
        import urllib.request
        urllib.request.urlopen('http://127.0.0.1:8002/api/health', timeout=2)
        backend_ready = True
        print("后端服务启动成功!")
        break
    except:
        pass

if not backend_ready:
    print("后端服务启动失败!")
    sys.exit(1)

# 启动前端
print("\n启动前端服务...")
node_exe = r"C:\Users\Timor\.workbuddy\binaries\node\versions\22.22.2\node.exe"
vite_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "node_modules", "vite", "bin", "vite.js")

frontend_proc = subprocess.Popen(
    [node_exe, vite_exe, '--host', '127.0.0.1', '--port', '5173'],
    cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend"),
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print(f"前端服务 PID: {frontend_proc.pid}")

# 等待前端启动
time.sleep(5)

print("\n" + "="*50)
print("所有服务已启动!")
print("="*50)
print(f"前端页面: http://127.0.0.1:5173")
print(f"后端 API: http://127.0.0.1:8002")
print(f"\n后端 PID: {backend_proc.pid}")
print(f"前端 PID: {frontend_proc.pid}")
print("="*50)

# 保持运行
print("\n按 Ctrl+C 停止所有服务...")
try:
    backend_proc.wait()
except:
    pass