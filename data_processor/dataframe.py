# Author: Abuzar
# data_processor/dataframe.py

"""
Dataframe - Wrapper-Klasse für pandas DataFrame.

Basiert auf dem Restaurant Violations Beispielprojekt des Professors.
Bietet einheitliche Schnittstelle für CSV-Operationen.
"""

import pandas as pd
from typing import Optional


class Dataframe:
    """
    Wrapper-Klasse für pandas DataFrame.
    Bietet einheitliche Schnittstelle für CSV-Operationen.
    """
    
    def __init__(self, file: str) -> None:
        """
        Initialisiert den Dataframe Wrapper.
        
        :param file: Pfad zur CSV-Datei
        """
        self.file = file
        self.data: Optional[pd.DataFrame] = None

    def __getitem__(self, column: str) -> pd.Series:
        """
        Ermöglicht direkten Zugriff auf Spalten über df['column'].
        
        :param column: Spaltenname
        :return: pandas Series mit den Spaltendaten
        """
        if self.data is None:
            raise ValueError("Daten wurden noch nicht geladen!")
        return self.data[column]

    def load_data(self) -> None:
        """
        Lädt Daten aus der CSV-Datei.
        """
        self.data = pd.read_csv(self.file, sep=",")
        print(f"✓ CSV geladen: {len(self.data):,} Zeilen, {len(self.data.columns)} Spalten")

    @property
    def shape(self) -> tuple:
        """
        Gibt die Dimensionen des DataFrames zurück.
        
        :return: Tuple (rows, columns)
        """
        if self.data is None:
            return (0, 0)
        return self.data.shape
    
    @property
    def columns(self) -> list:
        """
        Gibt die Spaltennamen zurück.
        
        :return: Liste mit Spaltennamen
        """
        if self.data is None:
            return []
        return self.data.columns.tolist()
