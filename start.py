import subprocess
import sys
import time
import os
import urllib.request

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_PORT = 8002
FRONTEND_PORT = 5173


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
                try:
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    print(f"  Killed PID {pid} on port {port}")
                except:
                    pass


print("=" * 50)
print("XHS_ALL_IN_ONE One-Click Launcher")
print("=" * 50)

print("\n[1/4] Cleaning occupied ports...")
kill_port(BACKEND_PORT)
kill_port(FRONTEND_PORT)
time.sleep(2)

print("\n[2/4] Starting backend server...")
backend_cmd = [sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--host', '0.0.0.0', '--port', str(BACKEND_PORT)]
backend_proc = subprocess.Popen(
    backend_cmd,
    cwd=PROJECT_ROOT,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print(f"  Backend PID: {backend_proc.pid}")

print("\n[3/4] Waiting for backend to be ready...")
backend_ready = False
for i in range(15):
    time.sleep(1)
    try:
        urllib.request.urlopen(f'http://127.0.0.1:{BACKEND_PORT}/api/health', timeout=2)
        backend_ready = True
        print(f"  Backend ready after {i+1} seconds!")
        break
    except:
        print(f"  Checking {i+1}/15...", end='\r')

if not backend_ready:
    print("  WARNING: Backend timeout, continuing...")

print("\n[4/4] Starting frontend server...")
frontend_dir = os.path.join(PROJECT_ROOT, 'frontend')
node_exe = r"C:\Users\Timor\.workbuddy\binaries\node\versions\22.22.2\node.exe"
vite_exe = os.path.join(frontend_dir, 'node_modules', 'vite', 'bin', 'vite.js')

frontend_cmd = [node_exe, vite_exe, '--host', '127.0.0.1', '--port', str(FRONTEND_PORT)]
frontend_proc = subprocess.Popen(
    frontend_cmd,
    cwd=frontend_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print(f"  Frontend PID: {frontend_proc.pid}")

print("\n" + "=" * 50)
print("Services launched!")
print("=" * 50)
print(f"\nBackend:  http://127.0.0.1:{BACKEND_PORT}")
print(f"Frontend: http://127.0.0.1:{FRONTEND_PORT}")
print(f"\nLogin: admin / admin123")
print("\nTwo console windows are running.")
print("Close them to stop services.")
print("\nPress Enter to open browser...")
input()

import webbrowser
webbrowser.open(f'http://127.0.0.1:{FRONTEND_PORT}')