import streamlit as st
import plotly.express as px


def show(df, avg_risk, max_risk, critical_objects, max_impact, tolerance):
    """
    Zeigt den Risiko & Physik Tab an.
    """
    st.markdown("### ☄️ Risiko-Analyse")

    # KPI Zeile
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Ø Risk Score", f"{avg_risk:.2f}")
    k2.metric("Max. Risk Score", f"{max_risk:.2f}")
    k3.metric("🚨 Kritische Objekte", f"{critical_objects}", help=f"Score > {tolerance}")
    k4.metric("💥 Max. Impact (TJ)", f"{max_impact:.4f}", help="Maximale Kinetische Energie")

    st.divider()

    # Risk Radar
    st.subheader("🌍 Risk Radar: Distanz vs. Impact")
    st.caption("Logarithmische Skala zur besseren Sichtbarkeit von Extremwerten.")

    fig_radar = px.scatter(
        df,
        x="miss_distance",
        y="impact",
        size="avg_diameter",
        color="risk_score",
        hover_name="name",
        log_x=True,  # Log Skala
        log_y=True,  # Log Skala
        color_continuous_scale="RdYlGn_r",  # Rot = Hoch
        labels={
            "miss_distance": "Distanz zur Erde (km)",
            "impact": "Impact Energie (TJ)",
            "risk_score": "Risiko Score",
            "avg_diameter": "Durchmesser"
        }
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Risk Verteilung
    st.subheader("Verteilung der Risikoscores")
    fig_hist_risk = px.histogram(
        df,
        x="risk_score",
        nbins=40,
        color_discrete_sequence=['#3366cc']
    )
    # Rote Linie für Toleranz
    fig_hist_risk.add_vline(x=tolerance, line_dash="dash", line_color="red", annotation_text="Limit")
    st.plotly_chart(fig_hist_risk, use_container_width=True)