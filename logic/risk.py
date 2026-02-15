import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class RiskEngine:
    def __init__(self, base_premium: float = 10000.0):
        self.base_premium = base_premium

    def calculate_physics(self, df: pd.DataFrame) -> pd.DataFrame:
        # Berechne physikalische Eigenschaften (Masse, Energie) basierend auf Rohdaten
        data = df.copy()

        # Masse berechnen
        # Annahme: Kugelform und Gesteinsdichte von 2500 kg/m³
        radius_m = (data['avg_diameter'] * 1000) / 2
        volumen_m3 = (4 / 3) * np.pi * (radius_m ** 3)
        data['mass_kg'] = volumen_m3 * 2500

        # Energie berechnen (E = 0.5 * m * v^2)
        data['energy_joule'] = 0.5 * data['mass_kg'] * (data['velocity_km_s'] ** 2)

        # Umrechnung in Terajoule (TJ) für bessere Lesbarkeit
        data['energy_tj'] = data['energy_joule'] / 1e12

        return data

    def evaluate_portfolio(self, df: pd.DataFrame) -> pd.DataFrame:
        # Physikalische Daten anreichern
        df_angereichert = self.calculate_physics(df)

        # Risk Score Berechnung
        # Normalisierung, um extreme Skalenunterschiede auszugleichen
        log_energy = np.log1p(df_angereichert['energy_tj'])
        log_dist = np.log1p(df_angereichert['miss_distance'])

        max_energy = log_energy.max() if log_energy.max() > 0 else 1
        max_dist = log_dist.max() if log_dist.max() > 0 else 1

        norm_energy = log_energy / max_energy
        norm_dist = 1 - (log_dist / max_dist)  # Je näher, desto höher das Risiko

        # Gewichtung: 70% Impact-Energie, 30% Nähe, haben wir selber einfach festgelegt fiktives Beispiel
        df_angereichert['risk_score'] = (0.7 * norm_energy + 0.3 * norm_dist) * 100


        # Policy: Objekte, die von der NASA als 'hazardous' markiert sind, werden abgelehnt.
        df_angereichert['policy_status'] = np.where(
            df_angereichert['hazardous'] == True,
            'ABGELEHNT',
            'GENEHMIGT'
        )


        # Nur genehmigte Objekte erhalten einen Preis,  Hoher Score treibt den Preis
        df_angereichert['premium_eur'] = np.where(
            df_angereichert['policy_status'] == 'GENEHMIGT',
            self.base_premium + (self.base_premium * df_angereichert['risk_score'] * 5),
            0.0
        )

        # Runden für saubere Anzeige im Dashboard
        df_angereichert['risk_score'] = df_angereichert['risk_score'].round(2)
        df_angereichert['premium_eur'] = df_angereichert['premium_eur'].round(2)

        return df_angereichert