"""
src.trading - Trading Module

Trading Engine, Risk Management, Backtesting und Notifications
"""

from .trading_engine import TradingEngine
from .risk_manager import RiskManager
from .backtest import BacktestEngine, MultiSymbolBacktest
from .notifier import (
    EmailNotifier,
    TelegramNotifier,
    NotificationManager,
)

__all__ = [
    'TradingEngine',
    'RiskManager',
    'BacktestEngine',
    'MultiSymbolBacktest',
    'EmailNotifier',
    'TelegramNotifier',
    'NotificationManager',
]

__version__ = '1.0.0'
__description__ = 'Trading Module with Risk Management and Backtesting'
