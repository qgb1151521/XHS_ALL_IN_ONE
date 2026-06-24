import urllib.request
import time

time.sleep(5)

try:
    req = urllib.request.Request('http://127.0.0.1:5173/')
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode()
        print(f"前端服务状态: {response.status}")
        print(f"内容前300字符: {content[:300]}")
        print("\n✅ 前端服务运行正常!")
        print("请在浏览器新标签页中访问: http://127.0.0.1:5173")
except Exception as e:
    print(f"前端服务错误: {e}")

try:
    req = urllib.request.Request('http://127.0.0.1:8002/api/health')
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode()
        print(f"\n后端服务状态: {response.status}")
        print(f"响应: {content}")
        print("\n✅ 后端服务运行正常!")
except Exception as e:
    print(f"\n后端服务错误: {e}")