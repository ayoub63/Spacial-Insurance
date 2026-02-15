# Autor: Adam Ibrahimkhel

import streamlit as st
import plotly.express as px


def show(df, total_premium, approval_rate, avg_premium, declined_count):
    st.markdown("Finanz-Übersicht")

    # KPI Zeile
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Prämien-Volumen", f"{total_premium:,.0f} €", help="Summe aller potenziellen Einnahmen")
    c2.metric("Genehmigungs-Quote", f"{approval_rate:.1f} %", help="Anteil der versicherbaren Objekte")
    c3.metric("Ø Prämie", f"{avg_premium:,.0f} €", help="Durchschnittspreis pro Police")
    c4.metric("Abgelehnt", f"{declined_count}", delta_color="inverse", help="Zu hohes Risiko (NASA hazardous)")

    st.divider()

    # Charts
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Genehmigungs-Status")
        status_counts = df['policy_status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Anzahl']
        fig_pie = px.pie(
            status_counts,
            values='Anzahl',
            names='Status',
            color='Status',
            color_discrete_map={'GENEHMIGT': 'green', 'ABGELEHNT': 'red'},
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        st.subheader("Prämien-Verteilung")
        # Nur genehmigte anzeigen für das Histogramm
        df_paid = df[df['premium_eur'] > 0]
        if not df_paid.empty:
            fig_hist_prem = px.histogram(
                df_paid,
                x="premium_eur",
                nbins=30,
                title="Verteilung der Policen-Preise",
                labels={'premium_eur': 'Prämie (€)'},
                color_discrete_sequence=['green']
            )
            st.plotly_chart(fig_hist_prem, use_container_width=True)
        else:
            st.info("Keine Prämien-Daten vorhanden.")