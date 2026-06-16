import urllib.request
import json
import time

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxNTg0NTQwfQ.2Uhlf8peBKyYvVGwT6tCEOXZZXP86ymip5Py_TjqmGc"

# 首先获取最新的二维码 session
print("获取最新的二维码 session...")
try:
    req = urllib.request.Request(
        'http://127.0.0.1:8002/api/xhs/login-sessions/pc/qrcode',
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST',
        data=b'{}'
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
        session_id = data['session_id']
        print(f"Session ID: {session_id}")
        print(f"QR URL: {data['qr_url']}")
        
        print("\n请在手机上扫描二维码并确认登录...")
        print("等待 10 秒后开始检查状态...")
        time.sleep(10)
        
        # 检查状态
        print("\n检查登录状态...")
        req2 = urllib.request.Request(
            f'http://127.0.0.1:8002/api/xhs/login-sessions/{session_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        with urllib.request.urlopen(req2, timeout=10) as response2:
            data2 = json.loads(response2.read().decode())
            print(f"状态: {data2['status']}")
            print(f"完整响应: {json.dumps(data2, indent=2, ensure_ascii=False)}")
            
            if data2['status'] == 'confirmed':
                print("\n登录成功！")
                if data2.get('account'):
                    print(f"账号信息: {json.dumps(data2['account'], indent=2, ensure_ascii=False)}")
                else:
                    print("但未返回账号信息，可能获取用户信息失败")
            elif data2['status'] == 'scanned':
                print("\n已扫码，等待确认...")
            elif data2['status'] == 'pending':
                print("\n等待扫码...")
            elif data2['status'] == 'expired':
                print("\n二维码已过期")
            else:
                print(f"\n未知状态: {data2['status']}")
                
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()