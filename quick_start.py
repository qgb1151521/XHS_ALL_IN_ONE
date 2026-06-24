import subprocess
import sys
import time
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def kill_port(port):
    result = subprocess.run(
        f'netstat -ano | findstr ":{port}.*LISTENING"',
        shell=True, capture_output=True, text=True
    )
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1]
                subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                print(f"Killed PID {pid} on port {port}")


print("[1] Cleaning occupied ports...")
kill_port(8002)
kill_port(5173)
time.sleep(2)

print("[2] Starting backend...")
backend_cmd = [sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--host', '0.0.0.0', '--port', '8002']
subprocess.Popen(backend_cmd, cwd=PROJECT_ROOT)

print("[3] Waiting for backend...")
time.sleep(10)

print("[4] Starting frontend...")
frontend_dir = os.path.join(PROJECT_ROOT, 'frontend')
node_exe = r"C:\Users\Timor\.workbuddy\binaries\node\versions\22.22.2\node.exe"
vite_exe = os.path.join(frontend_dir, 'node_modules', 'vite', 'bin', 'vite.js')
subprocess.Popen([node_exe, vite_exe, '--host', '127.0.0.1', '--port', '5173'], cwd=frontend_dir)

print("\nServices started!")
print("Frontend: http://127.0.0.1:5173")
print("Backend: http://127.0.0.1:8002")