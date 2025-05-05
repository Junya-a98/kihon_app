// frontend/src/pages/Home.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

interface MiniResult {
  solved_at: string;        // ISO 日時
  correct: number;          // 正解数
  total: number;            // 出題数
}

export default function Home() {
  const { logout } = useAuth();
  const navigate   = useNavigate();

  const [apiUser, setApiUser]       = useState<string | null>(null);
  const [results, setResults]       = useState<MiniResult[]>([]);

  // ① ユーザー名取得
  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) return;

    fetch("/api/users/me/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.ok ? r.json() : Promise.reject(r))
      .then((data: { username: string }) => setApiUser(data.username))
      .catch(() => setApiUser(null));
  }, []);

  // ② 直近結果を取得
  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) return;

    fetch("/api/answers/summary/", {   // ★要バックエンド実装
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.ok ? r.json() : [])
      .then((data: MiniResult[]) => setResults(data))
      .catch(() => setResults([]));
  }, []);

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-10">
      <header className="flex items-center justify-between">
        <span className="text-lg">
          こんにちは、<b>{apiUser ?? "ゲスト"}</b> さん
        </span>
        <button
          onClick={() => { logout(); navigate("/login", { replace: true }); }}
          className="px-3 py-1 bg-gray-200 rounded"
        >
          ログアウト
        </button>
      </header>

      <div className="space-y-4">
        <h1 className="text-2xl font-bold">基本情報演習</h1>
        <button
          onClick={() => navigate("/quiz")}
          className="px-6 py-3 bg-blue-600 text-white rounded"
        >
          演習を始める
        </button>
      </div>

      {/* ③ 直近の成績 */}
      {apiUser && (
        <section className="space-y-3">
          <h2 className="text-xl font-semibold">直近の成績</h2>
          {results.length === 0 ? (
            <p className="text-gray-500">まだ成績がありません。</p>
          ) : (
            <ul className="space-y-2">
              {results.map((r, i) => (
                <li
                  key={i}
                  className="border p-3 rounded flex justify-between items-center"
                >
                  <span>
                    {new Date(r.solved_at).toLocaleString()} に解答
                  </span>
                  <span className="font-semibold">
                    {r.correct} / {r.total}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  );
}
