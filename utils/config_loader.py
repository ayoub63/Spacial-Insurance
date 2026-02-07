# Author: Abuzar
# utils/config_loader.py

"""
ConfigLoader - Lädt und verwaltet die YAML-Konfigurationsdatei.

Basiert auf dem Restaurant Violations Beispielprojekt des Professors.
"""

import yaml
from typing import Dict, Any


class ConfigLoader:
    """
    Lädt und verwaltet die YAML-Konfigurationsdatei.
    Stellt Zugriffsmethoden für verschiedene Konfigurationsbereiche bereit.
    """
    
    def __init__(self, config_path: str) -> None:
        """
        Initialisiert den ConfigLoader.
        
        :param config_path: Pfad zur YAML-Konfigurationsdatei
        """
        self.config_path = config_path
        self.yaml_config = self._load_yaml()

    def _load_yaml(self) -> Dict[str, Any]:
        """
        Lädt die YAML-Datei und gibt den Inhalt als Dictionary zurück.
        
        :return: Dictionary mit allen Konfigurationen
        """
        with open(self.config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def get_database_config(self) -> Dict[str, Any]:
        """
        Gibt die Datenbank-Konfiguration zurück.
        
        :return: Dictionary mit PostgreSQL Connection Details
        """
        return self.yaml_config.get("database", {})

    def get_paths_config(self) -> Dict[str, str]:
        """
        Gibt die Dateipfad-Konfiguration zurück.
        
        :return: Dictionary mit Dateipfaden
        """
        return self.yaml_config.get("paths", {})

    def get_transformations_config(self) -> Dict[str, Any]:
        """
        Gibt die Transformations-Parameter zurück (Feature 1).
        
        :return: Dictionary mit Einheiten und Bereinigungsregeln
        """
        return self.yaml_config.get("transformations", {})
    
    def get_queries(self) -> Dict[str, str]:
        """
        Gibt alle SQL-Queries zurück.
        
        :return: Dictionary mit SQL Statements
        """
        return self.yaml_config.get("queries", {})
