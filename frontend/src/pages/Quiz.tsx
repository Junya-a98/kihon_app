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
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const yearParam = searchParams.get("year");
  const limitParam = searchParams.get("limit");

  // selector states (params 未指定時のみ使用)
  const [yearSel, setYearSel]   = useState<string>(yearParam ?? "");
  const [limitSel, setLimitSel] = useState<number>(Number(limitParam) || 5);
  const [yearMax, setYearMax]   = useState<number>(50); // 年度選択で更新

  const [qs, setQs]     = useState<Question[]>([]);
  const [idx, setIdx]   = useState(0);
  const [answer, setAnswer] = useState<string>("");

  // ---- 年度リスト ----
  const [yearOptions, setYearOptions] = useState<string[]>([]);
  useEffect(() => {
    fetch("/api/years/")
      .then(r => r.json())
      .then((data: string[]) => setYearOptions(data));
  }, []);

  // ---- 年度が選ばれたら最大問題数を取得 ----
  useEffect(() => {
    if (!yearSel) return;
    fetch(`/api/questions?exam_year=${yearSel}`)
      .then(r => r.json())
      .then((data: Question[]) => {
        setYearMax(data.length);
        if (limitSel > data.length) setLimitSel(data.length);
      });
  }, [yearSel]);

  // ---- 問題取得 ----
  useEffect(() => {
    if (!yearParam || !limitParam) return;
    const query = new URLSearchParams();
    query.append("exam_year", yearParam);
    query.append("limit", limitParam);

    fetch(`/api/questions?${query.toString()}`)
      .then(r => r.json())
      .then(setQs)
      .catch(err => console.error("fetch questions error", err));
  }, [yearParam, limitParam]);

  // ---- クイズ開始 ----
  const startQuiz = () => {
    if (!yearSel) return;
    setSearchParams({ year: yearSel, limit: String(limitSel) });
  };

  const submitAnswer = async () => {
    await fetch("/api/submit_answer/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access")}`,
      },
      body: JSON.stringify({
        question_id: q.id,
        user_answer: answer,
      }),
    });
  };

  // ---- 次へ ----
  const onNext = async() => {
    await submitAnswer();
          try {
             await submitAnswer();
           } catch (e) {
              console.error("回答の保存に失敗しました", e);
            }

    if (idx + 1 < qs.length) {
      setIdx(idx + 1);
      setAnswer("");
    } else {
      navigate("/result");
    }
  };

  /* ---------------- セレクター画面 ---------------- */
  if (!yearParam || !limitParam) {
    return (
      <div className="p-6 max-w-lg mx-auto space-y-6">
        <h2 className="text-xl font-semibold">年度と問題数を選択</h2>

        {/* 年度セレクト */}
        <div>
          <label className="block mb-1 font-medium">年度</label>
          <select
            className="border px-3 py-2 rounded w-full"
            value={yearSel}
            onChange={e => setYearSel(e.target.value)}
          >
            <option value="" disabled>
              年度を選択
            </option>
            {yearOptions.map(y => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </div>

        {/* 出題数インプット */}
        <div>
          <label className="block mb-1 font-medium">
            出題数 <span className="text-sm text-gray-500">(最大 {yearMax} 問)</span>
          </label>
          <input
            type="number"
            min={1}
            max={yearMax}
            className="border px-3 py-2 rounded w-full"
            value={limitSel}
            onChange={e => setLimitSel(Math.min(Number(e.target.value), yearMax))}
          />
        </div>

        <button
          onClick={startQuiz}
          disabled={!yearSel}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          クイズ開始
        </button>
      </div>
    );
  }

  /* ---------------- クイズ画面 ---------------- */
  if (!qs.length) return <p className="p-6">読み込み中…</p>;

  const q = qs[idx];
  const kana = ["ア", "イ", "ウ", "エ"] as const;

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-lg font-semibold mb-6">
        {yearParam} 年度 問題 ({idx + 1} / {qs.length})
      </h2>

      <p className="whitespace-pre-line leading-relaxed mb-8">{q.text}</p>

      {/* 選択肢を縦に並べる（各選択肢を明確にブロック要素として配置） */}
      <div className="mt-6">
        {(["a", "b", "c", "d"] as const).map((k, i) => (
          <div key={k} className="mb-4 block w-full">
            <label
              className="flex items-center p-4 border rounded cursor-pointer hover:bg-gray-50 w-full"
            >
              <input
                type="radio"
                name="ans"
                value={k}
                className="mr-3"
                checked={answer === k}
                onChange={() => setAnswer(k)}
              />
              <span className="font-semibold mr-2">{kana[i]}.</span>
              <span className="flex-1">{q[`choice_${k}`]}</span>
            </label>
          </div>
        ))}
      </div>

      <button
        onClick={onNext}
        disabled={!answer}
        className="mt-10 px-6 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {idx + 1 < qs.length ? "次へ" : "結果を見る"}
      </button>
    </div>
  );
}