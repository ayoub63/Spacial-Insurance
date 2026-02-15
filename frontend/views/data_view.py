import streamlit as st


def show(df):
    st.markdown("Top 10 Gefährlichste Objekte")

    # Top 10 Tabelle sortiert nach Risiko
    df_top10 = df.sort_values(by="risk_score", ascending=False).head(10)

    # Relevante Spalten auswählen
    cols_to_show = ['name', 'risk_score', 'premium_eur', 'policy_status', 'miss_distance', 'impact', 'velocity_km_s']

    st.dataframe(
        df_top10[cols_to_show].style.format({
            "risk_score": "{:.2f}",
            "premium_eur": "{:,.2f} €",
            "miss_distance": "{:,.0f}",
            "impact": "{:.4f}",
            "velocity_km_s": "{:.2f}"
        }),
        use_container_width=True
    )

    st.caption(f"Gesamtanzahl analysierter Objekte: {len(df)}")