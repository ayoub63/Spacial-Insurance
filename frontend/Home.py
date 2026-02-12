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
base_premium = st.sidebar.number_input("Basis-Prämie in Euro", 0, 100000, 1000)

st.write("Aktuelle Einstellungen: ")
st.write("Toleranz: ", tolerance)
st.write("Basis Prämie: ", base_premium)


col1, col2, col3, col4 = st.columns(4)

col1.metric("Durchschn. Risk Score", "Platzhalter")
col2.metric("Max. Risk Score", "platzhalter")
col3.metric("Objekte > Toleranz", "platzhalter")
col4.metric("Premien Summe (€)", "platzhalter")
