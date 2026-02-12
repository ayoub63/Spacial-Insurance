import streamlit as st
from queries import query_df
import pandas as pd
import plotly as pl
from queries import query_df, has_column


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

table = "space_objects"

st.subheader("Risk Score Verteilung")

if has_column(table, "risk_score"):
    df = query_df(f"SELECT risk_score FROM {table} WHERE risk_score IS NOT NULL;")
    his = pl.histogram(df, x="risk_score", nbins=20)
    st.plotly_chart(his, use_container_width=True)
else:
    st.info("risk_score noch nicht vorhanden")


st.subheader("Impact vs Distanz (Risk Radar)")

has_impact = has_column("space_objects", "impact")
has_distance = has_column("space_objects", "miss_distance")

if has_impact and has_distance:
    df_scatter = query_df("""
        SELECT miss_distance, impact
        FROM space_objects
        WHERE miss_distance IS NOT NULL
          AND impact IS NOT NULL;
    """)

    sc = pl.scatter(df_scatter, x="miss_distance", y="impact")
    st.plotly_chart(sc, use_container_width=True)

else:
    st.info("warte auf impact spalte")



st.subheader("Top 10 Risiko Objekte")

if has_column("space_objects", "risk_score"):
    df_top10 = query_df("""
        SELECT name, risk_score, miss_distance, velocity_km_s, avg_diameter
        FROM space_objects
        WHERE risk_score IS NOT NULL
        ORDER BY risk_score DESC
        LIMIT 10;
    """)
    st.dataframe(df_top10, use_container_width=True)
else:
    st.info("risk score fehlt")


st.subheader("Impact Breakdown")

if has_column("space_objects", "impact"):
    df_impact = query_df("""
        SELECT impact
        FROM space_objects
        WHERE impact IS NOT NULL;
    """)
    bdimpact = pl.histogram(df_impact, x="impact", nbins=30)
    st.plotly_chart(bdimpact, use_container_width=True)
else:
    st.info("Impact fehlt")


