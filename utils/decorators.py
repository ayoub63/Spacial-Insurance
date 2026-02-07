# Author: Abuzar
# utils/decorators.py

"""
Decorators für Logging und Performance-Messung.

Basiert auf dem Restaurant Violations Beispielprojekt des Professors.
"""

from typing import Any, Callable, TypeVar
import time
import logging

F = TypeVar('F', bound=Callable[..., Any])

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_execution(func: F) -> F:
    """
    Decorator der den Funktionsaufruf protokolliert.
    
    :param func: Funktion die dekoriert werden soll
    :return: Wrapper-Funktion
    """
    def wrapper(*args, **kwargs):
        logger.info(f"→ Starte: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"✓ Abgeschlossen: {func.__name__}")
        return result
    return wrapper  # type: ignore


def time_execution(func: F) -> F:
    """
    Decorator der die Ausführungszeit der Funktion misst.
    
    :param func: Funktion die dekoriert werden soll
    :return: Wrapper-Funktion
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"⏱  {func.__name__} benötigte {execution_time:.2f}s")
        return result
    return wrapper  # type: ignore
