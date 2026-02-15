# Autor: Ayoub Afkir

import pytest
import pandas as pd


from logic.risk import RiskEngine


@pytest.fixture
def engine():
    # Erstellt eine Instanz der RiskEngine für jeden Test
    return RiskEngine(base_premium=10000.0)


@pytest.fixture
def mock_data():
    # Erstellt Test-Daten (ein harmloser, ein gefährlicher Asteroid).
    return pd.DataFrame({
        'id': ['1', '2'],
        'name': ['Safe Rock', 'Doomsday Rock'],
        'avg_diameter': [0.02, 2.5],  # km (20m vs 2.5km)
        'velocity_km_s': [15.0, 25.0],  # km/s
        'miss_distance': [5000000, 100],  # km
        'hazardous': [False, True]  # NASA Flag
    })


def test_physics_calculation(engine, mock_data):
    # Prüft, ob Masse und Energie korrekt berechnet werden
    df = engine.calculate_physics(mock_data)

    # Prüfen, ob Spalten existieren
    assert 'mass_kg' in df.columns
    assert 'energy_tj' in df.columns

    # 2.5km Objekt muss schwerer sein als 20m Objekt
    mass_safe = df.loc[0, 'mass_kg']
    mass_doom = df.loc[1, 'mass_kg']
    assert mass_doom > mass_safe

    # Energie muss positiv sein
    assert (df['energy_tj'] > 0).all()


def test_hazardous_rejection(engine, mock_data):
    # Prüft, ob gefährliche Objekte automatisch abgelehnt werden.
    df = engine.evaluate_portfolio(mock_data)

    # Objekt 2 ist hazardous=True Muss ABGELEHNT sein
    status_doom = df.loc[1, 'policy_status']
    premium_doom = df.loc[1, 'premium_eur']

    assert status_doom == 'ABGELEHNT'
    assert premium_doom == 0.0


def test_pricing_logic(engine, mock_data):
    # Prüft, ob genehmigte Objekte einen Preis erhalten
    df = engine.evaluate_portfolio(mock_data)

    # Objekt 1 ist hazardous=False Muss GENEHMIGT sein
    status_safe = df.loc[0, 'policy_status']
    premium_safe = df.loc[0, 'premium_eur']

    assert status_safe == 'GENEHMIGT'
    # Preis muss höher als Basisprämie sein (wegen Risikoaufschlag)
    assert premium_safe >= 10000.0

