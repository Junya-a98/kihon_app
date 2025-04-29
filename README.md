# 基本情報技術者試験 演習サイト

このプロジェクトは、基本情報技術者試験（FE試験）に向けた練習問題演習サイトです。  
**Python (Django) + HTML** で開発しています。

---

## 🎯 現在の機能

- トップページから演習開始ができる
- ランダムに問題を1問ずつ出題
- 一度出題した問題は再出題しない
- 回答後、正誤判定を表示
- 全問終了後、正解数・不正解数をまとめて表示
- セッションリセット機能で再チャレンジ可能

---

## 🚀 セットアップ方法

1. リポジトリをクローン

```bash
git clone https://github.com/Junya-a98/kihon_app.git

2. 仮想環境を作成してアクティベート(任意)
python3 -m venv venv
source venv/bin/activate

3. パッケージをインストール（任意）
pip install -r requirements.txt
# もしくは
poetry install

4.マイグレーション実行
python manage.py migrate

5.開発サーバーを起動
python manage.py runserver


## 🆕 追加実装済みの機能

| 機能 | 概要 |
|------|------|
| 年度・出題数選択 | トップページで「令和 ○ 年度／○ 問だけ」など自由に指定して開始 |
| 進捗バー | 問題 n / N を表示しながら progress タグで視覚化 |
| 詳細結果 | 各問ごとに「あなたの回答 / 正解 / ○×」を色付きリストで表示 |
| ユーザー登録（任意） | `accounts/signup/` でだれでもアカウント作成 → 自動ログイン |
| ログイン／ログアウト | Django built-in 認証 (`/accounts/login/`, `/accounts/logout/`) |
| 解答履歴 | ログインユーザーは `/history/` で過去の正誤を時系列一覧で閲覧 |
| CSV 一括インポート | `scripts/import_fe_questions.py --csv … --year R06 --part A` で問題追加 |

---

## 🗺 画面遷移と URL 一覧

| URL | 画面 | ログイン必須 |
|-----|------|-------------|
| `/` | トップ（年度・出題数フォーム） | × |
| `/start/` | セッション初期化 (POST) | × |
| `/quiz/` | 問題出題ページ | × |
| `/result/` | 結果まとめ | × |
| `/reset/` | セッション初期化→ホーム | × |
| `/accounts/signup/` | ユーザー登録 | × |
| `/accounts/login/` | ログイン | × |
| `/accounts/logout/` | ログアウト | × |
| `/history/` | 自分の解答履歴 | ○ |

---

## 🛠 データベース構成（抜粋）

| モデル | 主なフィールド |
|--------|----------------|
| **Question** | `text`, `choice_a`〜`d`, `correct`, `category`, `exam_year`, `exam_part` |
| **Answer** | `user(FK)`, `question(FK)`, `is_correct`, `guess`, `solved_at` |

---

## ⚙ 開発用コマンド早見表

```bash
# テストユーザー作成
python manage.py createsuperuser

# お試し一般ユーザーを1行で
python manage.py shell -c \
'from django.contrib.auth import get_user_model as g; g().objects.create_user("sample", password="Sample123!")'

# CSVインポート（例：令和6年度 科目A）
python scripts/import_fe_questions.py \
  --csv data/fe_kamoku_a_2024r06_questions_split.csv --year R06 --part A
