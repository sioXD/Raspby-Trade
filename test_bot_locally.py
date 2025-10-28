"""
Quick Test Script for Trading Bot on Laptop
Testet alle Bot-Komponenten lokal auf deinem Laptop
"""

import logging
import os
import sys
from datetime import datetime

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_data_fetching():
    """Test: Daten laden von Yahoo Finance"""
    print("\n" + "="*60)
    print("TEST 1: DATA FETCHING")
    print("="*60)
    
    try:
        from src.analysis import get_closing_prices
        
        logger.info("Lade Daten für AAPL, GOOGL, MSFT...")
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        prices = get_closing_prices(symbols)
        
        logger.info(f"✓ Erfolgreich! {len(prices)} Datenpunkte geladen")
        logger.info(f"Shape: {prices.shape}")
        logger.info(f"\nLetzte 5 Tage:\n{prices.tail()}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        return False


def test_analysis():
    """Test: Stock Analysis"""
    print("\n" + "="*60)
    print("TEST 2: STOCK ANALYSIS")
    print("="*60)
    
    try:
        from src.analysis import fetch_stock_data, calculate_moving_averages, calculate_daily_returns
        
        logger.info("Lade AAPL Daten...")
        stock_data = fetch_stock_data(['AAPL'])
        
        if 'AAPL' not in stock_data:
            logger.error("AAPL Daten nicht geladen")
            return False
        
        aapl = stock_data['AAPL']
        
        logger.info("Berechne Moving Averages...")
        aapl = calculate_moving_averages(aapl, ma_days=[10, 20, 50])
        
        logger.info("Berechne Daily Returns...")
        aapl = calculate_daily_returns(aapl)
        
        logger.info(f"✓ Erfolgreich!")
        logger.info(f"\nAAPL Statistik:\n{aapl.describe()}")
        logger.info(f"\nMA Columns: {[col for col in aapl.columns if 'MA' in col]}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        return False


def test_correlation():
    """Test: Correlation Analysis"""
    print("\n" + "="*60)
    print("TEST 3: CORRELATION ANALYSIS")
    print("="*60)
    
    try:
        from src.analysis import get_closing_prices, calculate_returns_for_stocks
        
        logger.info("Lade Daten...")
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
        prices = get_closing_prices(symbols)
        
        logger.info("Berechne Returns...")
        returns = calculate_returns_for_stocks(prices)
        
        logger.info("Berechne Korrelation...")
        corr = returns.corr()
        
        logger.info(f"✓ Erfolgreich!")
        logger.info(f"\nKorrelationsmatrix:\n{corr}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        return False


def test_risk_management():
    """Test: Risk Manager"""
    print("\n" + "="*60)
    print("TEST 4: RISK MANAGEMENT")
    print("="*60)
    
    try:
        from src.trading import RiskManager
        
        logger.info("Initialisiere Risk Manager...")
        rm = RiskManager(
            account_balance=100000,
            risk_per_trade=0.02,
            max_positions=5
        )
        
        # Test Position Size Berechnung
        logger.info("\nTest Position Size:")
        entry_price = 150.0
        stop_loss_price = 142.5  # 5% below
        position_size = rm.calculate_position_size(entry_price, stop_loss_price)
        logger.info(f"Entry: ${entry_price}, SL: ${stop_loss_price}")
        logger.info(f"Position Size: {position_size} shares")
        
        # Test Stop Loss / Take Profit
        logger.info("\nTest Stop Loss & Take Profit:")
        sl = rm.calculate_stop_loss(entry_price, stop_loss_pct=0.05)
        tp = rm.calculate_take_profit(entry_price, take_profit_pct=0.10)
        logger.info(f"Stop Loss: ${sl:.2f}")
        logger.info(f"Take Profit: ${tp:.2f}")
        
        # Test Trade Validation
        logger.info("\nTest Trade Validation:")
        is_valid, msg = rm.validate_trade('AAPL', position_size, entry_price, sl)
        logger.info(f"Trade Valid: {is_valid}")
        logger.info(f"Message: {msg}")
        
        # Test Position hinzufügen
        logger.info("\nTest Position hinzufügen:")
        rm.add_position('AAPL', position_size, entry_price, sl, tp)
        logger.info(f"Position hinzugefügt")
        
        # Risk Exposure
        exposure = rm.get_risk_exposure()
        logger.info(f"\n✓ Erfolgreich!")
        logger.info(f"Risk Exposure: {exposure}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_trading_engine():
    """Test: Trading Engine (Mock Mode)"""
    print("\n" + "="*60)
    print("TEST 5: TRADING ENGINE (Mock Mode)")
    print("="*60)
    
    try:
        from src.trading import TradingEngine
        
        logger.info("Initialisiere Trading Engine (Mock Mode)...")
        engine = TradingEngine(use_paper_trading=True)
        
        # Test Account Info
        logger.info("\nGet Account Info:")
        account = engine.get_account_info()
        logger.info(f"Account: {account}")
        
        # Test Mock Buy Order
        logger.info("\nExecute Mock BUY Order:")
        buy_order = engine.execute_buy_order('AAPL', 10)
        logger.info(f"Order: {buy_order}")
        
        # Test Mock Sell Order
        logger.info("\nExecute Mock SELL Order:")
        sell_order = engine.execute_sell_order('AAPL', 5)
        logger.info(f"Order: {sell_order}")
        
        # Get Trades Log
        logger.info("\nTrades Log:")
        trades = engine.get_trades_log()
        logger.info(f"✓ Erfolgreich! {len(trades)} Orders ausgeführt")
        for trade in trades:
            logger.info(f"  {trade}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_notifier():
    """Test: Notifier (without actually sending)"""
    print("\n" + "="*60)
    print("TEST 6: NOTIFIER")
    print("="*60)
    
    try:
        from src.trading import NotificationManager
        
        logger.info("Initialisiere Notification Manager...")
        nm = NotificationManager()
        
        logger.info("✓ Notifier bereit (Email/Telegram nicht konfiguriert)")
        logger.info("  → Später konfigurierbar via .env")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        return False


def test_backtest():
    """Test: Backtesting"""
    print("\n" + "="*60)
    print("TEST 7: BACKTESTING")
    print("="*60)
    
    try:
        import numpy as np
        import pandas as pd
        from src.trading import BacktestEngine
        
        logger.info("Erstelle Sample Daten...")
        dates = pd.date_range('2024-01-01', periods=100)
        prices = 150 + np.cumsum(np.random.randn(100) * 2)
        price_data = pd.DataFrame({'Close': prices}, index=dates)
        
        # Generate simple signals
        signals = pd.Series([
            'BUY' if i % 20 == 0 else ('SELL' if i % 10 == 0 else None)
            for i in range(100)
        ], index=dates)
        
        logger.info("Starte Backtest...")
        engine = BacktestEngine(initial_balance=100000)
        results = engine.run_backtest('TEST', price_data, signals)
        
        if results:
            logger.info(f"✓ Backtest erfolgreich!")
            logger.info(f"  Total Trades: {results['total_trades']}")
            logger.info(f"  Win Rate: {results['win_rate_pct']:.2f}%")
            logger.info(f"  Total Return: {results['total_return_pct']:.2f}%")
            logger.info(f"  Sharpe Ratio: {results['sharpe_ratio']:.2f}")
            return True
        else:
            logger.warning("Keine Trades im Backtest")
            return False
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_monte_carlo():
    """Test: Monte Carlo Simulation"""
    print("\n" + "="*60)
    print("TEST 8: MONTE CARLO SIMULATION")
    print("="*60)
    
    try:
        import numpy as np
        from src.analysis import fetch_stock_data, monte_carlo_simulation_for_data
        
        logger.info("Lade AAPL Daten...")
        stock_data = fetch_stock_data(['AAPL'])
        
        if 'AAPL' not in stock_data:
            logger.error("AAPL Daten nicht geladen")
            return False
        
        aapl = stock_data['AAPL']
        
        logger.info("Starte Monte Carlo Simulation...")
        simulated = monte_carlo_simulation_for_data(aapl, num_simulations=50, num_days=100)
        
        logger.info(f"✓ Simulation erfolgreich!")
        logger.info(f"  Shape: {simulated.shape}")
        logger.info(f"  Mean Final Price: ${simulated[:, -1].mean():.2f}")
        logger.info(f"  Std Dev: ${simulated[:, -1].std():.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Führe alle Tests aus"""
    print("\n" + "="*70)
    print(" TRADING BOT - LAPTOP TEST SUITE")
    print("="*70)
    
    tests = [
        ("Data Fetching", test_data_fetching),
        ("Stock Analysis", test_analysis),
        ("Correlation", test_correlation),
        ("Risk Management", test_risk_management),
        ("Trading Engine", test_trading_engine),
        ("Notifier", test_notifier),
        ("Backtesting", test_backtest),
        ("Monte Carlo", test_monte_carlo),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status:8} | {test_name}")
    
    print("-" * 70)
    print(f"Result: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
