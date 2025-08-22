FROM python:3.12-slim

# backend 配下で作業する
WORKDIR /backend

# 依存パッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションとマイグレーション関連をコピー
COPY ./app ./app
COPY ./migrations ./migrations
COPY alembic.ini .

# FastAPI を起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
