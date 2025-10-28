"""
src.ml - Machine Learning Module

Machine Learning Modelle für Aktienvorhersagen (LSTM, etc.)
"""

from .lstm_prediction import (
    train_bi_lstm_from_mc,
    predict_future_bi_lstm_from_mc,
    predict_stock_price,
)

__all__ = [
    'train_bi_lstm_from_mc',
    'predict_future_bi_lstm_from_mc',
    'predict_stock_price',
]

__version__ = '1.0.0'
__description__ = 'Machine Learning Module for Stock Predictions'
