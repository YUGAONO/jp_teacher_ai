# JLPT例文自動生成Webアプリ

このアプリケーションは、日本語の単語とJLPTレベルを入力すると、その単語を使った例文を自動生成するWebサービスです。
バックエンド（FastAPI）とフロントエンド（Streamlit）で構成されています。

## 主な機能
- 単語とJLPTレベル（N1〜N5）を指定して例文を生成
- Dify APIを利用した自動生成（APIキーがない場合はモック例文を返します）

## ディレクトリ構成

```
apps/
  backend/    # FastAPI バックエンド
	 main.py
	 requirements.txt
  frontend/   # Streamlit フロントエンド
	 main.py
	 requirements.txt
render.yaml   # Renderデプロイ用設定
```

## セットアップ方法

1. **リポジトリをクローン**
	```sh
	git clone <このリポジトリのURL>
	cd jp_teacher_ai
	```

2. **環境変数の設定**  
	`apps/.env` ファイルに以下を記載します（Dify APIキーは任意）。
	```
	BACKEND_URL=http://127.0.0.1:8000
	DIFY_API_KEY=あなたのDifyAPIキー
	```

3. **バックエンドの起動**
	```sh
	cd apps/backend
	pip install -r requirements.txt
	uvicorn main:app --reload
	```

4. **フロントエンドの起動**
	```sh
	cd ../frontend
	pip install -r requirements.txt
	streamlit run main.py
	```

5. **Webブラウザでアクセス**  
	[http://localhost:8501](http://localhost:8501) にアクセスしてください。

## デプロイ

`render.yaml` を使って [Render](https://render.com/) で簡単にデプロイできます。

## ライセンス

MIT
