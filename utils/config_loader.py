# Author: Abuzar
# utils/config_loader.py

"""Lädt und verwaltet die YAML-Konfigurationsdatei."""

import yaml


class ConfigLoader:
    """Lädt und verwaltet die YAML-Konfigurationsdatei."""

    def __init__(self, config_path: str):
        """
        Initialisiert den ConfigLoader.
        :param config_path: Pfad zur YAML-Konfigurationsdatei
        """
        self.config_path = config_path
        self.yaml_config = self._load_yaml()

    def _load_yaml(self):
        """
        Lädt die YAML-Datei.
        :return: Dictionary mit Konfigurationen
        """
        with open(self.config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def get_database_path(self):
        """
        Gibt den Datenbank-Pfad zurück.
        :return: Pfad zur SQLite-Datenbank
        """
        db = self.yaml_config.get("database", {})
        return db.get("path")

    def get_csv_path(self):
        """
        Gibt den CSV-Dateipfad zurück.
        :return: Pfad zur CSV-Datei
        """
        paths = self.yaml_config.get("paths", {})
        return paths.get("csv_raw")

    def get_create_table_query(self):
        """
        Gibt die CREATE TABLE Query zurück.
        :return: SQL CREATE TABLE Statement
        """
        queries = self.yaml_config.get("queries", {})
        return queries.get("create_table")