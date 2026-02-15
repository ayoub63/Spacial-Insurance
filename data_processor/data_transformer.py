# Autor: Saidabuzar Zaher

import pandas as pd
from data_processor.dataframe import Dataframe


class DataTransformer:
    def __init__(self, df: Dataframe):
        self.df = df

    def transform(self) -> pd.DataFrame:
        """
        - Worst-Case Szenario pro Asteroid behalten (kleinste miss_distance)
        - Durchschnitts-Durchmesser berechnen
        - Geschwindigkeit normieren (km/h → km/s)
        - Datentypen konvertieren
        - Spalten auswählen
        """

        # Wir behalten die gefährlichste Annäherung
        self.df.data = self.df.data.sort_values('miss_distance', ascending=True)

        # Duplikate basierend auf ID entfernen (behalte gefährlichste = erste nach Sortierung)
        self.df.data = self.df.data.drop_duplicates(subset=['id'], keep='first')

        # Durchschnitts-Durchmesser berechnen (Mittelwert aus Min und Max)
        self.df.data['avg_diameter'] = (
        self.df.data['est_diameter_min'] + self.df.data['est_diameter_max']) / 2

        # Geschwindigkeit von km/h in km/s umrechnen (Division durch 3.6)
        self.df.data['velocity_km_s'] = self.df.data['relative_velocity'] / 3.6

        # Datentypen explizit konvertieren
        self.df.data['id'] = self.df.data['id'].astype(int)
        self.df.data['avg_diameter'] = self.df.data['avg_diameter'].astype(float)
        self.df.data['velocity_km_s'] = self.df.data['velocity_km_s'].astype(float)
        self.df.data['miss_distance'] = self.df.data['miss_distance'].astype(float)

        # Nur die relevanten Spalten auswählen
        columns_to_keep = [
            'id', 'name', 'est_diameter_min', 'est_diameter_max', 'avg_diameter',
            'relative_velocity', 'velocity_km_s', 'miss_distance',
            'orbiting_body', 'absolute_magnitude', 'hazardous'
        ]


        self.df.data = self.df.data[columns_to_keep]

        return self.df.data