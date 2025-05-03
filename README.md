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
