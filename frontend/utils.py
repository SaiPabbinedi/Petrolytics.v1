import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    try:
        uploaded_file.seek(0)
        size = uploaded_file.size if hasattr(uploaded_file, 'size') else None
        if size == 0:
            st.error(f"The file {uploaded_file.name} is empty.")
            return None
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.warning(f"The file {uploaded_file.name} loaded but has no data.")
        return df
    except pd.errors.EmptyDataError:
        st.error(f"File {uploaded_file.name} is empty or has no columns.")
        return None
    except pd.errors.ParserError as e:
        st.error(f"Parsing error in {uploaded_file.name}: {e}")
        return None
    except Exception as e:
        st.error(f"Error loading {uploaded_file.name}: {e}")
        return None