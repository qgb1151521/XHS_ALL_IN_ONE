import urllib.request
import json

print("="*50)
print("测试前端页面")
print("="*50)

# 测试前端
print("\n[1/2] 测试前端服务 (http://127.0.0.1:5173)")
try:
    req = urllib.request.Request('http://127.0.0.1:5173/')
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode()
        has_root = '<div id="root"' in content
        has_main = 'main.tsx' in content
        print(f"状态码: {response.status}")
        print(f"内容长度: {len(content)} 字符")
        print(f"内容前500字符:")
        print(content[:500])
        print(f"\n是否包含 'root' div: {has_root}")
        print(f"是否包含 'main.tsx': {has_main}")
except Exception as e:
    print(f"错误: {e}")

# 测试后端
print("\n[2/2] 测试后端服务 (http://127.0.0.1:8002)")
try:
    req = urllib.request.Request('http://127.0.0.1:8002/api/health')
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode()
        print(f"状态码: {response.status}")
        print(f"响应: {content}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "="*50)