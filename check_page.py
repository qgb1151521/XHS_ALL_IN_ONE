import urllib.request
try:
    req = urllib.request.Request('http://127.0.0.1:5173/')
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode()
        print(f"状态: {response.status}")
        print(f"内容前500字符:")
        print(content[:500])
except Exception as e:
    print(f"错误: {e}")