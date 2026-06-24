import subprocess
import sys
import time
import os

print("="*60)
print("启动项目服务")
print("="*60)

# 停止所有相关进程
print("\n[1/4] 停止现有进程...")
subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], capture_output=True)
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
time.sleep(2)

# 启动后端服务
print("\n[2/4] 启动后端服务...")
backend_proc = subprocess.Popen(
    [sys.executable, 'main.py', '--host', '0.0.0.0', '--port', '8002'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"后端服务 PID: {backend_proc.pid}")

# 等待后端启动
print("等待后端启动...")
for i in range(15):
    time.sleep(1)
    try:
        import urllib.request
        req = urllib.request.Request('http://127.0.0.1:8002/api/health')
        with urllib.request.urlopen(req, timeout=2) as response:
            print("✅ 后端服务启动成功!")
            break
    except:
        if i == 14:
            print("❌ 后端服务启动失败")
            sys.exit(1)

# 启动前端服务
print("\n[3/4] 启动前端服务...")
node_path = "C:\\Users\\Timor\\.workbuddy\\binaries\\node\\versions\\22.22.2\\node.exe"
vite_path = os.path.abspath("frontend/node_modules/vite/bin/vite.js")
frontend_proc = subprocess.Popen(
    [node_path, vite_path, "--host", "0.0.0.0", "--port", "5173", "--strictPort"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"前端服务 PID: {frontend_proc.pid}")

# 等待前端启动
print("等待前端启动...")
for i in range(15):
    time.sleep(1)
    try:
        import urllib.request
        req = urllib.request.Request('http://127.0.0.1:5173/')
        with urllib.request.urlopen(req, timeout=2) as response:
            content = response.read().decode()
            if '<html' in content.lower():
                print("✅ 前端服务启动成功!")
                break
    except:
        if i == 14:
            print("❌ 前端服务启动失败")
            sys.exit(1)

# 输出结果
print("\n" + "="*60)
print("服务启动完成!")
print("="*60)
print(f"\n后端服务: http://127.0.0.1:8002")
print(f"前端页面: http://127.0.0.1:5173")
print(f"\n请在浏览器新标签页中访问: http://127.0.0.1:5173")
print("登录账号: admin")
print("登录密码: admin123")
print("\n" + "="*60)