// src/pages/Result.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

interface AnswerItem {
  id: number;
  question_text: string;
  user_answer: string;     // "a" | "b" | "c" | "d"
  correct_answer: string;  // same
  is_correct: boolean;
}

const kanaMap: Record<string, string> = { a: "ア", b: "イ", c: "ウ", d: "エ" };

export default function Result() {
  const [answers, setAnswers] = useState<AnswerItem[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/login");
      return;
    }
    fetch("/api/answers/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data: AnswerItem[]) => setAnswers(data))
      .catch((err) => console.error("fetch answers error", err));
  }, []);

  if (!answers.length)
    return <p className="p-6 text-center">結果を読み込み中…</p>;

  const correctCount = answers.filter((a) => a.is_correct).length;

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold mb-2">結果</h2>
        <p className="text-lg">
          正解数: <span className="font-extrabold text-blue-600">{correctCount}</span> / {answers.length}
        </p>
      </div>

      <div className="overflow-x-auto rounded shadow">
        <table className="w-full border-collapse text-sm">
          <thead className="bg-gray-100 text-gray-700 whitespace-nowrap">
            <tr>
              <th className="border p-2 w-12">#</th>
              <th className="border p-2">問題文</th>
              <th className="border p-2 w-28">あなたの回答</th>
              <th className="border p-2 w-28">正解</th>
            </tr>
          </thead>
          <tbody>
            {answers.map((a, i) => (
              <tr
                key={a.id}
                className={a.is_correct ? "bg-green-50" : "bg-red-50"}
              >
                <td className="border p-2 text-center font-medium">{i + 1}</td>
                <td className="border p-2 whitespace-pre-wrap leading-relaxed">
                  {a.question_text}
                </td>
                <td className="border p-2 text-center font-semibold">
                  {kanaMap[a.user_answer] ?? "-"}
                </td>
                <td className="border p-2 text-center font-semibold">
                  {kanaMap[a.correct_answer] ?? "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="text-center pt-4">
        <button
          onClick={() => navigate("/")}
          className="inline-block px-8 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-500 transition"
        >
          ホームへ戻る
        </button>
      </div>
    </div>
  );
}
