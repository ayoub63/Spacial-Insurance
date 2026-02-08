# Author: Abuzar
# data_processor/postgres_database.py

"""PostgreSQL Database Context Manager"""

import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd


class PostgresDatabase:
    """Context Manager für PostgreSQL-Datenbank Operationen."""

    conn = None
    cursor = None

    def __init__(self, db_url: str):
        """
        Initialisiert den PostgreSQL Context Manager.
        :param db_url: Connection String (z.B. postgresql://user:pass@host:port/dbname)
        """
        self.db_url = db_url

    def __enter__(self):
        """Öffnet die Verbindung zur Datenbank."""
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError:
            print("Fehler: PostgreSQL läuft nicht!")
            print(
                "Starte mit: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=space_insurance_db postgres")
            raise
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Schließt die Verbindung zur Datenbank."""
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def create_table(self, query: str):
        """
        Erstellt eine Tabelle.
        :param query: SQL CREATE TABLE Statement
        """
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, data: pd.DataFrame, table_name: str):
        """
        Fügt Daten in die Tabelle ein.
        :param data: DataFrame mit Daten
        :param table_name: Name der Ziel-Tabelle
        """
        records = []
        for _, row in data.iterrows():
            records.append((
                int(row['id']),
                str(row['name']),
                float(row['est_diameter_min']),
                float(row['est_diameter_max']),
                float(row['avg_diameter']),
                float(row['relative_velocity']),
                float(row['velocity_km_s']),
                float(row['miss_distance']),
                str(row.get('orbiting_body', 'Earth')),
                float(row.get('absolute_magnitude', 0)),
                bool(row['hazardous']),
                bool(row.get('sentry_object', False))
            ))

        query = f"""
            INSERT INTO {table_name} (
                id, name, est_diameter_min, est_diameter_max, avg_diameter,
                relative_velocity, velocity_km_s, miss_distance, orbiting_body,
                absolute_magnitude, hazardous, sentry_object
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        execute_batch(self.cursor, query, records, page_size=1000)
        self.conn.commit()