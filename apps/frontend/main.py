import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json
from typing import Optional

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
    .auth-form {
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .user-info {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# バックエンドURLの設定（環境変数の優先順位を考慮）
BACKEND_URL = os.getenv("FASTAPI_URL") or os.getenv("BACKEND_URL") or "http://127.0.0.1:8000"

# セッション状態の初期化
if 'user' not in st.session_state:
    st.session_state.user = None
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# ローカルストレージからセッション復元
def load_session_from_storage():
    """ローカルストレージからセッション情報を復元 (簡易版)"""
    # Docker環境ではJavaScript機能を簡素化
    pass

def save_session_to_storage(user, token):
    """セッション情報をローカルストレージに保存 (簡易版)"""
    # Docker環境ではJavaScript機能を簡素化
    pass

def clear_session_from_storage():
    """ローカルストレージからセッション情報を削除 (簡易版)"""
    # Docker環境ではJavaScript機能を簡素化
    pass

# 初回ロード時にセッション復元を試行
if st.session_state.user is None:
    load_session_from_storage()

def make_authenticated_request(url, method="GET", data=None):
    """認証が必要なリクエストを送信"""
    headers = {}
    if st.session_state.access_token:
        headers['Authorization'] = f'Bearer {st.session_state.access_token}'
    
    if method == "GET":
        return requests.get(url, headers=headers)
    elif method == "POST":
        return requests.post(url, json=data, headers=headers)
    elif method == "PUT":
        return requests.put(url, json=data, headers=headers)

def signup_user(email, password, display_name, locale="ja"):
    """新規ユーザー登録"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/signup",
            json={
                "email": email,
                "password": password,
                "display_name": display_name,
                "locale": locale
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data['access_token']
            st.session_state.user = data['user']
            # ローカルストレージに保存
            save_session_to_storage(data['user'], data['access_token'])
            return True, "アカウントが正常に作成されました！"
        else:
            return False, f"登録に失敗しました: {response.json().get('detail', '不明なエラー')}"
    except Exception as e:
        return False, f"エラーが発生しました: {str(e)}"

def signin_user(email, password):
    """ユーザーログイン"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/signin",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data['access_token']
            st.session_state.user = data['user']
            # ローカルストレージに保存
            save_session_to_storage(data['user'], data['access_token'])
            return True, "ログインしました！"
        else:
            return False, f"ログインに失敗しました: {response.json().get('detail', '不明なエラー')}"
    except Exception as e:
        return False, f"エラーが発生しました: {str(e)}"

def signout_user():
    """ユーザーログアウト"""
    try:
        if st.session_state.access_token:
            make_authenticated_request(f"{BACKEND_URL}/api/v1/auth/signout", method="POST")
        
        st.session_state.user = None
        st.session_state.access_token = None
        st.session_state.show_signup = False
        # ローカルストレージからも削除
        clear_session_from_storage()
        return True, "ログアウトしました"
    except Exception as e:
        return False, f"ログアウト中にエラーが発生しました: {str(e)}"

def get_jlpt_examples(word, level):
    """例文取得（認証付き）"""
    try:
        response = make_authenticated_request(
            f"{BACKEND_URL}/api/v1/examples",
            method="POST",
            data={"word": word, "level": level}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_user_profile():
    """ユーザープロフィール取得"""
    try:
        response = make_authenticated_request(f"{BACKEND_URL}/api/v1/auth/profile")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get('detail', 'プロフィール取得に失敗しました')
    except Exception as e:
        return False, f"エラーが発生しました: {str(e)}"

def update_user_profile(display_name=None, locale=None, current_plan=None):
    """ユーザープロフィール更新"""
    try:
        update_data = {}
        if display_name is not None:
            update_data["display_name"] = display_name
        if locale is not None:
            update_data["locale"] = locale
        if current_plan is not None:
            update_data["current_plan"] = current_plan
        
        response = make_authenticated_request(
            f"{BACKEND_URL}/api/v1/auth/profile",
            method="PUT",
            data=update_data
        )
        
        if response.status_code == 200:
            updated_profile = response.json()
            # セッション状態のユーザー情報も更新
            st.session_state.user.update({
                "display_name": updated_profile["display_name"],
                "locale": updated_profile["locale"],
                "current_plan": updated_profile["current_plan"]
            })
            # ローカルストレージも更新
            save_session_to_storage(st.session_state.user, st.session_state.access_token)
            return True, "プロフィールが更新されました！"
        else:
            return False, response.json().get('detail', 'プロフィール更新に失敗しました')
    except Exception as e:
        return False, f"エラーが発生しました: {str(e)}"

# サイドバー
# サイドバー
with st.sidebar:
    st.title("JLPT Example Generator")
    
    # 認証状態に応じたUI表示
    if st.session_state.user is None:
        # 未ログイン時の表示
        st.subheader("ログイン・新規登録")
        
        # タブでログイン/サインアップを切り替え
        tab1, tab2 = st.tabs(["ログイン", "新規登録"])
        
        with tab1:
            # ログインフォーム
            with st.form("login_form"):
                email = st.text_input("メールアドレス", key="login_email")
                password = st.text_input("パスワード", type="password", key="login_password")
                login_submit = st.form_submit_button("ログイン", use_container_width=True)
                
                if login_submit:
                    if email and password:
                        success, message = signin_user(email, password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("メールアドレスとパスワードを入力してください")
        
        with tab2:
            # サインアップフォーム
            with st.form("signup_form"):
                new_email = st.text_input("メールアドレス", key="signup_email")
                new_password = st.text_input("パスワード", type="password", key="signup_password")
                confirm_password = st.text_input("パスワード確認", type="password", key="confirm_password")
                display_name = st.text_input("表示名", key="display_name")
                locale = st.selectbox("言語", ["ja", "en"], key="locale")
                signup_submit = st.form_submit_button("新規登録", use_container_width=True)
                
                if signup_submit:
                    if new_email and new_password and display_name:
                        if new_password == confirm_password:
                            success, message = signup_user(new_email, new_password, display_name, locale)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("パスワードが一致しません")
                    else:
                        st.warning("全ての項目を入力してください")
    
    else:
        # ログイン済み時の表示
        st.subheader("ユーザー情報")
        
        user = st.session_state.user
        
        # プロフィール表示・編集のタブ
        profile_tab1, profile_tab2 = st.tabs(["プロフィール", "設定"])
        
        with profile_tab1:
            # プロフィール情報表示
            with st.container():
                st.markdown(f"""
                <div class="user-info">
                    <p><strong>👤 {user.get('display_name', 'ユーザー')}</strong></p>
                    <p>📧 {user.get('email', '')}</p>
                    <p>🌐 言語: {user.get('locale', 'ja')}</p>
                    <p>📋 プラン: {user.get('current_plan', 'free')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # プロフィール詳細情報を取得ボタン
            if st.button("最新のプロフィール情報を取得", use_container_width=True):
                success, result = get_user_profile()
                if success:
                    st.success("プロフィール情報を更新しました")
                    # セッション状態を更新
                    st.session_state.user.update({
                        "display_name": result["display_name"],
                        "locale": result["locale"],
                        "current_plan": result["current_plan"]
                    })
                    save_session_to_storage(st.session_state.user, st.session_state.access_token)
                    st.rerun()
                else:
                    st.error(result)
        
        with profile_tab2:
            # プロフィール編集フォーム
            st.write("**プロフィール設定**")
            with st.form("profile_update_form"):
                new_display_name = st.text_input(
                    "表示名", 
                    value=user.get('display_name', ''),
                    key="update_display_name"
                )
                new_locale = st.selectbox(
                    "言語", 
                    ["ja", "en"], 
                    index=0 if user.get('locale', 'ja') == 'ja' else 1,
                    key="update_locale"
                )
                new_plan = st.selectbox(
                    "プラン",
                    ["free", "premium", "enterprise"],
                    index=["free", "premium", "enterprise"].index(user.get('current_plan', 'free')),
                    key="update_plan"
                )
                
                update_submit = st.form_submit_button("プロフィール更新", use_container_width=True)
                
                if update_submit:
                    # 変更があった項目のみ更新
                    updates = {}
                    if new_display_name != user.get('display_name', ''):
                        updates['display_name'] = new_display_name
                    if new_locale != user.get('locale', 'ja'):
                        updates['locale'] = new_locale
                    if new_plan != user.get('current_plan', 'free'):
                        updates['current_plan'] = new_plan
                    
                    if updates:
                        success, message = update_user_profile(**updates)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.info("変更がありませんでした")
        
        # ログアウトボタン
        st.divider()
        if st.button("ログアウト", use_container_width=True, type="secondary"):
            success, message = signout_user()
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    st.divider()
    
    # ヘルプ情報
    st.subheader("使用方法")
    st.markdown("""
    1. 学習したい日本語の単語を入力
    2. 目標のJLPTレベルを選択
    3. 「例文を生成」ボタンをクリック
    """)
    
    st.divider()
    st.write("© 2024 JLPT Example Generator")

# メインコンテンツ
st.title("JLPT Example Sentence Generator")

# ログイン状態に応じたメッセージ表示
if st.session_state.user:
    st.write(f"こんにちは、{st.session_state.user.get('display_name', 'ユーザー')}さん！")
    st.write("単語とJLPTレベルを入力すると、例文を生成します。")
else:
    st.write("ログインして例文生成機能をご利用ください。")

# ログイン済みの場合のみ例文生成フォームを表示
if st.session_state.user:
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

else:
    # 未ログイン時のメッセージ
    st.info("サイドバーからログインまたは新規登録を行ってください。")

# フッター情報
st.divider()
if st.session_state.user:
    st.markdown("**使用方法:**")
    st.markdown("1. 学習したい日本語の単語を入力")
    st.markdown("2. 目標のJLPTレベルを選択")
    st.markdown("3. 「例文を生成」ボタンをクリック")
