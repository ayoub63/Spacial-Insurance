# Author: Abuzar
# data_processor/postgres_database.py

"""
PostgreSQL Database Context Manager

Basiert auf dem Restaurant Violations Beispielprojekt des Professors.
Verwendet psycopg2 für PostgreSQL-Verbindungen.

WICHTIG: PostgreSQL muss laufen (z.B. via Docker)!
"""

import psycopg2
from psycopg2 import sql
from typing import Optional, Dict, Any
import pandas as pd


class PostgresDatabase:
    """
    Context Manager für PostgreSQL-Datenbank Operationen.
    
    Vorteile:
    - Automatisches Öffnen und Schließen der Verbindung
    - Automatisches Commit bei Erfolg, Rollback bei Fehler
    - Sauberes Exception Handling
    
    Basiert auf dem sqlite_database.py aus dem Professor-Beispiel.
    """
    
    conn: Optional[psycopg2.extensions.connection] = None
    cursor: Optional[psycopg2.extensions.cursor] = None

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialisiert den PostgreSQL Context Manager.
        
        :param config: Database Config aus YAML (host, port, user, password, name)
        """
        self.config = config
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 5432)
        self.database = config.get('name', 'space_insurance_db')
        self.user = config.get('user', 'postgres')
        self.password = config.get('password', 'postgres')

    def __enter__(self) -> "PostgresDatabase":
        """
        Öffnet die Verbindung zur Datenbank beim Eintreten des Context Managers.
        
        :return: PostgresDatabase-Instanz für weitere Operationen
        """
        print(f"\n→ Verbinde mit PostgreSQL...")
        print(f"  Host: {self.host}:{self.port}")
        print(f"  Database: {self.database}")
        
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()
            print("✓ Verbindung erfolgreich\n")
        except psycopg2.OperationalError as e:
            print(f"\n✗ FEHLER: Kann nicht zu PostgreSQL verbinden!")
            print(f"  {e}")
            print(f"\n💡 TIPP: Stelle sicher dass PostgreSQL läuft:")
            print(f"  docker ps")
            print(f"  docker start space_insurance_postgres")
            raise
        
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        """
        Schließt die Verbindung zur Datenbank beim Verlassen des Context Managers.
        
        :param exc_type: Exception-Typ (falls Fehler aufgetreten)
        :param exc_value: Exception-Wert
        :param exc_tb: Exception-Traceback
        """
        if exc_type is None:
            # Kein Fehler → Commit
            self.conn.commit()
            print("\n✓ Transaktion committed")
        else:
            # Fehler → Rollback
            self.conn.rollback()
            print(f"\n✗ Fehler: Rollback durchgeführt: {exc_value}")
        
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        
        print("✓ Datenbankverbindung geschlossen\n")

    def create_table(self, query: str) -> None:
        """
        Erstellt eine Tabelle gemäß der SQL-Query.
        
        :param query: SQL CREATE TABLE Statement
        """
        print("→ Erstelle Tabelle 'space_objects'...")
        self.cursor.execute(query)
        self.conn.commit()
        print("  ✓ Tabelle erstellt")

    def create_indexes(self, queries: str) -> None:
        """
        Erstellt Indizes für Performance-Optimierung.
        
        :param queries: SQL CREATE INDEX Statements (mehrere)
        """
        print("→ Erstelle Indizes...")
        
        # Split multi-statement query
        for query in queries.split(';'):
            query = query.strip()
            if query:
                self.cursor.execute(query)
        
        self.conn.commit()
        print("  ✓ Indizes erstellt")

    def insert_data(self, data: pd.DataFrame, query: str) -> None:
        """
        Fügt Daten aus einem DataFrame in die Datenbank ein (Batch Insert).
        
        :param data: DataFrame mit den zu speichernden Daten
        :param query: SQL INSERT Statement mit Platzhaltern (%s)
        """
        print(f"→ Füge {len(data):,} Zeilen ein...")
        
        # Konvertiere DataFrame zu Liste von Tupeln
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
                bool(row.get('sentry_object', False)),
                float(row.get('absolute_magnitude', 0)),
                bool(row['hazardous'])
            ))
        
        # Batch-Insert für Performance
        from psycopg2.extras import execute_batch
        execute_batch(self.cursor, query, records, page_size=1000)
        self.conn.commit()
        
        print(f"  ✓ {len(records):,} Zeilen eingefügt")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Holt Statistiken aus der Datenbank.
        
        :return: Dictionary mit Statistiken
        """
        print("→ Hole Statistiken...")
        
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total_objects,
                AVG(avg_diameter) as avg_diameter,
                AVG(velocity_km_s) as avg_velocity,
                SUM(CASE WHEN hazardous = true THEN 1 ELSE 0 END) as hazardous_count
            FROM space_objects
        """)
        
        result = self.cursor.fetchone()
        
        stats = {
            'total_objects': result[0],
            'avg_diameter': round(result[1], 4),
            'avg_velocity': round(result[2], 2),
            'hazardous_count': result[3]
        }
        
        print(f"  ✓ Statistiken geholt:")
        print(f"    - Gesamt Objekte: {stats['total_objects']:,}")
        print(f"    - Ø Durchmesser: {stats['avg_diameter']} km")
        print(f"    - Ø Geschwindigkeit: {stats['avg_velocity']} km/s")
        print(f"    - Hazardous: {stats['hazardous_count']:,}")
        
        return stats
