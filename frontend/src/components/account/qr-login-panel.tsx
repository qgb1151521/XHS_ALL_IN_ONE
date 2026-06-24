import { Alert, Button, Card, Checkbox, Space, Typography } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import axios from "axios";
import { useCallback, useEffect, useRef, useState } from "react";

import { createXhsCreatorQrLoginSession, createXhsPcQrLoginSession, pollXhsLoginSession } from "../../lib/api";
import type { PlatformAccount, XhsQrLoginSession } from "../../types";

const { Text, Link: AntLink } = Typography;

type QrLoginPanelProps = {
  accountType: "pc" | "creator";
  onConfirmed: (account: PlatformAccount) => void;
};

export function QrLoginPanel({ accountType, onConfirmed }: QrLoginPanelProps) {
  const [session, setSession] = useState<XhsQrLoginSession | null>(null);
  const [statusText, setStatusText] = useState("准备生成二维码");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [syncCreator, setSyncCreator] = useState(false);
  const confirmedRef = useRef(false);

  // 用 ref 保存 onConfirmed，避免 useEffect 依赖变化导致 interval 重建
  const onConfirmedRef = useRef(onConfirmed);
  onConfirmedRef.current = onConfirmed;

  function errorMessage(error: unknown): string {
    if (axios.isAxiosError(error)) {
      const detail = error.response?.data?.detail;
      if (typeof detail === "string" && detail) {
        return detail;
      }
    }
    return "二维码生成失败，请稍后重试。";
  }

  async function startSession() {
    setIsLoading(true);
    setError(null);
    confirmedRef.current = false;
    try {
      const nextSession =
        accountType === "pc"
          ? await createXhsPcQrLoginSession({ sync_creator: syncCreator })
          : await createXhsCreatorQrLoginSession();
      setSession(nextSession);
      setStatusText(accountType === "pc" ? "请使用小红书 App 扫描二维码" : "请使用小红书 App 扫描 Creator 二维码");
    } catch (caught) {
      setError(errorMessage(caught));
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void startSession();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [accountType, syncCreator]);

  // 轮询 useEffect：只依赖 session_id，不依赖 session.status
  // 这样 interval 不会被 status 变化重建，确保轮询稳定进行
  useEffect(() => {
    const sessionId = session?.session_id;
    if (!sessionId) return;

    // 如果已经是终态，不再轮询
    if (session.status === "confirmed" || session.status === "expired") {
      return;
    }

    const interval = window.setInterval(async () => {
      try {
        const polled = await pollXhsLoginSession(sessionId);
        // 轮询成功时清除之前的错误
        setError(null);
        setSession((current) => ({
          ...polled,
          qr_image_data_url: polled.qr_image_data_url ?? current?.qr_image_data_url
        }));
        if (polled.status === "scanned") {
          setStatusText("已扫码，请在手机端确认登录");
        } else if (polled.status === "expired") {
          setStatusText("二维码已过期，请刷新");
        } else if (polled.status === "confirmed") {
          if (polled.account && !confirmedRef.current) {
            confirmedRef.current = true;
            setStatusText("账号绑定成功");
            onConfirmedRef.current(polled.account);
          } else if (!polled.account) {
            // confirmed 但没有 account 数据，仍然标记成功
            confirmedRef.current = true;
            setStatusText("登录成功，但获取账号信息失败");
          }
        }
      } catch (err: unknown) {
        // 提取具体错误信息方便调试
        let detail = "轮询登录状态失败，正在等待下一次尝试。";
        if (axios.isAxiosError(err)) {
          const respDetail = err.response?.data?.detail;
          if (typeof respDetail === "string" && respDetail) {
            detail = respDetail;
          } else if (err.code === "ECONNABORTED" || err.code === "ETIMEDOUT") {
            detail = "请求超时，正在等待下一次尝试。";
          } else if (!err.response) {
            detail = "网络连接异常，正在等待下一次尝试。";
          }
        }
        console.error("[QR_POLL] failed:", err);
        setError(detail);
      }
    }, 2000);

    return () => window.clearInterval(interval);
    // 关键修复：不再依赖 session?.status，避免每次 status 变化时重建 interval
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session?.session_id, session?.status === "confirmed", session?.status === "expired"]);

  return (
    <Space direction="vertical" size="middle" style={{ width: "100%" }}>
      <Card
        styles={{
          body: {
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: 24,
            minHeight: 220,
            background: "#1f1f1f",
          },
        }}
        style={{ borderColor: "#303030" }}
      >
        {session?.qr_image_data_url ? (
          <img
            src={session.qr_image_data_url}
            alt="小红书登录二维码"
            style={{ width: 180, height: 180, borderRadius: 8, background: "#fff", padding: 8 }}
          />
        ) : (
          <div
            style={{
              width: 180,
              height: 180,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: "#262626",
              borderRadius: 8,
              color: "rgba(255,255,255,0.3)",
              fontSize: 28,
              fontWeight: 700,
            }}
          >
            QR
          </div>
        )}
      </Card>

      <div style={{ textAlign: "center" }}>
        <Text strong style={{ display: "block", marginBottom: 4, color: "rgba(255,255,255,0.88)" }}>
          {statusText}
        </Text>
        {session?.qr_url ? (
          <AntLink href={session.qr_url} target="_blank" rel="noreferrer">
            打开二维码链接
          </AntLink>
        ) : null}
      </div>

      {accountType === "pc" ? (
        <Checkbox
          checked={syncCreator}
          onChange={(event) => setSyncCreator(event.target.checked)}
          style={{ color: "rgba(255,255,255,0.88)" }}
        >
          登录 PC 后同步 Creator 账号
        </Checkbox>
      ) : null}

      {error ? <Alert type="error" message={error} showIcon /> : null}

      <Button
        block
        icon={<ReloadOutlined />}
        onClick={startSession}
        loading={isLoading}
      >
        {isLoading ? "生成中..." : "刷新二维码"}
      </Button>
    </Space>
  );
}
