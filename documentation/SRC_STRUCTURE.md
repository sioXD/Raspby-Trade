# Source Code Structure

## Overview

Das `src/` Verzeichnis wurde reorganisiert für bessere Wartbarkeit und logische Gruppierung:

```
src/
├── __init__.py                 # Main package exports
├── env_loader.py              # Environment variable management
├── analysis/                  # Stock Market Analysis
│   ├── __init__.py
│   ├── data_fetching.py       # Yahoo Finance data retrieval
│   ├── stock_analysis.py      # Technical analysis (MA, returns)
│   ├── correlation_analysis.py  # Multi-stock correlation
│   ├── risk_analysis.py       # Risk metrics (VaR, CVaR, etc)
│   └── monte_carlo_simulation.py # GBM simulations
├── ml/                        # Machine Learning
│   ├── __init__.py
│   └── lstm_prediction.py     # LSTM neural network predictions
├── trading/                   # Trading Execution & Risk
│   ├── __init__.py
│   ├── trading_engine.py      # Alpaca API integration
│   ├── risk_manager.py        # Position sizing, stop loss/TP
│   ├── backtest.py            # Strategy backtesting
│   └── notifier.py            # Email/Telegram alerts
└── utils/                     # Utilities & Orchestration
    ├── __init__.py
    └── main.py                # Main orchestration function
```

## Module Organization

### 📊 `src/analysis/` - Financial Data & Analysis
Handles all data retrieval and technical analysis:

| Module | Purpose | Key Functions |
|--------|---------|---|
| `data_fetching.py` | Retrieve stock data from Yahoo Finance | `fetch_stock_data()`, `get_closing_prices()` |
| `stock_analysis.py` | Technical indicators & statistics | `calculate_moving_averages()`, `calculate_daily_returns()` |
| `correlation_analysis.py` | Multi-stock correlation analysis | `calculate_returns_for_stocks()`, `plot_correlation_heatmap()` |
| `risk_analysis.py` | Risk metrics & Value at Risk | `calculate_var_bootstrap()`, `calculate_cvar()` |
| `monte_carlo_simulation.py` | Geometric Brownian Motion simulations | `monte_carlo_simulation_for_data()`, `stock_monte_carlo()` |

**Imports (in main files):**
```python
from src.analysis import (
    fetch_stock_data,
    get_closing_prices,
    calculate_moving_averages,
    calculate_daily_returns,
    calculate_returns_for_stocks,
    monte_carlo_simulation_for_data,
)
```

---

### 🤖 `src/ml/` - Machine Learning Models
AI-based price prediction:

| Module | Purpose | Key Functions |
|--------|---------|---|
| `lstm_prediction.py` | LSTM neural network for price forecasting | `train_bi_lstm_from_mc()`, `predict_future_bi_lstm_from_mc()`, `predict_stock_price()` |

**Imports (in main files):**
```python
from src.ml import predict_stock_price
```

---

### 💰 `src/trading/` - Trading Execution & Risk Management
Order execution, position management, and backtesting:

| Module | Purpose | Key Classes/Functions |
|--------|---------|---|
| `trading_engine.py` | Alpaca API integration for live trading | `TradingEngine` class |
| `risk_manager.py` | Position sizing & risk metrics | `RiskManager` class |
| `backtest.py` | Strategy backtesting engine | `BacktestEngine`, `MultiSymbolBacktest` classes |
| `notifier.py` | Alert notifications (Email/Telegram) | `EmailNotifier`, `TelegramNotifier`, `NotificationManager` classes |

**Imports (in main files):**
```python
from src.trading import (
    TradingEngine,
    RiskManager,
    BacktestEngine,
    NotificationManager,
)
```

---

### 🛠️ `src/utils/` - Utilities & Orchestration
Main orchestration and helper functions:

| Module | Purpose | Key Functions |
|--------|---------|---|
| `main.py` | Main bot orchestration | `main()` function |

**Imports (in main files):**
```python
from src.utils import main
```

---

### ⚙️ `src/env_loader.py` - Configuration
Environment variable management for secure credential storage.

**Imports (in main files):**
```python
from src.env_loader import load_env_config, get_alpaca_keys
```

---

## Import Patterns

### ✅ New Pattern (After Refactoring)

```python
# Import from specific submodules
from src.analysis import fetch_stock_data, calculate_moving_averages
from src.ml import predict_stock_price
from src.trading import TradingEngine, RiskManager
from src.utils import main

# Or import from top-level src package
from src import fetch_stock_data, TradingEngine, predict_stock_price
```

### ❌ Old Pattern (No Longer Works)

```python
# These imports WILL FAIL after refactoring
from src.data_fetching import fetch_stock_data  # ❌
from src.trading_engine import TradingEngine    # ❌
from src.lstm_prediction import predict_stock_price  # ❌
```

---

## Files Using New Structure

### ✅ Already Updated

- **pi_bot_main.py** - Main production bot (uses new imports)
- **demo_bot.py** - Interactive demo (uses new imports)
- **test_bot_locally.py** - Local testing suite (uses new imports)

### Module __init__.py Files

Each submodule has an `__init__.py` that exports public APIs:

```python
# src/analysis/__init__.py
from .data_fetching import fetch_stock_data, get_closing_prices
from .stock_analysis import calculate_moving_averages, calculate_daily_returns
from .correlation_analysis import calculate_returns_for_stocks, plot_correlation_heatmap
from .risk_analysis import calculate_var_bootstrap, calculate_cvar
from .monte_carlo_simulation import monte_carlo_simulation_for_data

__all__ = [
    'fetch_stock_data',
    'get_closing_prices',
    'calculate_moving_averages',
    'calculate_daily_returns',
    'calculate_returns_for_stocks',
    'plot_correlation_heatmap',
    'calculate_var_bootstrap',
    'calculate_cvar',
    'monte_carlo_simulation_for_data',
]
```

---

## Migration Guide

If you need to update existing files to use the new structure:

### Step 1: Replace Old Imports

Replace:
```python
from src.data_fetching import fetch_stock_data
from src.stock_analysis import calculate_moving_averages
from src.trading_engine import TradingEngine
```

With:
```python
from src.analysis import fetch_stock_data, calculate_moving_averages
from src.trading import TradingEngine
```

### Step 2: Consolidate Related Imports

Before:
```python
from src.data_fetching import fetch_stock_data, get_closing_prices
from src.correlation_analysis import calculate_returns_for_stocks
```

After:
```python
from src.analysis import (
    fetch_stock_data,
    get_closing_prices,
    calculate_returns_for_stocks,
)
```

---

## Benefits of New Structure

✅ **Better Organization** - Related modules grouped by functionality  
✅ **Easier Navigation** - Clear separation of concerns  
✅ **Maintainability** - Simpler to add new features  
✅ **Scalability** - Easy to add submodules within categories  
✅ **Clean Imports** - Consolidated, readable import statements  

---

## Next Steps

If adding new features:

1. **Data Analysis?** → Add to `src/analysis/`
2. **ML Model?** → Add to `src/ml/`
3. **Trading Logic?** → Add to `src/trading/`
4. **Utilities?** → Add to `src/utils/`

Then update the corresponding `__init__.py` file to export new functions/classes.

---

*Last Updated: December 2024*
