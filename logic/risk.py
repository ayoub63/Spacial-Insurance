# Autor: Ayoub

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class RiskEngine:
    def __init__(self, base_premium: float = 10000.0):
        self.base_premium = base_premium

    # KEIN @log_execution
    def calculate_physics(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()

        # Berechnung
        radius_m = (data['avg_diameter'] * 1000) / 2
        volumen_m3 = (4 / 3) * np.pi * (radius_m ** 3)
        data['mass_kg'] = volumen_m3 * 2500
        data['energy_joule'] = 0.5 * data['mass_kg'] * (data['velocity_km_s'] ** 2)
        data['energy_tj'] = data['energy_joule'] / 1e12

        return data

    # KEIN @log_execution
    # KEIN @time_execution
    def evaluate_portfolio(self, df: pd.DataFrame) -> pd.DataFrame:
        # 1. Physik
        enriched_df = self.calculate_physics(df)

        # 2. Risk Score
        log_energy = np.log1p(enriched_df['energy_tj'])
        log_dist = np.log1p(enriched_df['miss_distance'])

        max_energy = log_energy.max() if log_energy.max() > 0 else 1
        max_dist = log_dist.max() if log_dist.max() > 0 else 1

        norm_energy = log_energy / max_energy
        norm_dist = 1 - (log_dist / max_dist)

        enriched_df['risk_score'] = (0.7 * norm_energy + 0.3 * norm_dist) * 100

        # 3. Status (DEUTSCH - passend zu deinem Dashboard Home.py)
        enriched_df['policy_status'] = np.where(
            enriched_df['hazardous'] == True,
            'ABGELEHNT',
            'GENEHMIGT'
        )

        # 4. Pricing
        enriched_df['premium_eur'] = np.where(
            enriched_df['policy_status'] == 'GENEHMIGT',
            self.base_premium + (self.base_premium * enriched_df['risk_score'] * 5),
            0.0
        )

        enriched_df['risk_score'] = enriched_df['risk_score'].round(2)
        enriched_df['premium_eur'] = enriched_df['premium_eur'].round(2)

        return enriched_df