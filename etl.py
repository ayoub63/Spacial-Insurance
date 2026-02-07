# Author: Abuzar
# etl.py

"""
Space Insurance ETL Pipeline - Feature 1

Team:
- Abuzar: ETL & Feature 1 (Daten-Veredelung)
- Ayoub: Feature 2 (Risk Calculator & Pricing)
- Adam: Dashboard (Frontend)

Dieser Script macht NUR Feature 1 (Abuzars Verantwortung):
- CSV laden
- Daten bereinigen
- avg_diameter berechnen
- Einheiten normalisieren
- In PostgreSQL laden

Basiert auf dem Restaurant Violations Beispielprojekt des Professors.
"""

import sys
import os

# Füge Projekt-Root zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config_loader import ConfigLoader
from data_processor.dataframe import Dataframe
from data_processor.data_transformer import DataTransformer
from data_processor.postgres_database import PostgresDatabase


def print_header():
    """Gibt den Header aus."""
    print("\n" + "="*70)
    print("  🛰️  SPACE INSURANCE ETL - FEATURE 1")
    print("  Daten-Veredelung (Data Refinement)")
    print("="*70)
    print("\n  Verantwortlich: Abuzar")
    print("  Aufgabe: CSV → Bereinigung → PostgreSQL")
    print("="*70 + "\n")


def print_footer(stats: dict):
    """Gibt die Zusammenfassung aus."""
    print("\n" + "="*70)
    print("  ✅  FEATURE 1 ERFOLGREICH ABGESCHLOSSEN")
    print("="*70)
    print("\n📊 ERGEBNISSE:")
    print(f"  - Objekte in Datenbank: {stats['total_objects']:,}")
    print(f"  - Ø Durchmesser: {stats['avg_diameter']} km")
    print(f"  - Ø Geschwindigkeit: {stats['avg_velocity']} km/s")
    print(f"  - Hazardous Objekte: {stats['hazardous_count']:,}")
    print("\n✅ Daten bereit für Feature 2 (Ayoub)!")
    print("\n💡 Nächste Schritte:")
    print("   1. Ayoub: Risk Calculator implementieren")
    print("   2. Adam: Dashboard entwickeln")
    print("="*70 + "\n")


def main():
    """
    Hauptfunktion: Koordiniert Feature 1 (ETL).
    
    Pipeline:
    1. Konfiguration laden
    2. CSV-Daten extrahieren
    3. Daten transformieren (Feature 1)
    4. In PostgreSQL laden
    """
    
    print_header()
    
    try:
        # ====================================================================
        # SCHRITT 1: Konfiguration laden
        # ====================================================================
        print("[SCHRITT 1] Lade Konfiguration...")
        yaml_path = "config/space_insurance_config.yaml"
        
        if not os.path.exists(yaml_path):
            print(f"✗ FEHLER: Config nicht gefunden: {yaml_path}")
            sys.exit(1)
        
        config_loader = ConfigLoader(yaml_path)
        print("✓ Konfiguration geladen\n")
        
        # ====================================================================
        # SCHRITT 2: CSV-Daten extrahieren
        # ====================================================================
        print("[SCHRITT 2] EXTRACT - Lade CSV-Daten...")
        paths_config = config_loader.get_paths_config()
        csv_path = paths_config.get('csv_raw')
        
        if not os.path.exists(csv_path):
            print(f"✗ FEHLER: CSV nicht gefunden: {csv_path}")
            print(f"💡 TIPP: Lege neo.csv in {csv_path}")
            sys.exit(1)
        
        df = Dataframe(csv_path)
        df.load_data()
        
        # ====================================================================
        # SCHRITT 3: Daten transformieren (Feature 1)
        # ====================================================================
        print("\n[SCHRITT 3] TRANSFORM - Feature 1 (Abuzar)...")
        transformations_config = config_loader.get_transformations_config()
        transformer = DataTransformer(df, transformations_config)
        transformed_data = transformer.transform()
        
        # ====================================================================
        # SCHRITT 4: In PostgreSQL laden
        # ====================================================================
        print("[SCHRITT 4] LOAD - Lade in PostgreSQL...")
        
        db_config = config_loader.get_database_config()
        queries = config_loader.get_queries()
        
        with PostgresDatabase(db_config) as db:
            # Tabelle erstellen
            db.create_table(queries['create_table'])
            
            # Indizes erstellen
            db.create_indexes(queries['create_indexes'])
            
            # Daten einfügen
            db.insert_data(transformed_data, queries['insert_data'])
            
            # Statistiken holen
            stats = db.get_statistics()
        
        # ====================================================================
        # ERFOLG!
        # ====================================================================
        print_footer(stats)
        
    except KeyboardInterrupt:
        print("\n\n✗ ETL abgebrochen durch Benutzer")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
