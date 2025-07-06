import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

from utils import load_data
from report import generate_reportlab_pdf

st.set_page_config(
    page_title="Analytics",
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

loaded_dfs_dict = {}
generated_chart_images = {}

st.title("Data Analysis & Revenue Optimization")

if "uploaded_files_list" not in st.session_state:
    st.session_state["uploaded_files_list"] = []
if "analysis_mode" not in st.session_state:
    st.session_state["analysis_mode"] = False

uploaded_files = st.file_uploader(
    "Upload your CSV or Excel files for analysis",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    key="analysis_file_uploader"
)

if uploaded_files:
    st.session_state["uploaded_files_list"] = uploaded_files
    st.success(f"Uploaded {len(uploaded_files)} file(s).")

if st.session_state["uploaded_files_list"]:
    st.subheader("Preview of Uploaded Data")
    for uploaded_file in st.session_state["uploaded_files_list"]:
        with st.expander(f"Preview: {uploaded_file.name}"):
            df = load_data(uploaded_file)
            if df is not None:
                st.dataframe(df.head())
            else:
                st.warning(f"Could not load {uploaded_file.name}")

    if st.button("Analyze Data and Generate Charts"):
        st.session_state["analysis_mode"] = True

if st.session_state["analysis_mode"]:
    st.markdown("---")
    st.subheader("Analysis & Chart Generation")

    for uploaded_file in st.session_state["uploaded_files_list"]:
        st.write(f"### Processing: {uploaded_file.name}")
        df = load_data(uploaded_file)

        if df is None or df.empty:
            st.warning(f"Skipping {uploaded_file.name} due to empty data.")
            continue

        cols = df.columns.tolist()
        if len(cols) >= 2:
            x = st.selectbox(f"Select X-axis ({uploaded_file.name})", cols, key=f"x_{uploaded_file.name}")
            y = st.selectbox(f"Select Y-axis ({uploaded_file.name})", cols, key=f"y_{uploaded_file.name}")
            chart_type = st.selectbox(
                f"Chart type ({uploaded_file.name})",
                ["Line", "Bar", "Area"],
                key=f"chart_{uploaded_file.name}"
            )

            if chart_type == "Line":
                st.line_chart(df, x=x, y=y)
            elif chart_type == "Bar":
                st.bar_chart(df, x=x, y=y)
            else:
                st.area_chart(df, x=x, y=y)

            fig, ax = plt.subplots(figsize=(8, 4))
            if chart_type == "Line":
                ax.plot(df[x], df[y])
            elif chart_type == "Bar":
                ax.bar(df[x], df[y])
            else:
                ax.fill_between(df[x], df[y], alpha=0.5)
                ax.plot(df[x], df[y], color="blue")
            ax.set(xlabel=x, ylabel=y, title=f"{chart_type} of {y} vs {x}")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            plt.close(fig)
            generated_chart_images[f"{chart_type} ({y} vs {x}) for {uploaded_file.name}"] = buf

        loaded_dfs_dict[uploaded_file.name] = df
        st.markdown("---")

    if loaded_dfs_dict or generated_chart_images:
        if st.button("Download PDF Report"):
            with st.spinner("Generating PDF report..."):
                pdf = generate_reportlab_pdf(loaded_dfs_dict, generated_chart_images)
                st.download_button("Download PDF", pdf, "analysis_report.pdf", "application/pdf")
            st.success("PDF created successfully!")
    else:
        st.info("No charts generated to include in PDF.")
else:
    st.info("Upload files to start analysis.")
