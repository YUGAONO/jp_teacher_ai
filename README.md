# JP Teacher AI

このアプリケーションは、日本語学習を支援するWebサービスです。学習した単語からPDFの単語帳を生成したり、単語とJLPTレベルを指定して例文を生成することができます。

## 主な機能
- **単語PDF生成**: 学習した単語リストから美しい学習用PDFを生成
- **例文生成**: 単語とJLPTレベル（N1〜N5）を指定して例文を自動生成
- **Dify API連携**: AI による高品質な例文・単語分析

## 技術スタック
- **フロントエンド**: Vue.js + TypeScript + Vite + Tailwind CSS
- **バックエンド**: FastAPI + Python
- **PDF生成**: ReportLab
- **AI連携**: Dify API
- **認証**: JWT認証
- **データベース**: Supabase

## ディレクトリ構成

```
apps/
  backend/        # FastAPI バックエンド
    main.py
    requirements.txt
    models/         # Pydanticモデル
    routers/        # APIルーター
    services/       # ビジネスロジック
    config/         # 設定ファイル
  frontend-vue/   # Vue.js フロントエンド
    src/
      components/   # Vueコンポーネント
      services/     # API通信
      stores/       # Pinia状態管理
      router/       # Vue Router
docker-compose.yml     # 開発用Docker Compose
docker-compose.prod.yml # 本番用Docker Compose
```

## 🐳 Docker Composeでの起動（推奨）

### 開発環境
```bash
# リポジトリをクローン
git clone <このリポジトリのURL>
cd jp_teacher_ai

# 環境変数の設定
cp .env.example .env
# .envファイルを編集して必要な設定を行う

# Docker Composeで起動
docker compose up --build

# アクセス
# フロントエンド: http://localhost:3000
# バックエンド: http://localhost:8000
```

### 本番環境
```bash
# 本番用設定で起動
docker compose -f docker-compose.prod.yml up --build

# アクセス
# フロントエンド: http://localhost
# バックエンド: http://localhost:8000
```

## 🛠️ ローカル開発セットアップ

### 必要な環境変数
`.env` ファイルを作成し、以下を設定してください：

```env
# Dify API設定
DIFY_API_KEY=your_dify_api_key
DIFY_BASE_URL=https://api.dify.ai/v1/workflows/run

# JWT設定
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Supabase設定
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# CORS設定
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### バックエンドの起動
```bash
cd apps/backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### フロントエンドの起動
```bash
cd apps/frontend-vue
npm install
npm run dev
```

## 📚 使用方法

1. **ユーザー登録・ログイン**
   - サイドバーから新規登録またはログインを行います

2. **単語PDF生成**
   - 「📚 単語PDF生成」メニューをクリック
   - 学習した単語を改行区切りで入力
   - 「PDF生成」ボタンでPDFを生成・ダウンロード

3. **例文生成**
   - 「📝 例文生成」メニューをクリック
   - 単語とJLPTレベルを入力して例文を生成

## 🚀 デプロイ

`render.yaml` を使って [Render](https://render.com/) でデプロイ可能です。

## 🤝 開発に参加

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 ライセンス

MIT License
