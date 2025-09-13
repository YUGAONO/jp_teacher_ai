# import streamlit as st
# import requests
# import os
# from dotenv import load_dotenv

# # .envファイルの読み込み
# load_dotenv()

# # ページの基本設定
# st.set_page_config(
#     page_title="JLPT Example Generator",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # カスタムCSS
# st.markdown("""
#     <style>
#     .main {
#         padding: 2rem;
#     }
#     .stButton>button {
#         width: 100%;
#     }
#     .output-area {
#         margin: 2rem 0;
#         padding: 1rem;
#         border-radius: 5px;
#         background-color: #f8f9fa;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # バックエンドURLの設定
# BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# def get_jlpt_examples(word, level):
#     try:
#         response = requests.post(
#             f"{BACKEND_URL}/api/v1/examples",
#             json={"word": word, "level": level}
#         )
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         return {"error": str(e)}

# # サイドバー
# with st.sidebar:
#     st.title("設定")
#     st.write("JLPT Example Generator の設定やヘルプ情報を表示します。")
#     st.divider()
#     st.write("© 2024 JLPT Example Generator")

# # メインコンテンツ
# st.title("JLPT Example Sentence Generator")
# st.write("単語とJLPTレベルを入力すると、例文を生成します。")

# # 出力エリア（中央部分）
# output_container = st.container()

# # 入力フォーム（下部に配置）
# with st.container():
#     st.divider()
#     cols = st.columns([2, 1, 1])
    
#     with cols[0]:
#         word_input = st.text_input("単語を入力してください", "勉強")
    
#     with cols[1]:
#         level_input = st.selectbox(
#             "JLPTレベル",
#             ["1", "2", "3", "4", "5"]
#         )
    
#     with cols[2]:
#         generate_button = st.button("例文を生成", use_container_width=True)

# # 例文生成と表示（中央の出力エリアに表示）
# with output_container:
#     if generate_button:
#         if word_input:
#             result = get_jlpt_examples(word_input, level_input)
#             if "error" in result:
#                 st.error(f"エラーが発生しました: {result['error']}")
#             else:
#                 st.subheader("生成された例文:")
#                 with st.container():
#                     for i, example in enumerate(result['examples'], 1):
#                         st.write(f"{i}. {example}")
#         else:
#             st.warning("単語を入力してください")

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# ページの基本設定
st.set_page_config(
    page_title="JLPT Example Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .output-area {
        margin: 2rem 0;
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# バックエンドURLの設定
BACKEND_URL = os.getenv("FASTAPI_URL")

def get_jlpt_examples(word, level):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/examples",
            json={"word": word, "level": level}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# サイドバー
with st.sidebar:
    st.title("設定")
    st.write("JLPT Example Generator の設定やヘルプ情報を表示します。")
    st.divider()
    st.write("© 2024 JLPT Example Generator")

# メインコンテンツ
st.title("JLPT Example Sentence Generator")
st.write("単語とJLPTレベルを入力すると、例文を生成します。")

# 入力フォーム
with st.form(key="example_form"):
    cols = st.columns([2, 1, 1])
    
    with cols[0]:
        word_input = st.text_input("単語を入力してください", value="勉強")
    
    with cols[1]:
        level_input = st.selectbox(
            "JLPTレベル",
            ["1", "2", "3", "4", "5"],
            index=4  # デフォルトをN5（レベル5）に設定
        )
    
    with cols[2]:
        submit_button = st.form_submit_button("例文を生成", use_container_width=True)

# 例文生成と表示
if submit_button:
    if word_input.strip():
        with st.spinner("例文を生成中..."):
            result = get_jlpt_examples(word_input, level_input)
            
        if "error" in result:
            st.error(f"エラーが発生しました: {result['error']}")
        else:
            st.success(f"「{word_input}」のJLPT N{level_input}レベルの例文を生成しました！")
            
            # 例文を表示
            st.subheader("生成された例文:")
            examples = result.get('examples', [])
            
            if examples:
                for i, example in enumerate(examples, 1):
                    st.write(f"**{i}.** {example}")
            else:
                st.warning("例文が生成されませんでした。")
    else:
        st.warning("単語を入力してください")

# フッター情報
st.divider()
st.markdown("**使用方法:**")
st.markdown("1. 学習したい日本語の単語を入力")
st.markdown("2. 目標のJLPTレベルを選択")
st.markdown("3. 「例文を生成」ボタンをクリック")
