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
cd リポジトリ名

2. 仮想環境を作成してアクティベート
python3 -m venv venv
source venv/bin/activate

3. パッケージをインストール
pip install -r requirements.txt
# もしくは
poetry install

4.マイグレーション実行
python manage.py migrate

5.開発サーバーを起動
python manage.py runserver


ページ | 説明
/ | トップページ
/quiz/ | 演習問題を解く
/result/ | 演習結果をまとめて表示
/reset/ | セッションリセットして再スタート
