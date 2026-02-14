# Autor: Ayoub

"""
FEATURE 2: Risk Engine (Deterministic)
Logik-Schicht für Space Insurance ohne ML.
"""

import pandas as pd
import numpy as np
import logging

from utils.decorators import log_execution, time_execution

# Logger für dieses Modul
logger = logging.getLogger(__name__)

class RiskEngine:
    """
    Kern-Logik (Regelbasiert):
    Berechnet physikalische Eigenschaften (Masse, Energie)
    Prüft NASA-Flag 'hazardous' als Ausschlusskriterium
    Berechnet Versicherungsprämien für den Rest
    """

    def __init__(self, base_premium: float = 10000.0):
        """
        :param base_premium: Startpreis für die ungefährlichste Police.
        """
        self.base_premium = base_premium

    @log_execution
    def calculate_physics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formeln:
        - Masse = Volumen * Dichte (Annahme: Gestein ~2500 kg/m³)
        - Energie = 0.5 * Masse * Geschwindigkeit²
        """
        data = df.copy()

        # Radius in Metern berechnen
        radius_m = (data['avg_diameter'] * 1000) / 2

        # Volumen einer Kugel (4/3 * pi * r³)
        volumen_m3 = (4/3) * np.pi * (radius_m ** 3)

        # Masse in kg (Dichte ca. 2500 kg/m³ für Asteroiden)
        data['mass_kg'] = volumen_m3 * 2500

        # Kinetische Energie in Joule (E = 0.5 * m * v²)
        data['energy_joule'] = 0.5 * data['mass_kg'] * (data['velocity_km_s'] ** 2)

        # Umrechnung in Terajoule (TJ) für lesbare Zahlen (1 TJ = 10^12 J)
        data['energy_tj'] = data['energy_joule'] / 1e12

        return data

    @log_execution
    @time_execution
    def evaluate_portfolio(self, df: pd.DataFrame) -> pd.DataFrame:
        # Physik berechnen
        enriched_df = self.calculate_physics(df)

        # Risk Score Berechnung (0 - 100)
        # Auch abgelehnte Objekte bekommen einen Score

        # Logarithmus, um extreme Unterschiede bei Energie zu glätten
        log_energy = np.log1p(enriched_df['energy_tj'])
        log_dist = np.log1p(enriched_df['miss_distance'])

        # Normalisierung
        norm_energy = log_energy / log_energy.max()
        # Bei Distanz: 1 - Wert, weil kleine Distanz = hohes Risiko
        norm_dist = 1 - (log_dist / log_dist.max())

        # Gewichtung: 70% Energie (Zerstörungskraft), 30% Wahrscheinlichkeit (Nähe),
        # haben wir einfach so festgelegt fiktiv
        enriched_df['risk_score'] = (0.7 * norm_energy + 0.3 * norm_dist) * 100

        # Policy Status
        # Logik: Wir vertrauen der NASA. Wenn 'hazardous' == True -> ABGELEHNT.
        enriched_df['policy_status'] = np.where(
            enriched_df['hazardous'] == True,
            'ABGELEHNT',
            'GENEHMIGT'
        )

        # Pricing
        # Preis berechnen (Basispreis + Faktor * Risk Score)
        # Nur für genehmigte Asteroiden, sonst 0
        enriched_df['premium_eur'] = np.where(
            enriched_df['policy_status'] == 'APPROVED',
            self.base_premium + (self.base_premium * enriched_df['risk_score'] * 5),
            0.0
        )