"""
Environment Variable Loader
Lädt Konfiguration von .env Datei mit python-dotenv
"""

import os
import logging
from pathlib import Path
from typing import Optional

# Versuche dotenv zu laden, wenn nicht installiert = funktioniert trotzdem
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logging.warning("python-dotenv nicht installiert. Nur os.environ wird genutzt.")

logger = logging.getLogger(__name__)


class EnvironmentLoader:
    """Lädt und verwaltet Umgebungsvariablen"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialisiert Environment Loader
        
        Args:
            env_file: Pfad zur .env Datei (default: .env im aktuellen Verzeichnis)
        """
        if env_file is None:
            env_file = ".env"
        
        self.env_file = Path(env_file)
        self._load_env()
    
    def _load_env(self):
        """Laden der .env Datei"""
        if DOTENV_AVAILABLE:
            if self.env_file.exists():
                load_dotenv(str(self.env_file))
                logger.info(f"✓ .env Datei geladen: {self.env_file}")
            else:
                logger.warning(f"⚠ .env Datei nicht gefunden: {self.env_file}")
        else:
            logger.debug("python-dotenv nicht verfügbar, nutze nur os.environ")
    
    @staticmethod
    def get(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
        """
        Hole Umgebungsvariable
        
        Args:
            key: Name der Variable
            default: Standardwert wenn nicht gesetzt
            required: Wenn True, wirft Fehler wenn nicht gesetzt
        
        Returns:
            Wert der Umgebungsvariable
        
        Raises:
            ValueError: Wenn required=True und Variable nicht gesetzt
        """
        value = os.getenv(key, default)
        
        if value is None and required:
            raise ValueError(f"Erforderliche Umgebungsvariable '{key}' nicht gesetzt!")
        
        if value and key.lower().endswith("password"):
            # Maskiere Passwörter in Logs
            masked = value[:3] + "*" * (len(value) - 6) if len(value) > 6 else "***"
            logger.debug(f"Umgebungsvariable '{key}' = {masked}")
        else:
            logger.debug(f"Umgebungsvariable '{key}' = {value}")
        
        return value
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """
        Hole Boolean-Umgebungsvariable
        
        Args:
            key: Name der Variable
            default: Standardwert wenn nicht gesetzt
        
        Returns:
            Boolean Wert
        """
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """
        Hole Integer-Umgebungsvariable
        
        Args:
            key: Name der Variable
            default: Standardwert wenn nicht gesetzt
        
        Returns:
            Integer Wert
        """
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Ungültiger Integer für '{key}': {os.getenv(key)}")
            return default
    
    @staticmethod
    def get_float(key: str, default: float = 0.0) -> float:
        """
        Hole Float-Umgebungsvariable
        
        Args:
            key: Name der Variable
            default: Standardwert wenn nicht gesetzt
        
        Returns:
            Float Wert
        """
        try:
            return float(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Ungültiger Float für '{key}': {os.getenv(key)}")
            return default
    
    @staticmethod
    def get_list(key: str, default: Optional[list] = None) -> list:
        """
        Hole Komma-getrennte Liste als Umgebungsvariable
        
        Args:
            key: Name der Variable
            default: Standardliste wenn nicht gesetzt
        
        Returns:
            Liste von Strings
        """
        if default is None:
            default = []
        
        value = os.getenv(key, "")
        if not value:
            return default
        
        return [item.strip() for item in value.split(",")]


# Globale Loader-Instanz
_loader = None


def init_env(env_file: Optional[str] = None):
    """
    Initialisiere globalen Environment Loader
    
    Args:
        env_file: Pfad zur .env Datei
    """
    global _loader
    _loader = EnvironmentLoader(env_file)


def get(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """Wrapper für EnvironmentLoader.get()"""
    return EnvironmentLoader.get(key, default, required)


def get_bool(key: str, default: bool = False) -> bool:
    """Wrapper für EnvironmentLoader.get_bool()"""
    return EnvironmentLoader.get_bool(key, default)


def get_int(key: str, default: int = 0) -> int:
    """Wrapper für EnvironmentLoader.get_int()"""
    return EnvironmentLoader.get_int(key, default)


def get_float(key: str, default: float = 0.0) -> float:
    """Wrapper für EnvironmentLoader.get_float()"""
    return EnvironmentLoader.get_float(key, default)


def get_list(key: str, default: Optional[list] = None) -> list:
    """Wrapper für EnvironmentLoader.get_list()"""
    return EnvironmentLoader.get_list(key, default)


# Automatisches Laden von .env bei Import
if DOTENV_AVAILABLE:
    init_env()
