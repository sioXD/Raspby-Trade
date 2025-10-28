"""
src.analysis - Stock Market Analysis Module

Datenanalyse und technische Indikatoren für Aktienmarktanalyse.
"""

from .data_fetching import fetch_stock_data, get_closing_prices
from .stock_analysis import (
    calculate_moving_averages,
    calculate_daily_returns,
    plot_closing_price,
    plot_moving_averages,
)
from .correlation_analysis import (
    calculate_returns_for_stocks,
    plot_correlation_heatmap,
    plot_pairplot,
)
from .risk_analysis import (
    plot_risk_return_scatter,
    calculate_var_bootstrap,
    calculate_var_for_all_stocks,
)
from .monte_carlo_simulation import (
    stock_monte_carlo,
    monte_carlo_var_analysis,
    plot_monte_carlo_simulations,
    monte_carlo_simulation_for_data,
)

__all__ = [
    'fetch_stock_data',
    'get_closing_prices',
    'calculate_moving_averages',
    'calculate_daily_returns',
    'plot_closing_price',
    'plot_moving_averages',
    'calculate_returns_for_stocks',
    'plot_correlation_heatmap',
    'plot_pairplot',
    'plot_risk_return_scatter',
    'calculate_var_bootstrap',
    'calculate_var_for_all_stocks',
    'stock_monte_carlo',
    'monte_carlo_var_analysis',
    'plot_monte_carlo_simulations',
    'monte_carlo_simulation_for_data',
]

__version__ = '1.0.0'
__description__ = 'Stock Market Analysis Module'
