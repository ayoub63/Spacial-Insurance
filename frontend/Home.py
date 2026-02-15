# Author: Adam Ibrahimkhel & Ayoub (Refactored with Views)

import streamlit as st
import pandas as pd
import sys
import os

# --- PFAD-SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from frontend.db import get_db
from logic.risk import RiskEngine

# --- VIEWS IMPORTIEREN ---
from views import business_view, risk_view, data_view

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SpaceGuard Dashboard",
    layout="wide"
)


st.sidebar.title("⚙Einstellungen")
tolerance = st.sidebar.slider("Max. Risiko-Toleranz", 0, 100, 80)
base_premium = st.sidebar.number_input("Basis-Prämie (€)", 1000, 1000000, 10000, step=1000)

st.sidebar.markdown("---")
st.sidebar.info(f"**Aktueller Status:**\nToleranz: {tolerance}\nBasis: {base_premium:,.0f} €")

st.title("SpaceGuard Insurance Dashboard")
st.markdown("Automatisierte Risiko-Bewertung für Near-Earth Objects (NEOs)")

# --- DATEN LADEN ---
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
    st.error("Keine Daten gefunden. Bitte 'etl.py' ausführen!")
    st.stop()

# --- LOGIK AUSFÜHREN ---
engine = RiskEngine(base_premium=base_premium)
df_enriched = engine.evaluate_portfolio(df_raw)
df_enriched['impact'] = df_enriched['energy_tj'] # Mapping für Views

# --- KPI BERECHNUNG (Zentral im Controller) ---
# Business KPIs
total_premium = df_enriched['premium_eur'].sum()
total_objects = len(df_enriched)
declined_count = len(df_enriched[df_enriched['policy_status'] == 'ABGELEHNT'])
approved_count = total_objects - declined_count
approval_rate = (approved_count / total_objects * 100) if total_objects > 0 else 0
avg_premium = df_enriched[df_enriched['premium_eur'] > 0]['premium_eur'].mean() if approved_count > 0 else 0

# Risk KPIs
avg_risk = df_enriched['risk_score'].mean()
max_risk = df_enriched['risk_score'].max()
critical_objects = len(df_enriched[df_enriched['risk_score'] > tolerance])
max_impact = df_enriched['impact'].max()

# --- TABS & VIEWS AUFRUFEN ---
tab_biz, tab_risk, tab_data = st.tabs(["Business & Finanzen", "Risiko & Physik", "Daten-Explorer"])

with tab_biz:
    business_view.show(df_enriched, total_premium, approval_rate, avg_premium, declined_count)

with tab_risk:
    risk_view.show(df_enriched, avg_risk, max_risk, critical_objects, max_impact, tolerance)

with tab_data:
    data_view.show(df_enriched)