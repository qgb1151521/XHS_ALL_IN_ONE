from __future__ import annotations

import importlib
import logging
import sys
from typing import Any

from backend.app.adapters.xhs.request_env import direct_xhs_request_env

logger = logging.getLogger(__name__)


def _ensure_login_apis_module():
    """强制重载 apis.xhs_pc_login_apis 模块，确保修改后无需重启后端即可生效。"""
    if "apis.xhs_pc_login_apis" in sys.modules:
        importlib.reload(sys.modules["apis.xhs_pc_login_apis"])


class XhsPcLoginAdapter:
    def create_qrcode(self) -> dict[str, Any]:
        with direct_xhs_request_env():
            _ensure_login_apis_module()
            from apis.xhs_pc_login_apis import XHSLoginApi

            api = XHSLoginApi()
            cookies = api.generate_init_cookies()
            success, message, payload = api.generate_qrcode(cookies)
        if not success or not payload:
            raise RuntimeError(message)
        return {
            "cookies": payload["cookies"],
            "qr_id": payload["qr_id"],
            "code": payload["code"],
            "qr_url": payload["qr_url"],
        }

    def check_qrcode_status(self, qr_id: str, code: str, cookies: dict[str, Any]) -> dict[str, Any]:
        with direct_xhs_request_env():
            _ensure_login_apis_module()
            from apis.xhs_pc_login_apis import XHSLoginApi

            api = XHSLoginApi()
            success, message, updated_cookies = api.check_qrcode_status(qr_id, code, cookies)
        logger.info(f"[PC_LOGIN] check_qrcode_status: success={success}, message={message!r}, has_web_session={'web_session' in updated_cookies}")
        status = "confirmed" if success else "pending"
        if "过期" in message or "expired" in message.lower():
            status = "expired"
        if "确认" in message or "confirm" in message.lower():
            status = "scanned"
        return {"status": status, "cookies": updated_cookies}

    def get_user_info(self, cookies: dict[str, Any]) -> dict[str, Any]:
        with direct_xhs_request_env():
            _ensure_login_apis_module()
            from apis.xhs_pc_login_apis import XHSLoginApi

            api = XHSLoginApi()
            success, data, _ = api.get_user_info(cookies)
        if not success or not data:
            logger.warning(f"[PC_LOGIN] get_user_info failed or empty, cookies may still be valid. success={success}, data_keys={list(data.keys()) if data else 'EMPTY'}")
            # 不抛异常 —— cookies可能仍有效，返回最小user_info让账户仍可创建
            return {
                "external_user_id": "",
                "nickname": "",
                "avatar_url": "",
                "profile": {"raw": data or {}},
            }
        return {
            "external_user_id": data.get("user_id", ""),
            "nickname": data.get("nickname", ""),
            "avatar_url": data.get("images") or data.get("imageb") or "",
            "profile": {
                "red_id": data.get("red_id") or data.get("redId") or "",
                "followers": data.get("fans") or data.get("followers") or data.get("follower_count"),
                "following": data.get("follows") or data.get("following") or data.get("following_count"),
                "likes": data.get("liked_count") or data.get("likes") or data.get("like_count"),
                "raw": data,
            },
        }

    def create_phone_session(self, phone: str) -> dict[str, Any]:
        with direct_xhs_request_env():
            _ensure_login_apis_module()
            from apis.xhs_pc_login_apis import XHSLoginApi

            api = XHSLoginApi()
            cookies = api.generate_init_cookies()
            success, message, _ = api.send_phone_code(phone, cookies)
        if not success:
            raise RuntimeError(message)
        return {"cookies": cookies, "message": message or "sent"}

    def confirm_phone_login(self, phone: str, code: str, cookies: dict[str, Any]) -> dict[str, Any]:
        with direct_xhs_request_env():
            _ensure_login_apis_module()
            from apis.xhs_pc_login_apis import XHSLoginApi

            api = XHSLoginApi()
            success, message, payload = api.login_by_phone(phone, code, cookies)
        if not success or not payload:
            raise RuntimeError(message)
        return {"status": "confirmed", "cookies": payload["cookies"]}
