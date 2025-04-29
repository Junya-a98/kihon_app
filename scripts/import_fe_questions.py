#!/usr/bin/env python
"""
任意年度・任意科目A/Bの CSV をまとめてインポートするツール

例:
  python scripts/import_fe_questions.py \
      --csv data/fe_kamoku_a_2024r06_questions_split.csv \
      --year R06 --part A
  python scripts/import_fe_questions.py \
      --csv data/fe_kamoku_a_text_only.csv \
      --year R06 --part A
"""
import argparse, csv, os, django, pathlib, sys
from typing import List

# Django 設定ロード
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from exams.models import Question  # noqa: E402

# カナ→アルファベットマッピング
KANA2ABC = {"ア": "a", "イ": "b", "ウ": "c", "エ": "d"}


def import_csv(path: pathlib.Path, year: str, part: str) -> int:
    """
    任意フォーマットの CSV を読み込み、
    Question モデルに bulk_create する
    """
    objs: List[Question] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        # 列名を動的に決定
        text_key   = "説明文" if "説明文" in headers else "問題文"
        # 選択肢列のペア (モデル側のフィールド, CSVヘッダ)
        choice_keys = [
            ("choice_a", "選択肢ア" if "選択肢ア" in headers else "ア"),
            ("choice_b", "選択肢イ" if "選択肢イ" in headers else "イ"),
            ("choice_c", "選択肢ウ" if "選択肢ウ" in headers else "ウ"),
            ("choice_d", "選択肢エ" if "選択肢エ" in headers else "エ"),
        ]
        answer_key = "解答" if "解答" in headers else "答"

        for row in reader:
            # 正解カナ取得
            raw = row.get(answer_key, "").strip()
            if not raw:
                print(f"[WARN] 解答欄が空: {row}")
                continue
            kana = raw[0]
            if kana not in KANA2ABC:
                print(f"[WARN] 変換不能な解答: {raw} (行スキップ)")
                continue
            correct_letter = KANA2ABC[kana]

            # 問題文
            text = row.get(text_key, "").strip()

            # 各選択肢
            choices = {}
            for field_name, col_name in choice_keys:
                choices[field_name] = row.get(col_name, "").strip()

            objs.append(
                Question(
                    text       = text,
                    choice_a   = choices["choice_a"],
                    choice_b   = choices["choice_b"],
                    choice_c   = choices["choice_c"],
                    choice_d   = choices["choice_d"],
                    correct    = correct_letter,
                    category   = f"FE_{year}{part}",
                    exam_year  = year,
                    exam_part  = part,
                )
            )

    # bulk insert（重複は無視）
    created = Question.objects.bulk_create(objs, ignore_conflicts=True)
    return len(created)


def main() -> None:
    parser = argparse.ArgumentParser(description="FE 質問 CSV インポータ")
    parser.add_argument("--csv",  required=True, help="CSV ファイルパス")
    parser.add_argument("--year", required=True, help="年度コード 例: R06")
    parser.add_argument(
        "--part", required=True,
        choices=["A", "B"], help="科目 A or B"
    )
    args = parser.parse_args()

    csv_path = pathlib.Path(args.csv)
    if not csv_path.exists():
        print(f"[ERROR] CSV が見つかりません: {csv_path}")
        sys.exit(1)

    count = import_csv(csv_path, args.year, args.part)
    print(f"✅  {count} 件を category=FE_{args.year}{args.part} として登録しました")


if __name__ == "__main__":
    main()
