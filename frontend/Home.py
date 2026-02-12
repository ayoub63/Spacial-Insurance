import streamlit as st
from queries import query_df
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

st.title("Spacial-Insurance Dashboard")

st.sidebar.title("Einstellungen")
tolerance = st.sidebar.slider("Max Risk Tolerance", 0, 100, 80)
base_premium = st.sidebar.slider("Basis-Prämie in Euro", 0, 100000, 1000)

st.write("Aktuelle Einstellungen: ")
st.write("Tolerance: ", tolerance)
st.write("Base premium: ", base_premium)