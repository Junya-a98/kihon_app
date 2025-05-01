# 基本情報技術者試験 Webアプリ

## 🚀 セットアップ手順（非 Docker）

```bash
# 1. リポジトリ取得
git clone https://github.com/Junya-a98/kihon_app.git
cd kihon_app

# 2. （任意）仮想環境
python3 -m venv venv
source venv/bin/activate

# 3. 依存パッケージ
pip install -r requirements.txt        # または poetry install

# 4. マイグレーション
python manage.py migrate

# 5. 開発サーバー
python manage.py runserver



🐳 Docker での起動
# 初回ビルド＆起動
docker compose up --build

# DB マイグレーション
docker compose exec backend python manage.py migrate

# 静的ファイル（管理画面用）
docker compose exec backend python manage.py collectstatic --noinput

# CSV インポート（例：令和6年度 科目A）
docker compose exec backend \
  python /app/scripts/import_fe_questions.py \
    --csv /app/data/reiwa6_only.csv --year R06 --part A


🆕 実装済み機能

| 機能 | 概要 |
|------|------|
| 年度・出題数選択 | トップで「令和◯年／◯問」など自由に指定 |
| 進捗バー | n / N を progress タグで表示 |
| 詳細結果 | 各問の回答・正誤を色付きで表示 |
| ユーザー登録 & 認証 | `/accounts/signup/`, `/accounts/login/` |
| 解答履歴 | `/history/` に時系列で保存 |
| CSV インポート | `scripts/import_fe_questions.py` で一括登録 |


🗺 URL 一覧

| URL | 画面 | 要ログイン |
|-----|------|-----------|
| `/` | トップ（年度選択） | × |
| `/start/` | クイズ開始 (POST) | × |
| `/quiz/` | 出題ページ | × |
| `/result/` | 結果まとめ | × |
| `/reset/` | セッション初期化 | × |
| `/accounts/signup/` | 新規登録 | × |
| `/accounts/login/` | ログイン | × |
| `/accounts/logout/` | ログアウト | × |
| `/history/` | 自分の履歴 | ○ |




🧪 開発用コマンド集
# スーパーユーザー
docker compose exec backend python manage.py createsuperuser

# テストユーザー1行生成
docker compose exec backend python manage.py shell -c \
'from django.contrib.auth import get_user_model as g; g().objects.create_user("sample", password="Sample123!")'

# インポート例（令和6年度）
docker compose exec backend \
  python /app/scripts/import_fe_questions.py \
    --csv /app/data/reiwa6_only.csv --year R06 --part A
