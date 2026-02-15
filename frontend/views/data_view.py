# Autor: Adam Ibrahimkhel
import streamlit as st


def show(df):
    st.markdown("### Top 10 Gefährlichste Objekte")

    df_top10 = df.sort_values(by="risk_score", ascending=False).head(10)

    cols_top10 = ['name', 'risk_score', 'premium_eur', 'policy_status', 'miss_distance', 'impact', 'velocity_km_s']

    st.dataframe(
        df_top10[cols_top10].style.format({
            "risk_score": "{:.2f}",
            "premium_eur": "{:,.2f} €",
            "miss_distance": "{:,.0f}",
            "impact": "{:.4f}",
            "velocity_km_s": "{:.2f}"
        }),
        use_container_width=True
    )

    st.divider()

    st.markdown("Objekt-Überblick")
    st.caption(
        "Alle Objekte aufgelistet")


    all_cols = [
        'name', 'risk_score', 'premium_eur', 'policy_status',
        'avg_diameter', 'miss_distance', 'velocity_km_s',
        'impact', 'hazardous'
    ]


    if 'hazard_class' in df.columns:
        all_cols.insert(4, 'hazard_class')

    valid_cols = [c for c in all_cols if c in df.columns]

    st.dataframe(
        df[valid_cols].style.format({
            "risk_score": "{:.2f}",
            "premium_eur": "{:,.2f} €",
            "avg_diameter": "{:.3f} km",
            "miss_distance": "{:,.0f} km",
            "velocity_km_s": "{:.2f} km/s",
            "impact": "{:.4f} TJ"
        }),
        use_container_width=True,
        height=600
    )

    st.caption(f"Gesamtanzahl Datensätze: {len(df)}")