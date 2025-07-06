import streamlit as st

st.set_page_config(page_title="Petrolytics", layout="wide")

pages = {
    "Resources": [
        st.Page("pages/dashboard.py", title="Dashboard"),
    ],
    "Menu": [
        st.Page("pages/analysis.py", title="Analysis"),
        st.Page("pages/bot.py", title="Chatbot"),
    ],
}

pg = st.navigation(pages, position="top")
pg.run()