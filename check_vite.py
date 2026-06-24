import subprocess
import time
import os
import urllib.request
import sys

# 1. 停止所有 node 进程
print("停止所有 node 进程...")
subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], capture_output=True)
time.sleep(2)

# 2. 启动前端服务
print("\n启动前端服务...")
node_path = "C:\\Users\\Timor\\.workbuddy\\binaries\\node\\versions\\22.22.2\\node.exe"
vite_path = os.path.abspath("frontend/node_modules/vite/bin/vite.js")
print(f"Vite 路径: {vite_path}")
print(f"Vite 是否存在: {os.path.exists(vite_path)}")

proc = subprocess.Popen(
    [node_path, vite_path, "--host", "127.0.0.1", "--port", "5173", "--strictPort"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"前端服务已启动，PID: {proc.pid}")

# 3. 等待服务启动
for i in range(15):
    time.sleep(1)
    try:
        req = urllib.request.Request('http://127.0.0.1:5173/')
        with urllib.request.urlopen(req, timeout=2) as response:
            content = response.read().decode()
            print(f"\n✅ 前端服务已启动！状态: {response.status}")
            print(f"页面内容（前200字符）: {content[:200]}")
            break
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"等待中... 端口已开启但返回 404 ({i+1}/15)")
        else:
            print(f"等待中... 错误: {e} ({i+1}/15)")
    except Exception as e:
        print(f"等待中... {e} ({i+1}/15)")
else:
    print("\n❌ 前端服务启动失败")
    sys.exit(1)