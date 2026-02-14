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