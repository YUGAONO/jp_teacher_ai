import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Dify API configuration
DIFY_API_KEY = os.getenv('DIFY_API_KEY', '')
DIFY_BASE_URL = 'https://api.dify.ai/v1/workflows/run'

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# CORS configuration
def get_cors_origins():
    origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
    if origins_env.strip():
        return [o.strip() for o in origins_env.split(",") if o.strip()]
    else:
        # 環境に応じて動的に設定
        default_origins = [
            "http://localhost:8501", 
            "http://127.0.0.1:8501",
            "http://streamlit:8501",  # Docker環境用
            "http://localhost:5173",  # Vue.js 開発サーバー（デフォルト）
            "http://127.0.0.1:5173",  # Vue.js 開発サーバー（代替）
            "http://localhost:3000",  # Vue.js 開発サーバー（カスタムポート）
            "http://127.0.0.1:3000",  # Vue.js 開発サーバー（カスタムポート代替）
            "http://localhost:4173",  # Vue.js プレビューサーバー
            "http://127.0.0.1:4173"   # Vue.js プレビューサーバー（代替）
        ]
        return default_origins

CORS_ALLOWED_ORIGINS = get_cors_origins()