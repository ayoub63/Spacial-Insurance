# Author: Saidabuzar Zaher

"""
FEATURE 1: Daten-Veredelung (Data Refinement)
"""

import pandas as pd
from data_processor.dataframe import Dataframe


class DataTransformer:
    def __init__(self, df: Dataframe):
        """
        Initialisiert den DataTransformer.
        :param df: DataFrame mit den zu transformierenden Daten
        """
        self.df = df

    def transform(self) -> pd.DataFrame:
        """
        Transformiert die Daten:
        - Worst-Case Szenario pro Asteroid behalten (kleinste miss_distance)
        - Fehlende Werte behandeln
        - Durchschnitts-Durchmesser berechnen
        - Geschwindigkeit normieren (km/h → km/s)
        - Datentypen konvertieren
        - Ungültige Werte filtern
        - Spalten auswählen
        :return: Transformierter DataFrame
        """
        # Sortiere nach miss_distance (kleinste = gefährlichste zuerst)
        # Rationale: Gleicher Asteroid wurde mehrfach beobachtet mit verschiedenen Entfernungen
        # Wir behalten die gefährlichste Annäherung (Worst Case)
        self.df.data = self.df.data.sort_values('miss_distance', ascending=True)

        # Duplikate basierend auf ID entfernen (behalte gefährlichste = erste nach Sortierung)
        self.df.data = self.df.data.drop_duplicates(subset=['id'], keep='first')

        # Fehlende Werte in kritischen numerischen Spalten entfernen
        self.df.data = self.df.data.dropna(subset=['est_diameter_min', 'est_diameter_max'])
        self.df.data = self.df.data.dropna(subset=['relative_velocity', 'miss_distance'])

        # Fehlende Werte in optionalen Spalten mit Standardwerten füllen
        if 'orbiting_body' in self.df.data.columns:
            self.df.data['orbiting_body'] = self.df.data['orbiting_body'].fillna('Earth')

        if 'absolute_magnitude' in self.df.data.columns:
            self.df.data['absolute_magnitude'] = self.df.data['absolute_magnitude'].fillna(0.0)

        # Boolean-Spalten mit False als Standardwert füllen
        self.df.data['hazardous'] = self.df.data['hazardous'].fillna(False).astype(bool)

        if 'sentry_object' in self.df.data.columns:
            self.df.data['sentry_object'] = self.df.data['sentry_object'].fillna(False).astype(bool)

        # Durchschnitts-Durchmesser berechnen (Mittelwert aus Min und Max)
        self.df.data['avg_diameter'] = (
                                               self.df.data['est_diameter_min'] + self.df.data['est_diameter_max']
                                       ) / 2

        # Geschwindigkeit von km/h in km/s umrechnen (Division durch 3.6)
        self.df.data['velocity_km_s'] = self.df.data['relative_velocity'] / 3.6

        # Datentypen explizit konvertieren
        self.df.data['id'] = self.df.data['id'].astype(int)
        self.df.data['avg_diameter'] = self.df.data['avg_diameter'].astype(float)
        self.df.data['velocity_km_s'] = self.df.data['velocity_km_s'].astype(float)
        self.df.data['miss_distance'] = self.df.data['miss_distance'].astype(float)

        # Ungültige Werte filtern: Geschwindigkeit muss größer als 0.1 km/s sein
        self.df.data = self.df.data[self.df.data['velocity_km_s'] > 0.1]

        # Ungültige Werte filtern: Entfernung muss größer als 1000 km sein
        self.df.data = self.df.data[self.df.data['miss_distance'] > 1000]

        # Ungültige Werte filtern: Durchmesser muss positiv sein
        self.df.data = self.df.data[self.df.data['avg_diameter'] > 0]

        # Nur die relevanten Spalten auswählen
        columns_to_keep = [
            'id', 'name', 'est_diameter_min', 'est_diameter_max', 'avg_diameter',
            'relative_velocity', 'velocity_km_s', 'miss_distance',
            'orbiting_body', 'absolute_magnitude', 'hazardous'
        ]

        # Sentry_object nur hinzufügen wenn vorhanden
        if 'sentry_object' in self.df.data.columns:
            columns_to_keep.append('sentry_object')

        self.df.data = self.df.data[columns_to_keep]

        return self.df.data