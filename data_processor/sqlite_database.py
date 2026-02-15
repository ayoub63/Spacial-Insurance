# Author: Abuzar

#SQLite Database Context Manager

import sqlite3
import pandas as pd


class SqliteDatabase:
     #Context Manager für SQLite-Datenbank Operationen.

    conn = None
    cursor = None

    def __init__(self, db_path: str):
        """
        Initialisiert den SQLite Context Manager.
        :param db_path: Pfad zur SQLite-Datenbank Datei
        """
        self.db_path = db_path

    def __enter__(self):
        #Öffnet die Verbindung zur Datenbank.
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        #Schließt die Verbindung zur Datenbank.
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
                int(row['hazardous']),
                int(row.get('sentry_object', False))
            ))

        query = f"""
            INSERT INTO {table_name} (
                id, name, est_diameter_min, est_diameter_max, avg_diameter,
                relative_velocity, velocity_km_s, miss_distance, orbiting_body,
                absolute_magnitude, hazardous, sentry_object
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.cursor.executemany(query, records)
        self.conn.commit()