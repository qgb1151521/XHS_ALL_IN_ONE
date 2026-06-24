import subprocess
import sys
import time
import os

# 停止已有的 Python 进程（除了当前进程）
current_pid = os.getpid()
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'], capture_output=True, text=True)
for line in result.stdout.strip().split('\n')[1:]:
    parts = line.strip().strip('"').split('","')
    if len(parts) >= 2:
        try:
            pid = int(parts[1])
            if pid != current_pid:
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
                time.sleep(0.5)
        except ValueError:
            pass

# 启动后端服务
print("启动后端服务...")
proc = subprocess.Popen(
    [sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--host', '0.0.0.0', '--port', '8002'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print(f"后端服务启动中，PID: {proc.pid}")

# 等待服务启动
for i in range(15):
    time.sleep(1)
    try:
        import urllib.request
        req = urllib.request.Request('http://127.0.0.1:8002/api/health')
        with urllib.request.urlopen(req, timeout=2) as response:
            print("后端服务启动成功!")
            break
    except:
        if i == 14:
            print("后端服务启动失败")
            sys.exit(1)