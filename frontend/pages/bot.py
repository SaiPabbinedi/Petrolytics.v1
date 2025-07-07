import os
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Chatbot",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto",
)

hide_buttons_css = '''
<style>
button[data-testid="stDeployButton"],
button[data-testid="stSettingsButton"],
button[data-testid="stOptionButton"],
button[data-testid="stBaseButton-header"] { display: none; }
</style>
'''
st.markdown(hide_buttons_css, unsafe_allow_html=True)

st.title("✨ Gemini Chatbot")

FASTAPI_URL = os.getenv("API_URL", "http://127.0.0.1:8000") + "/chat/"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello there! How can I assist you today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

uploaded_file = None
csv_preview = ""

uploaded_files = st.session_state.get("uploaded_files_list", [])
if uploaded_files and isinstance(uploaded_files, list):
    uploaded_file = uploaded_files[0]

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
        csv_preview = df.head(15).to_markdown(index=False)
    except Exception as e:
        csv_preview = f"⚠️ Error reading file: {e}"

if prompt := st.chat_input("What would you like to ask?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "@Session" in prompt and csv_preview:
        combined_prompt = prompt.replace("@Session", csv_preview)
    else:
        combined_prompt = prompt

    with st.chat_message("user"):
        st.markdown(prompt)
        if "@Session" in prompt:
            if csv_preview:
                st.markdown("📊 CSV Preview (First 15 Rows):")
                st.markdown(csv_preview)
            else:
                st.markdown("⚠️ No readable CSV file found.")

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            res = requests.post(
                FASTAPI_URL,
                json={"text": combined_prompt},
                timeout=120
            )
            res.raise_for_status()
            answer = res.json().get("response", "❗️ No response text returned.")
        except Exception as e:
            answer = f"**Error:** {e}"
        placeholder.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
