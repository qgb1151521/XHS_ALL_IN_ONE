import urllib.request
import json

print("="*50)
print("服务状态测试")
print("="*50)

# 测试前端
print("\n[1/2] 测试前端服务 (http://127.0.0.1:5173)")
try:
    req = urllib.request.Request('http://127.0.0.1:5173/')
    with urllib.request.urlopen(req, timeout=5) as response:
        content = response.read().decode()
        print(f"  ✅ 状态码: {response.status}")
        print(f"  ✅ 内容包含 HTML: {'<html' in content.lower()}")
        print(f"  ✅ 内容长度: {len(content)} 字符")
except Exception as e:
    print(f"  ❌ 错误: {e}")

# 测试后端
print("\n[2/2] 测试后端服务 (http://127.0.0.1:8002)")
try:
    req = urllib.request.Request('http://127.0.0.1:8002/api/health')
    with urllib.request.urlopen(req, timeout=5) as response:
        content = response.read().decode()
        print(f"  ✅ 状态码: {response.status}")
        print(f"  ✅ 响应: {content}")
except Exception as e:
    print(f"  ❌ 错误: {e}")

print("\n" + "="*50)