import json
import requests
from apis.xhs_pc_login_apis import XHSLoginApi
from xhs_utils.xhs_util import generate_headers, splice_str

# 测试二维码登录流程
api = XHSLoginApi()

print("[1/3] 生成初始 cookies...")
cookies = api.generate_init_cookies()
print(f"a1: {cookies.get('a1')}")

print("\n[2/3] 生成二维码...")
success, msg, qr_data = api.generate_qrcode(cookies)
if not success:
    print(f"生成二维码失败: {msg}")
    exit(1)

cookies = qr_data['cookies']
qr_id = qr_data['qr_id']
code = qr_data['code']
qr_url = qr_data['qr_url']

print(f"qr_id: {qr_id}")
print(f"code: {code}")
print(f"qr_url: {qr_url}")

print("\n[3/3] 检查二维码状态（请扫码后查看）...")
print("请在手机上扫描二维码并确认登录...")

# 模拟轮询
import time
for i in range(30):
    success, msg, updated_cookies = api.check_qrcode_status(qr_id, code, cookies)
    print(f"第 {i+1} 次检查: success={success}, msg={msg}")
    
    if success:
        print("登录成功！")
        print(f"cookies: {json.dumps(updated_cookies, indent=2)}")
        
        # 测试获取用户信息
        print("\n尝试获取用户信息...")
        info_success, user_info, final_cookies = api.get_user_info(updated_cookies)
        print(f"获取用户信息: success={info_success}")
        print(f"user_info: {json.dumps(user_info, indent=2, ensure_ascii=False)}")
        break
    
    if "过期" in msg:
        print("二维码已过期")
        break
    
    time.sleep(2)
else:
    print("轮询超时")