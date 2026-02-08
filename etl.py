# Author: Abuzar
# etl.py

"""
Space Insurance ETL Pipeline - Feature 1
Team: Abuzar (ETL), Ayoub (Risk), Adam (Dashboard)
"""

import sys
import os

from utils.config_loader import ConfigLoader
from data_processor.dataframe import Dataframe
from data_processor.data_transformer import DataTransformer
from data_processor.sqlite_database import SqliteDatabase


def main():
    """
    Hauptfunktion: Koordiniert Feature 1 (ETL).
    Pipeline: CSV laden → Transformieren → In SQLite laden
    """

    try:
        # Konfiguration laden
        config_loader = ConfigLoader("config/space_insurance_config.yaml")

        # CSV laden
        csv_path = config_loader.get_csv_path()
        if not os.path.exists(csv_path):
            print(f"Fehler: CSV nicht gefunden: {csv_path}")
            sys.exit(1)

        df = Dataframe(csv_path)
        df.load_data()
        print(f"CSV geladen: {len(df.data)} Zeilen")

        # Daten transformieren
        transformer = DataTransformer(df)
        transformed_data = transformer.transform()
        print(f"Transformiert: {len(transformed_data)} Objekte")

        # In SQLite laden
        db_path = config_loader.get_database_path()
        create_table_query = config_loader.get_create_table_query()

        # Erstelle Ordner falls nicht existiert
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        with SqliteDatabase(db_path) as db:
            db.create_table(create_table_query)
            db.insert_data(transformed_data, "space_objects")

        print(f"Erfolgreich abgeschlossen! DB: {db_path}")

    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()