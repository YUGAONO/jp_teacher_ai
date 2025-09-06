import streamlit as st
import requests
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# バックエンドURLの設定
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def get_jlpt_examples(word, level):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/examples",
            json={"word": word, "level": level}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

st.title("JLPT Example Sentence Generator")
st.write("単語とJLPTレベルを入力すると、例文を生成します。")

# 入力フォーム
word_input = st.text_input("単語を入力してください", "勉強")
level_input = st.selectbox(
    "JLPTレベルを選択してください",
    ["N1", "N2", "N3", "N4", "N5"]
)

# 例文生成ボタン
if st.button("例文を生成"):
    if word_input:
        result = get_jlpt_examples(word_input, level_input)
        if "error" in result:
            st.error(f"エラーが発生しました: {result['error']}")
        else:
            st.subheader("生成された例文:")
            for i, example in enumerate(result["examples"], 1):
                st.write(f"{i}. {example}")
    else:
        st.warning("単語を入力してください")