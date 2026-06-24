import urllib.request
import sys

try:
    req = urllib.request.Request('http://127.0.0.1:5173/')
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode()
        sys.stdout.write(f"状态: {response.status}\n")
        sys.stdout.write(f"内容:\n{content[:500]}\n")
        sys.stdout.flush()
except Exception as e:
    sys.stdout.write(f"错误: {e}\n")
    sys.stdout.flush()