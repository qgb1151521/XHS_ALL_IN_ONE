import urllib.request
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxNTg0NTQwfQ.2Uhlf8peBKyYvVGwT6tCEOXZZXP86ymip5Py_TjqmGc"

session_id = input("请输入 Session ID: ")

req = urllib.request.Request(
    f'http://127.0.0.1:8002/api/xhs/login-sessions/{session_id}',
    headers={'Authorization': f'Bearer {token}'}
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
        print(f"状态: {data['status']}")
        print(f"完整响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"错误: {e}")