# Author: Abuzar  
# data_processor/data_transformer.py

"""
FEATURE 1: Daten-Veredelung (Data Refinement)

Verantwortlich: Abuzar
Aufgabe: Rohdaten bereinigen, normalisieren und für die Datenbank vorbereiten

Transformationen (laut WP_PLAN.pdf):
1. Durchschnitts-Durchmesser berechnen (avg_diameter)
2. Einheiten normieren (km/h → km/s)
3. Duplikate entfernen (gleiche ID)
4. Ungültige Werte filtern (Geschwindigkeit ≈ 0)

Basiert auf dem Restaurant Violations Beispielprojekt des Professors.
"""

import pandas as pd
from typing import Dict, Any
from data_processor.dataframe import Dataframe
from utils.decorators import log_execution, time_execution


class DataTransformer:
    """
    Feature 1: Daten-Veredelung für Space Insurance Analytics.
    
    Diese Klasse ist verantwortlich für:
    - Datenbereinigung (Duplikate, Null-Werte)
    - Einheiten-Normalisierung
    - Berechnung abgeleiteter Werte (avg_diameter)
    
    WICHTIG: Diese Klasse macht NUR Feature 1!
    Risk Score, Premium etc. sind Ayoubs Verantwortung (Feature 2)!
    """
    
    def __init__(self, df: Dataframe, config: Dict[str, Any]) -> None:
        """
        Initialisiert den DataTransformer.
        
        :param df: Dataframe mit Rohdaten
        :param config: Transformations-Konfiguration aus YAML
        """
        self.df = df
        self.config = config
        
        # Lade Konfigurations-Parameter
        self.units = config.get('units', {})
        self.cleaning = config.get('cleaning', {})

    @log_execution
    @time_execution
    def transform(self) -> pd.DataFrame:
        """
        Hauptmethode: Führt alle Transformationen nacheinander aus.
        
        Pipeline (Feature 1):
        1. Datenbereinigung (Duplikate, NULL-Werte)
        2. Durchmesser-Mittelwert berechnen
        3. Einheiten normalisieren
        4. Ungültige Werte filtern
        5. Validierung
        
        :return: Transformierter DataFrame
        """
        print("\n" + "="*70)
        print("  FEATURE 1: DATEN-VEREDELUNG (Abuzar)")
        print("="*70 + "\n")
        
        initial_count = len(self.df.data)
        print(f"Start: {initial_count:,} Objekte\n")
        
        # 1. Datenbereinigung
        self._remove_duplicates()
        self._handle_missing_values()
        
        # 2. Durchmesser-Mittelwert
        self._calculate_avg_diameter()
        
        # 3. Einheiten normalisieren
        self._normalize_units()
        
        # 4. Ungültige Werte filtern
        self._filter_invalid_values()
        
        # 5. Validierung
        self._validate()
        
        final_count = len(self.df.data)
        removed = initial_count - final_count
        
        print("\n" + "="*70)
        print(f"  ✓ FEATURE 1 ABGESCHLOSSEN")
        print(f"  Start: {initial_count:,} | Bereinigt: {final_count:,} | Entfernt: {removed:,}")
        print("="*70 + "\n")
        
        return self.df.data

    def _remove_duplicates(self) -> None:
        """
        Schritt 1: Entfernt Duplikate basierend auf der ID.
        
        Rationale: Manche Objekte kommen mehrfach im Datensatz vor
        (z.B. bei verschiedenen Annäherungen). Wir behalten nur das erste.
        """
        print("→ Entferne Duplikate...")
        
        before = len(self.df.data)
        self.df.data = self.df.data.drop_duplicates(subset=['id'], keep='first')
        after = len(self.df.data)
        removed = before - after
        
        print(f"  ✓ Duplikate entfernt: {removed:,} ({removed/before*100:.1f}%)")

    def _handle_missing_values(self) -> None:
        """
        Schritt 2: Behandelt fehlende Werte in kritischen Spalten.
        
        Strategie:
        - Kritische Spalten (diameter, velocity, distance): Zeile entfernen
        - Nicht-kritische Spalten: Standardwert setzen
        """
        print("→ Behandle fehlende Werte...")
        
        before = len(self.df.data)
        
        # Kritische Spalten: Zeile entfernen wenn NULL
        critical_columns = ['est_diameter_min', 'est_diameter_max', 
                           'relative_velocity', 'miss_distance']
        self.df.data = self.df.data.dropna(subset=critical_columns)
        
        # Boolean-Spalten: Standardwert
        self.df.data['hazardous'] = self.df.data['hazardous'].fillna(False).astype(bool)
        if 'sentry_object' in self.df.data.columns:
            self.df.data['sentry_object'] = self.df.data['sentry_object'].fillna(False).astype(bool)
        
        after = len(self.df.data)
        removed = before - after
        
        print(f"  ✓ Ungültige Werte entfernt: {removed:,}")

    def _calculate_avg_diameter(self) -> None:
        """
        Schritt 3: Berechnet den Durchschnitts-Durchmesser.
        
        Formel: avg_diameter = (est_diameter_min + est_diameter_max) / 2
        
        Rationale: Die NASA gibt Min/Max an, wir brauchen einen Einzelwert
        für die Risikobewertung (die dann Ayoub macht).
        """
        print("→ Berechne Durchschnitts-Durchmesser...")
        
        self.df.data['avg_diameter'] = (
            self.df.data['est_diameter_min'] + self.df.data['est_diameter_max']
        ) / 2
        
        avg = self.df.data['avg_diameter'].mean()
        min_d = self.df.data['avg_diameter'].min()
        max_d = self.df.data['avg_diameter'].max()
        
        print(f"  ✓ avg_diameter erstellt: Ø {avg:.4f} km, Range [{min_d:.4f}, {max_d:.4f}] km")

    def _normalize_units(self) -> None:
        """
        Schritt 4: Normalisiert Einheiten.
        
        Transformationen:
        - relative_velocity: km/h → km/s (÷ 3.6)
        
        Rationale: Einheitliche Einheiten für spätere Berechnungen.
        """
        print("→ Normalisiere Einheiten...")
        
        # Geschwindigkeit: km/h → km/s
        velocity_factor = self.units.get('velocity_to_km_s', 3.6)
        self.df.data['velocity_km_s'] = self.df.data['relative_velocity'] / velocity_factor
        
        avg_vel = self.df.data['velocity_km_s'].mean()
        min_vel = self.df.data['velocity_km_s'].min()
        max_vel = self.df.data['velocity_km_s'].max()
        
        print(f"  ✓ Einheiten normalisiert:")
        print(f"    - Geschwindigkeit: km/h → km/s")
        print(f"    - Ø {avg_vel:.2f} km/s, Range [{min_vel:.2f}, {max_vel:.2f}] km/s")

    def _filter_invalid_values(self) -> None:
        """
        Schritt 5: Filtert ungültige/unrealistische Werte.
        
        Regel aus Config:
        - Geschwindigkeit ≈ 0: Physikalisch unmöglich für NEOs
        - Minimale Distanz: Zu nahe Objekte sind bereits vorbei
        """
        print("→ Filtere ungültige Werte...")
        
        before = len(self.df.data)
        
        # Minimale Geschwindigkeit (aus Config)
        min_velocity = self.cleaning.get('min_velocity', 0.1)
        self.df.data = self.df.data[self.df.data['velocity_km_s'] > min_velocity]
        
        # Minimale Distanz (aus Config)
        min_distance = self.cleaning.get('min_distance', 1000)
        self.df.data = self.df.data[self.df.data['miss_distance'] > min_distance]
        
        after = len(self.df.data)
        removed = before - after
        
        print(f"  ✓ Ungültige Werte gefiltert: {removed:,}")
        print(f"    - Min. Geschwindigkeit: {min_velocity} km/s")
        print(f"    - Min. Entfernung: {min_distance} km")

    def _validate(self) -> None:
        """
        Schritt 6: Validiert die transformierten Daten.
        
        Prüfungen:
        - Neue Spalten existieren
        - Keine NULL-Werte in kritischen Spalten
        - Wertebereiche sind plausibel
        """
        print("→ Validiere Daten...")
        
        required_columns = ['avg_diameter', 'velocity_km_s']
        missing = [col for col in required_columns if col not in self.df.data.columns]
        
        if missing:
            raise ValueError(f"Fehlende Spalten: {missing}")
        
        # Prüfe auf negative Werte
        if (self.df.data['avg_diameter'] < 0).any():
            raise ValueError("Negative Durchmesser gefunden!")
        if (self.df.data['velocity_km_s'] < 0).any():
            raise ValueError("Negative Geschwindigkeiten gefunden!")
        
        print("  ✓ Validierung erfolgreich")
        print(f"  ✓ Finale Datenqualität: {len(self.df.data):,} saubere Objekte")
