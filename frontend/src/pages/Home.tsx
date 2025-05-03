// frontend/src/pages/Home.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Home() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [apiUser, setApiUser] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) return;

    (async () => {
      try {
        // ← ここを相対パスに戻す
        const res = await fetch(`/api/users/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error(`status ${res.status}`);
        const data = (await res.json()) as { username: string };
        setApiUser(data.username);
      } catch (err) {
        console.error("ユーザー取得失敗", err);
      }
    })();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <header style={{ marginBottom: 20 }}>
        <span>こんにちは、{apiUser ?? "ゲスト"} さん</span>
        <button
          onClick={() => {
            logout();
            navigate("/login", { replace: true });
          }}
          style={{ marginLeft: 12 }}
        >
          ログアウト
        </button>
      </header>
      <h1>基本情報演習</h1>
      <button onClick={() => navigate("/quiz")} style={{ marginTop: 20 }}>
        演習を始める
      </button>
    </div>
  );
}
