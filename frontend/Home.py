import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data_src/processed/space_insurance.db")

tabelle = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn)

anzahlZeilen = pd.read_sql(
    "SELECT COUNT(*) FROM space_objects",
    conn

)

st.set_page_config(
    page_title="Spacial-Insurance",
    layout="wide"
)

st.dataframe(tabelle)
st.dataframe(anzahlZeilen)


st.title("Spacial-Insurance Dashboard")
st.markdown("""
Willkommen zum **mehrseitigen Analyse-Dashboard**.

Nutze die Navigation links, um:
- eine Übersicht zu sehen
""")