#!/usr/bin/env python
"""
任意年度・任意科目A/Bの CSV をまとめてインポートするツール

例:
  python scripts/import_fe_questions.py \
      --csv data/fe_kamoku_a_2024r06_questions_split.csv \
      --year R06 --part A
"""
import argparse, csv, os, django, pathlib, sys
from typing import List

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from exams.models import Question  # noqa: E402


KANA2ABC = {"ア": "a", "イ": "b", "ウ": "c", "エ": "d"}


def import_csv(path: pathlib.Path, year: str, part: str) -> int:
    """1 つの CSV を読み込み、DB に Question を bulk_create する"""
    objs: List[Question] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                correct_letter = KANA2ABC[row["解答"].strip()[0]]
            except KeyError:
                print(f"[WARN] 変換不能な解答: {row['解答']}, スキップ")
                continue

            objs.append(
                Question(
                    text=row["説明文"].strip(),
                    choice_a=row["選択肢ア"].strip(),
                    choice_b=row["選択肢イ"].strip(),
                    choice_c=row["選択肢ウ"].strip(),
                    choice_d=row["選択肢エ"].strip(),
                    correct=correct_letter,
                    category=f"FE_{year}{part}",
                    exam_year=year,
                    exam_part=part,
                )
            )

    created = Question.objects.bulk_create(objs, ignore_conflicts=True)
    return len(created)


def main() -> None:
    parser = argparse.ArgumentParser(description="FE 質問 CSV インポータ")
    parser.add_argument("--csv", required=True, help="CSV ファイルパス")
    parser.add_argument("--year", required=True, help="年度コード 例: R06")
    parser.add_argument("--part", required=True, choices=["A", "B"], help="科目 A or B")
    args = parser.parse_args()

    csv_path = pathlib.Path(args.csv)
    if not csv_path.exists():
        print(f"[ERROR] CSV が見つかりません: {csv_path}")
        sys.exit(1)

    inserted = import_csv(csv_path, args.year, args.part)
    print(f"✅  {inserted} 件を category=FE_{args.year}{args.part} として登録しました")


if __name__ == "__main__":
    main()

