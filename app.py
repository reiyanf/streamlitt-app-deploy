from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み（ローカル用）
load_dotenv()

# OpenAI APIキー取得
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# APIキーの先頭だけ安全にログ出力
if openai_api_key:
    st.write(f"✅ OPENAI_API_KEY Loaded: {openai_api_key[:4]}***")
else:
    st.error("❌ OPENAI_API_KEY が設定されていません。")

st.title("21-6アプリ")
st.write("##### 以下の専門家に対し相談可能です")

selected_item = st.radio(
    "専門家：",
    ["食事", "運動"]
)

st.divider()

input_message = st.text_input(label="相談内容を入力してください。")

if st.button("実行"):
    st.divider()

    if not input_message:
        st.error("相談内容を入力してから「実行」ボタンを押してください。")
    else:
        # ChatOpenAI を初期化（APIキーを明示的に渡す）
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            api_key=openai_api_key
        )

        if selected_item == "食事":
            system_prompt = "あなたは食事の専門家です。"
        else:
            system_prompt = "あなたは運動の専門家です。"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=input_message),
        ]

        try:
            result = llm(messages)
            st.write(result.content)
        except Exception as e:
            # エラー内のAPIキーは伏字化
            safe_error = str(e).replace(openai_api_key, "****")
            st.error(f"エラーが発生しました: {safe_error}")