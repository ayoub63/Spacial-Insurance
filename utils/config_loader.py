# Author: Abuzar
# utils/config_loader.py

# Lädt und verwaltet die YAML-Konfigurationsdatei

import yaml


class ConfigLoader:

    def __init__(self, config_path: str):
        # Initialisiert den ConfigLoader
        self.config_path = config_path
        self.yaml_config = self._load_yaml()

    def _load_yaml(self):
        # Lädt die YAML-Datei
        with open(self.config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def get_database_path(self):
        # Gibt den Datenbank-Pfad zurück.
        db = self.yaml_config.get("database", {})
        return db.get("path")

    def get_csv_path(self):
        # Gibt den CSV-Dateipfad zurück
        paths = self.yaml_config.get("paths", {})
        return paths.get("csv_raw")

    def get_create_table_query(self):
        # Gibt die CREATE TABLE Query zurück
        queries = self.yaml_config.get("queries", {})
        return queries.get("create_table")