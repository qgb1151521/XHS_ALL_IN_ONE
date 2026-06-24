import json
import time
import random
import uuid

import requests
import qrcode
from loguru import logger

from apis.xhs_pc_apis import XHS_Apis
from xhs_utils.http_util import REQUEST_TIMEOUT
from xhs_utils.xhs_util import generate_headers, generate_xs_xs_common, splice_str
from xhs_utils.common_util import generate_a1, generate_web_id


class XHSLoginApi:
    def __init__(self):
        self.base_url = "https://edith.xiaohongshu.com"
        self.as_url = "https://as.xiaohongshu.com"
        self.home_url = 'https://www.xiaohongshu.com/explore'

    @staticmethod
    def _get_sec_headers():
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'origin': 'https://www.xiaohongshu.com',
            'referer': 'https://www.xiaohongshu.com/',
        }

    def _fetch_sec_cookies(self, cookies):
        api = '/api/sec/v1/scripting'
        data = {"callFrom": "web", "callback": "", "type": "ds", "appId": "xhs-pc-web"}

        xs, xt, xs_common = generate_xs_xs_common(cookies['a1'], api, data)
        headers = self._get_sec_headers()
        headers['x-s'] = xs
        headers['x-t'] = str(xt)
        headers['x-s-common'] = xs_common

        data_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        try:
            resp = requests.post(
                self.as_url + api,
                headers=headers, cookies=cookies,
                data=data_str.encode('utf-8'),
                timeout=REQUEST_TIMEOUT
            )
            res = resp.json()
            return res.get('data', {}).get('secPoisonId')
        except Exception as e:
            logger.debug(f'fetch sec_poison_id failed: {e}')
            return None

    def _fetch_gid(self, cookies):
        api = '/api/sec/v1/shield/webprofile'
        data = {"platform": "Windows", "sdkVersion": "4.3.5", "svn": "2", "profileData": ""}

        xs, xt, xs_common = generate_xs_xs_common(cookies['a1'], api, data)
        headers = self._get_sec_headers()
        headers['x-s'] = xs
        headers['x-t'] = str(xt)
        headers['x-s-common'] = xs_common

        data_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        try:
            resp = requests.post(
                self.as_url + api,
                headers=headers, cookies=cookies,
                data=data_str.encode('utf-8'),
                timeout=REQUEST_TIMEOUT
            )
            for key, value in resp.cookies.items():
                cookies[key] = value
            return cookies.get('gid')
        except Exception as e:
            logger.debug(f'fetch gid failed: {e}')
            return None

    def generate_init_cookies(self):
        ts = int(time.time() * 1000)
        a1 = generate_a1()
        web_id = generate_web_id(a1)
        cookies = {
            'abRequestId': str(uuid.uuid4()),
            'ets': str(ts),
            'webBuild': '6.7.4',
            'xsecappid': 'xhs-pc-web',
            'loadts': str(ts + random.randint(50, 200)),
            'a1': a1,
            'webId': web_id,
        }

        sec_poison_id = self._fetch_sec_cookies(cookies)
        if sec_poison_id:
            cookies['sec_poison_id'] = sec_poison_id

        gid = self._fetch_gid(cookies)
        if gid:
            cookies['gid'] = gid

        return cookies

    def generate_qrcode(self, cookies):
        api = '/api/sns/web/v1/login/qrcode/create'
        data = {"qr_type": 1}

        headers, data = generate_headers(cookies['a1'], api, data)
        resp = requests.post(
            self.base_url + api,
            headers=headers, cookies=cookies, data=data,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        if not res.get('success'):
            return False, res.get('msg', '未知错误'), None
        data = res.get('data') or {}
        if not all(key in data for key in ('qr_id', 'code', 'url')):
            return False, res.get('msg', '二维码响应缺少必要字段'), {'cookies': cookies, 'res_json': res}

        return True, '成功', {
            'cookies': cookies,
            'qr_id': data['qr_id'],
            'code': data['code'],
            'qr_url': data['url'],
        }

    def check_qrcode_status(self, qr_id, code, cookies):
        """轮询二维码扫码状态 — 使用 /api/sns/web/v1/login/qrcode/status (XHS Web客户端标准轮询端点)"""
        api = '/api/sns/web/v1/login/qrcode/status'
        params = {"qr_id": qr_id, "code": code}
        splice_api = splice_str(api, params)

        headers, _ = generate_headers(cookies['a1'], splice_api, method='GET')
        logger.info(f"_login_by_qrcode_status request: {self.base_url + splice_api}")
        resp = requests.get(
            self.base_url + splice_api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        logger.info(f"_login_by_qrcode_status response status: {resp.status_code}")
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        logger.info(f'[check_qrcode_status] /api/sns/web/v1/login/qrcode/status FULL response: {json.dumps(res, ensure_ascii=False)[:1500]}')
        logger.info(f'[check_qrcode_status] resp.cookies keys={list(resp.cookies.keys())}, items={[(k, str(v)[:50]) for k, v in resp.cookies.items()]}')

        data_field = res.get('data') or {}
        # XHS API返回 code_status (下划线格式)，也兼容 codeStatus (驼峰格式)
        code_status = None
        if isinstance(data_field, dict):
            code_status = data_field.get('code_status', data_field.get('codeStatus'))

        if code_status is None:
            logger.warning(f'[check_qrcode_status] no code_status in response, data_keys={list(data_field.keys()) if isinstance(data_field, dict) else type(data_field)}, FULL: {json.dumps(res, ensure_ascii=False)[:500]}')
            return False, res.get('msg', '二维码状态响应缺少 code_status'), cookies

        # code_status 状态映射: 0=未扫码, 1=已扫码待确认, 2=登录成功, 3=已过期
        status_map = {
            0: (False, '请扫描二维码'),
            1: (False, '请确认登录'),
            2: (True, '验证成功'),
            3: (False, '二维码已过期'),
        }
        success, msg = status_map.get(code_status, (False, f'未知状态: {code_status}'))

        # 登录成功时(code_status==2)，提取 web_session
        if code_status == 2 and isinstance(data_field, dict):
            login_info = data_field.get('login_info')
            if isinstance(login_info, dict):
                # 方式1: secure_session 对应 web_session (XHS标准)
                secure_session = login_info.get('secure_session')
                if secure_session and 'web_session' not in cookies:
                    cookies['web_session'] = secure_session
                    logger.info(f'[check_qrcode_status] got web_session from login_info.secure_session')

                # 方式2: 如果没有 secure_session，尝试用 session 字段
                session_val = login_info.get('session')
                if session_val and 'web_session' not in cookies:
                    cookies['web_session'] = session_val
                    logger.info(f'[check_qrcode_status] got web_session from login_info.session')

                # 提取 user_id
                user_id = login_info.get('user_id')
                if user_id:
                    logger.info(f'[check_qrcode_status] got user_id from login_info: {user_id}')

            # 方式3: 如果还是没有 web_session，检查 response cookies (Set-Cookie header)
            if 'web_session' not in cookies:
                logger.warning(f'[check_qrcode_status] web_session not found in login_info or response cookies. login_info={login_info if isinstance(login_info, dict) else "N/A"}, resp_cookies_keys={list(resp.cookies.keys())}')

        logger.info(f'[check_qrcode_status] final: code_status={code_status}, success={success}, msg={msg!r}, has_web_session={"web_session" in cookies}')
        return success, msg, cookies

    def get_user_info(self, cookies):
        api = '/api/sns/web/v2/user/me'

        headers, _ = generate_headers(cookies['a1'], api)
        resp = requests.get(
            self.base_url + api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        # 小红书API响应可能没有success字段，只有code:0表示成功
        success = res.get('success', False) or res.get('code') == 0
        data = res.get('data') or {}
        logger.info(f'[get_user_info] /api/sns/web/v2/user/me response: code={res.get("code")}, success={res.get("success")}, data_keys={list(data.keys()) if isinstance(data, dict) else type(data)}, has_web_session_in_cookies={"web_session" in cookies}')
        if not success and not data:
            logger.warning(f'get_user_info failed: FULL response: {json.dumps(res, ensure_ascii=False)[:500]}')
        return success, data, cookies

    def send_phone_code(self, phone, cookies, zone='86'):
        api = '/api/sns/web/v2/login/send_code'
        params = {"phone": phone, "zone": zone, "type": "login"}
        splice_api = splice_str(api, params)

        headers, _ = generate_headers(cookies['a1'], splice_api)
        resp = requests.get(
            self.base_url + splice_api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        res = resp.json()
        return res.get('success', False), res.get('msg', ''), res

    def login_by_phone(self, phone, code, cookies, zone='86'):
        check_api = '/api/sns/web/v1/login/check_code'
        params = {"phone": phone, "zone": zone, "code": code}
        splice_api = splice_str(check_api, params)

        headers, _ = generate_headers(cookies['a1'], splice_api)
        resp = requests.get(
            self.base_url + splice_api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        res = resp.json()
        if not res.get('success'):
            return False, res.get('msg', '验证码验证失败'), {'cookies': cookies}
        mobile_token = (res.get('data') or {}).get('mobile_token')
        if not mobile_token:
            return False, res.get('msg', '验证码响应缺少 mobile_token'), {'cookies': cookies, 'res_json': res}

        login_api = '/api/sns/web/v2/login/code'
        data = {"mobile_token": mobile_token, "zone": zone, "phone": phone}
        headers, data = generate_headers(cookies['a1'], login_api, data)
        resp = requests.post(
            self.base_url + login_api,
            headers=headers, cookies=cookies, data=data,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        if not res.get('success'):
            return False, res.get('msg', '登录失败'), {'cookies': cookies}
        session = (res.get('data') or {}).get('session')
        if not session:
            return False, res.get('msg', '登录响应缺少 session'), {'cookies': cookies, 'res_json': res}
        cookies['web_session'] = session
        return True, '成功', {
            'cookies': cookies,
            'res_json': res,
        }

    @staticmethod
    def cookies_to_str(cookies):
        return '; '.join(f'{k}={v}' for k, v in cookies.items())

    @staticmethod
    def show_qrcode_terminal(url):
        qr = qrcode.QRCode(box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)

    @staticmethod
    def show_qrcode_image(url):
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.show()

    def qrcode_login(self, show_in_terminal=True):
        logger.info('[1/4] 正在生成初始cookies...')
        cookies = self.generate_init_cookies()
        logger.info(f'{cookies}')

        logger.info('[2/4] 正在获取二维码...')
        success, msg, qr_data = self.generate_qrcode(cookies)
        if not success:
            logger.error(f'获取二维码失败: {msg}')
            return None
        cookies = qr_data['cookies']

        logger.info('请使用小红书APP扫描以下二维码:')
        if show_in_terminal:
            self.show_qrcode_terminal(qr_data['qr_url'])
        else:
            self.show_qrcode_image(qr_data['qr_url'])

        logger.info('[3/4] 等待扫码...')
        while True:
            success, msg, cookies = self.check_qrcode_status(
                qr_data['qr_id'], qr_data['code'], cookies
            )
            if success:
                logger.info(msg)
                break
            if msg == '二维码已过期':
                logger.error(msg)
                return None
            time.sleep(2)

        logger.info('[4/4] 验证登录状态...')
        success, user_info, cookies = self.get_user_info(cookies)
        if success:
            logger.info(f'用户: {user_info.get("nickname", "未知")} (RedID: {user_info.get("red_id", "未知")})')
        else:
            logger.warning('获取用户信息失败，但cookies可能仍有效')

        cookies_str = self.cookies_to_str(cookies)
        logger.success(f'登录成功!\ncookies:\n{cookies_str}')
        return cookies_str

    def phone_login(self):
        logger.info('[1/4] 正在生成初始cookies...')
        cookies = self.generate_init_cookies()
        logger.info(f'a1={cookies["a1"]}')

        phone = input('请输入手机号: ')
        logger.info('[2/4] 正在发送验证码...')
        success, msg, _ = self.send_phone_code(phone, cookies)
        if not success:
            logger.error(f'发送失败: {msg}')
            return None
        logger.info('验证码已发送')

        code = input('请输入验证码: ')
        logger.info('[3/4] 正在验证...')
        success, msg, result = self.login_by_phone(phone, code, cookies)
        if not success:
            logger.error(f'验证失败: {msg}')
            return None
        cookies = result['cookies']

        logger.info('[4/4] 验证登录状态...')
        success, user_info, cookies = self.get_user_info(cookies)
        if success:
            logger.info(f'用户: {user_info.get("nickname", "未知")} (RedID: {user_info.get("red_id", "未知")})')

        cookies_str = self.cookies_to_str(cookies)
        logger.success(f'登录成功!\ncookies:\n{cookies_str}')
        return cookies_str


if __name__ == '__main__':
    login_api = XHSLoginApi()
    cookies_str = login_api.qrcode_login(show_in_terminal=True)
    # cookies_str = login_api.phone_login()

    xhs_apis = XHS_Apis()
    # 获取用户信息
    user_url = 'https://www.xiaohongshu.com/user/profile/67a332a2000000000d008358?xsec_token=ABTf9yz4cLHhTycIlksF0jOi1yIZgfcaQ6IXNNGdKJ8xg=&xsec_source=pc_feed'
    success, msg, user_info = xhs_apis.search_note("888666", cookies_str)
    print(success, msg, user_info)
