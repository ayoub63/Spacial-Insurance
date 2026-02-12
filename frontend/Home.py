import streamlit as st
from queries import query_df
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

df_count = query_df("SELECT COUNT(*) AS total_objects FROM space_objects;")

total = df_count["total_objects"][0]

st.metric("Total objects", total)

df_cols = query_df("PRAGMA table_info(space_objects);")
st.write(df_cols)




st.title("Spacial-Insurance Dashboard")
st.markdown("""
Willkommen zum **mehrseitigen Analyse-Dashboard**.

Nutze die Navigation links, um:
- eine Übersicht zu sehen
""")