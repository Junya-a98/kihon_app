// src/pages/Quiz.tsx
import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";

interface Question {
  id: number;
  text: string;
  choice_a: string;
  choice_b: string;
  choice_c: string;
  choice_d: string;
  correct: string;
}

export default function Quiz() {
  const [qs, setQs] = useState<Question[]>([]);
  const [idx, setIdx] = useState(0);
  const [answer, setAnswer] = useState<string>("");
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const year = params.get("year")!;
  const limit = params.get("limit")!;

  useEffect(() => {
    fetch(`/api/questions?exam_year=${year}&limit=${limit}`)
      .then((r) => r.json())
      .then(setQs);
  }, [year, limit]);

  const onNext = () => {
    // TODO: 正誤判定 & API へ POST して保存
    if (idx + 1 < qs.length) {
      setIdx(idx + 1);
      setAnswer("");
    } else {
      navigate("/result");
    }
  };

  if (!qs.length) return <p>読み込み中…</p>;

  const q = qs[idx];
  return (
    <div className="p-6">
      <h2>
        {year}年度 問題 ({idx + 1} / {qs.length})
      </h2>
      <p className="mt-4">{q.text}</p>
      <div className="mt-4 space-y-2">
        {(["a","b","c","d"] as const).map((k) => (
          <label key={k} className="block">
            <input
              type="radio"
              name="ans"
              value={k}
              checked={answer===k}
              onChange={() => setAnswer(k)}
            />{" "}
            {q[`choice_${k}`]}
          </label>
        ))}
      </div>
      <button
        onClick={onNext}
        disabled={!answer}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded"
      >
        {idx + 1 < qs.length ? "次へ" : "結果を見る"}
      </button>
    </div>
  );
}
