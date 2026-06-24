import subprocess
import time
import urllib.request

# 检查 5173 端口
print("=== 检查 5173 端口 ===")
result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
for line in result.stdout.split('\n'):
    if '5173' in line:
        print(f"  {line.strip()}")

# 检查 8002 端口
print("\n=== 检查 8002 端口 ===")
for line in result.stdout.split('\n'):
    if '8002' in line:
        print(f"  {line.strip()}")

# 测试 HTTP 连接
print("\n=== HTTP 测试 ===")
for url in ['http://127.0.0.1:5173/', 'http://127.0.0.1:8002/api/health']:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode()
            print(f"  {url}: 状态={response.status}, 内容前200字符={content[:200]}")
    except Exception as e:
        print(f"  {url}: 错误={e}")