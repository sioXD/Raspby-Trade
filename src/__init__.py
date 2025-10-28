"""
src - Stock Market Trading Bot Package

Main package für den Stock Market Trading Bot mit:
- Datenanalyse (analysis)
- Machine Learning (ml)
- Trading Logik (trading)
- Utilities (utils)
- Environment Management (env_loader)
"""

from . import analysis
from . import ml
from . import trading
from . import utils
from .env_loader import (
    EnvironmentLoader,
    init_env,
    get,
    get_bool,
    get_int,
    get_float,
    get_list,
)

__all__ = [
    'analysis',
    'ml',
    'trading',
    'utils',
    'EnvironmentLoader',
    'init_env',
    'get',
    'get_bool',
    'get_int',
    'get_float',
    'get_list',
]

__version__ = '2.0.0'
__description__ = 'Stock Market Trading Bot for Raspberry Pi'
