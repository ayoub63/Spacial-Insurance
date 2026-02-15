# Author: Adam Ibrahimkhel

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Pfad-Fix
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from frontend.db import get_db
# WICHTIG: Importiert aus risk.py
from logic.risk import RiskEngine

st.set_page_config(page_title="SpaceGuard Dashboard", layout="wide")

st.title("SpaceGuard Dashboard (Lowkirk)")

# Einstellungen
st.sidebar.header("Einstellungen")
base_premium = st.sidebar.number_input("Basis-Prämie (€)", value=10000)
risk_tolerance = st.sidebar.slider("Toleranz", 0, 100, 80)

# Daten laden
@st.cache_data
def load_data():
    conn = get_db()
    try:
        query = "SELECT * FROM space_objects"
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()

df_raw = load_data()

if df_raw.empty:
    st.error("Datenbank ist leer. Führe 'etl.py' aus!")
    st.stop()

#LOGIK
try:
    engine = RiskEngine(base_premium=base_premium)
    df_enriched = engine.evaluate_portfolio(df_raw)
except Exception as e:
    st.error(f"Fehler in der RiskEngine: {e}")
    st.stop()

# --- DEBUGGING CHECK ---
if df_enriched is None:
    st.error(" Fehler: RiskEngine hat 'None' zurückgegeben! Prüfe logic/risk.py")
    st.stop()
else:
    st.success(f" Erfolg! {len(df_enriched)} Datenpunkte berechnet")

# --- DASHBOARD ---
total_premium = df_enriched['premium_eur'].sum()
avg_risk = df_enriched['risk_score'].mean()
crit_count = len(df_enriched[df_enriched['risk_score'] > risk_tolerance])
declined_count = len(df_enriched[df_enriched['policy_status'] == 'ABGELEHNT'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Volumen", f"{total_premium:,.0f} €")
c2.metric("Ø Risk", f"{avg_risk:.2f}")
c3.metric("Kritisch", f"{crit_count}")
c4.metric("Abgelehnt", f"{declined_count}")

# Tabelle anzeigen
st.dataframe(df_enriched.head(50))