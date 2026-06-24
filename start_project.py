import subprocess
import sys
import time
import os

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
                subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)


print("[1] Cleaning occupied ports...")
kill_port(BACKEND_PORT)
kill_port(FRONTEND_PORT)
time.sleep(2)

print("[2] Starting backend...")
backend_cmd = [sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--host', '0.0.0.0', '--port', str(BACKEND_PORT)]
backend_proc = subprocess.Popen(
    backend_cmd, cwd=PROJECT_ROOT,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
print(f"  Backend PID: {backend_proc.pid}")

print("[3] Waiting for backend...")
time.sleep(10)

print("[4] Starting frontend...")
frontend_dir = os.path.join(PROJECT_ROOT, 'frontend')
node_exe = r"C:\Users\Timor\.workbuddy\binaries\node\versions\22.22.2\node.exe"
vite_exe = os.path.join(frontend_dir, 'node_modules', 'vite', 'bin', 'vite.js')
frontend_cmd = [node_exe, vite_exe, '--host', '127.0.0.1', '--port', str(FRONTEND_PORT)]
frontend_proc = subprocess.Popen(
    frontend_cmd, cwd=frontend_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
print(f"  Frontend PID: {frontend_proc.pid}")

print("\n" + "=" * 50)
print("Services launched!")
print("=" * 50)
print(f"\nFrontend: http://127.0.0.1:{FRONTEND_PORT}")
print(f"Backend:  http://127.0.0.1:{BACKEND_PORT}")
print(f"\nLogin: admin / admin123")
print("\nTwo console windows are running.")
print("Close them to stop services.")