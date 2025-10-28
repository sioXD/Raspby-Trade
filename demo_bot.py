"""
Trading Bot Demo - Interaktives Test-Szenario
Simuliert einen echten Handelsalltag auf deinem Laptop
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_trading_workflow():
    """
    Demo: Kompletter Trading-Workflow
    - Daten laden
    - Signale generieren
    - Trades ausführen
    - Risiko managen
    """
    print("\n" + "="*70)
    print(" TRADING BOT - DEMO: Kompletter Workflow")
    print("="*70 + "\n")
    
    from src.analysis import get_closing_prices, calculate_returns_for_stocks
    from src.trading import RiskManager, TradingEngine
    
    try:
        # 1. Daten laden
        print("[SCHRITT 1] Lade Aktiendaten...")
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        prices = get_closing_prices(symbols)
        print(f"✓ {len(prices)} Datenpunkte für {len(symbols)} Symbole geladen\n")
        
        # 2. Aktuelle Preise
        print("[SCHRITT 2] Aktuelle Preise:")
        current_prices = prices.iloc[-1]
        for symbol in symbols:
            price = current_prices[symbol]
            prev_price = prices[symbol].iloc[-2]
            change = ((price - prev_price) / prev_price) * 100
            print(f"  {symbol}: ${price:.2f} ({change:+.2f}%)")
        print()
        
        # 3. Trading Setup
        print("[SCHRITT 3] Starte Trading Engine & Risk Manager...")
        engine = TradingEngine(use_paper_trading=True)
        rm = RiskManager(account_balance=100000, risk_per_trade=0.02)
        
        account = engine.get_account_info()
        print(f"  Account Balance: ${account['buying_power']:.2f}")
        print(f"  Risk per Trade: 2% (${account['buying_power']*0.02:.2f})\n")
        
        # 4. Simuliere Trading-Szenario
        print("[SCHRITT 4] Simuliere Trading-Szenario...")
        
        # Buy Signal für AAPL
        print("\n  → AAPL: BULLISH Signal (Confidence: 85%)")
        aapl_price = current_prices['AAPL']
        sl = rm.calculate_stop_loss(aapl_price, 0.05)
        tp = rm.calculate_take_profit(aapl_price, 0.10)
        qty = rm.calculate_position_size(aapl_price, sl)
        
        print(f"    Entry: ${aapl_price:.2f}")
        print(f"    Stop Loss: ${sl:.2f}")
        print(f"    Take Profit: ${tp:.2f}")
        print(f"    Position Size: {qty} shares")
        
        # Validiere Trade
        is_valid, msg = rm.validate_trade('AAPL', qty, aapl_price, sl)
        print(f"    Trade Valid: {is_valid} - {msg}")
        
        if is_valid:
            # Execute Trade
            print(f"    → Executing BUY Order...")
            order = engine.execute_buy_order('AAPL', qty)
            if order:
                print(f"    ✓ Order gefüllt: {qty} @ ${aapl_price:.2f}")
                rm.add_position('AAPL', qty, aapl_price, sl, tp)
        
        # Buy Signal für GOOGL
        print("\n  → GOOGL: BULLISH Signal (Confidence: 72%)")
        googl_price = current_prices['GOOGL']
        sl = rm.calculate_stop_loss(googl_price, 0.05)
        tp = rm.calculate_take_profit(googl_price, 0.10)
        qty = rm.calculate_position_size(googl_price, sl)
        
        print(f"    Entry: ${googl_price:.2f}")
        print(f"    Stop Loss: ${sl:.2f}")
        print(f"    Take Profit: ${tp:.2f}")
        print(f"    Position Size: {qty} shares")
        
        is_valid, msg = rm.validate_trade('GOOGL', qty, googl_price, sl)
        print(f"    Trade Valid: {is_valid} - {msg}")
        
        if is_valid:
            order = engine.execute_buy_order('GOOGL', qty)
            if order:
                print(f"    ✓ Order gefüllt: {qty} @ ${googl_price:.2f}")
                rm.add_position('GOOGL', qty, googl_price, sl, tp)
        
        # MSFT: Verkaufsignal (wenn Position existiert würde)
        print("\n  → MSFT: BEARISH Signal (aber keine Position)")
        print("    (Skipped: Keine Position zum Verkaufen)")
        
        # 5. Risiko-Übersicht
        print("\n[SCHRITT 5] Risiko-Übersicht:")
        exposure = rm.get_risk_exposure()
        positions = rm.get_all_positions()
        
        print(f"  Open Positions: {len(positions)}")
        for symbol in positions:
            pos = positions[symbol]
            print(f"    {symbol}: {pos['qty']} shares @ ${pos['entry_price']:.2f}")
            print(f"      SL: ${pos['stop_loss']:.2f}, TP: ${pos['take_profit']:.2f}")
        
        print(f"\n  Total Risk Exposure: ${exposure['total_risk']:.2f}")
        print(f"  Risk %: {exposure['risk_percentage']:.2f}%")
        print(f"  Max Allowed: ${exposure['max_allowed_risk']:.2f}")
        
        # 6. Trade Log
        print("\n[SCHRITT 6] Trade Log:")
        trades = engine.get_trades_log()
        for i, trade in enumerate(trades, 1):
            print(f"  {i}. {trade['side'].upper()} {trade['symbol']} - {trade['qty']} shares")
        
        print("\n✓ Demo erfolgreich abgeschlossen!")
        return True
        
    except Exception as e:
        logger.error(f"Demo Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_backtesting():
    """
    Demo: Backtesting einer Strategie
    """
    print("\n" + "="*70)
    print(" TRADING BOT - DEMO: Backtesting")
    print("="*70 + "\n")
    
    from src.trading import BacktestEngine
    from src.analysis import get_closing_prices, fetch_stock_data
    
    try:
        # 1. Lade Daten
        print("[SCHRITT 1] Lade historische Daten...")
        stock_data = fetch_stock_data(['AAPL'])
        aapl_data = stock_data['AAPL']
        print(f"✓ {len(aapl_data)} Datenpunkte geladen (von {aapl_data.index[0].date()} bis {aapl_data.index[-1].date()})\n")
        
        # 2. Generiere einfache Signale (Moving Average Strategie)
        print("[SCHRITT 2] Generiere Trading Signale (Simple MA Strategie)...")
        price_series = aapl_data['Close']
        sma_short = price_series.rolling(window=10).mean()
        sma_long = price_series.rolling(window=50).mean()
        
        signals = pd.Series(index=aapl_data.index, dtype=object)
        for i in range(len(aapl_data)):
            sma_short_val = sma_short.iloc[i]
            sma_long_val = sma_long.iloc[i]
            
            # Konvertiere zu Python-float für direkten Vergleich
            try:
                sma_short_float = float(sma_short_val)
                sma_long_float = float(sma_long_val)
            except (ValueError, TypeError):
                signals.iloc[i] = None
                continue
                
            if np.isnan(sma_short_float) or np.isnan(sma_long_float):
                signals.iloc[i] = None
            elif sma_short_float > sma_long_float:
                signals.iloc[i] = 'BUY'
            else:
                signals.iloc[i] = 'SELL'
        
        buy_signals = (signals == 'BUY').sum()
        sell_signals = (signals == 'SELL').sum()
        print(f"✓ {buy_signals} BUY und {sell_signals} SELL Signale generiert\n")
        
        # 3. Starte Backtest
        print("[SCHRITT 3] Starte Backtest...")
        engine = BacktestEngine(initial_balance=100000)
        results = engine.run_backtest('AAPL', aapl_data, signals)
        
        if results:
            print("✓ Backtest abgeschlossen!\n")
            
            # 4. Zeige Ergebnisse
            print("[SCHRITT 4] Backtest Ergebnisse:")
            print(f"  Initial Balance:        ${results['initial_balance']:,.2f}")
            print(f"  Final Balance:          ${results['final_balance']:,.2f}")
            print(f"  Total Profit:           ${results['total_profit']:,.2f}")
            print(f"  Total Return:           {results['total_return_pct']:.2f}%")
            print()
            print(f"  Total Trades:           {results['total_trades']}")
            print(f"  Winning Trades:         {results['winning_trades']}")
            print(f"  Losing Trades:          {results['losing_trades']}")
            print(f"  Win Rate:               {results['win_rate_pct']:.2f}%")
            print()
            print(f"  Avg Profit/Trade:       ${results['avg_profit']:,.2f}")
            print(f"  Max Profit:             ${results['max_profit']:,.2f}")
            print(f"  Max Loss:               ${results['max_loss']:,.2f}")
            print(f"  Profit Factor:          {results['profit_factor']:.2f}")
            print()
            print(f"  Sharpe Ratio:           {results['sharpe_ratio']:.2f}")
            print(f"  Max Drawdown:           {results['max_drawdown_pct']:.2f}%")
            print(f"  Avg Hold Days:          {results['avg_hold_days']:.1f}")
            
            # 5. Top Trades
            print("\n[SCHRITT 5] Top 3 Gewinntrades:")
            trades = results['trades']
            top_winners = trades.nlargest(3, 'profit')
            for idx, (_, trade) in enumerate(top_winners.iterrows(), 1):
                print(f"  {idx}. {trade['entry_date'].date()}: {trade['profit']:+,.2f} ({trade['profit_pct']:+.2f}%)")
            
            print("\n✓ Backtest Demo abgeschlossen!")
            return True
        else:
            print("✗ Backtest fehlgeschlagen")
            return False
            
    except Exception as e:
        logger.error(f"Backtest Demo Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_risk_scenarios():
    """
    Demo: Verschiedene Risiko-Szenarien
    """
    print("\n" + "="*70)
    print(" TRADING BOT - DEMO: Risiko-Szenarien")
    print("="*70 + "\n")
    
    from src.trading import RiskManager
    
    try:
        # Scenario 1: Normaler Trade
        print("[SZENARIO 1] Normaler Trade:")
        rm = RiskManager(account_balance=100000, risk_per_trade=0.02, max_positions=5)
        
        entry = 150
        sl = rm.calculate_stop_loss(entry, 0.05)
        tp = rm.calculate_take_profit(entry, 0.10)
        qty = rm.calculate_position_size(entry, sl)
        
        is_valid, msg = rm.validate_trade('AAPL', qty, entry, sl)
        print(f"  Entry: ${entry}, SL: ${sl:.2f}, TP: ${tp:.2f}")
        print(f"  Position Size: {qty}, Valid: {is_valid}\n")
        
        # Scenario 2: Zu großer Trade
        print("[SZENARIO 2] Zu großer Trade:")
        huge_qty = 10000  # Viel zu groß
        is_valid, msg = rm.validate_trade('GOOGL', huge_qty, 150, 142.5)
        print(f"  Position Size: {huge_qty}")
        print(f"  Valid: {is_valid}")
        print(f"  Reason: {msg}\n")
        
        # Scenario 3: Max Positionen erreicht
        print("[SZENARIO 3] Max Positionen erreicht:")
        rm_small = RiskManager(account_balance=100000, risk_per_trade=0.02, max_positions=2)
        
        # Add 2 positions
        rm_small.add_position('AAPL', 100, 150, 142.5, 165)
        rm_small.add_position('GOOGL', 50, 130, 123.5, 143)
        
        # Try to add 3rd
        is_valid, msg = rm_small.validate_trade('MSFT', 100, 380, 361)
        print(f"  Open Positions: {len(rm_small.get_all_positions())}/2")
        print(f"  Valid for 3rd: {is_valid}")
        print(f"  Reason: {msg}\n")
        
        # Scenario 4: Stop Loss Hit
        print("[SZENARIO 4] Stop Loss wird ausgelöst:")
        rm_test = RiskManager(account_balance=100000, risk_per_trade=0.02)
        
        entry = 100
        sl = rm_test.calculate_stop_loss(entry, 0.05)  # $95
        tp = rm_test.calculate_take_profit(entry, 0.10)  # $110
        
        rm_test.add_position('TEST', 100, entry, sl, tp)
        
        print(f"  Position: 100 shares @ ${entry}")
        print(f"  Stop Loss: ${sl:.2f}")
        
        # Prüfe verschiedene Preise
        prices = [105, 99, 95, 90]
        for price in prices:
            hit = rm_test.check_stop_loss('TEST', price)
            status = "🔴 HIT!" if hit else "✓ OK"
            print(f"  Preis ${price}: {status}")
        
        print("\n✓ Risk-Szenarios Demo abgeschlossen!")
        return True
        
    except Exception as e:
        logger.error(f"Risk Demo Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_interactive_menu():
    """Interaktives Menü für Demo-Auswahl"""
    print("\n" + "="*70)
    print(" TRADING BOT - INTERAKTIVE DEMO")
    print("="*70)
    
    demos = [
        ("Trading Workflow Demo", demo_trading_workflow),
        ("Backtesting Demo", demo_backtesting),
        ("Risk Szenarien Demo", demo_risk_scenarios),
    ]
    
    while True:
        print("\nWähle eine Demo:")
        for i, (name, _) in enumerate(demos, 1):
            print(f"  {i}. {name}")
        print("  0. Alle Demos ausführen")
        print("  q. Quit")
        
        choice = input("\nEingabe: ").strip().lower()
        
        if choice == 'q':
            print("Auf Wiedersehen!")
            break
        elif choice == '0':
            for name, func in demos:
                print(f"\n{'='*70}\n")
                func()
                input("Drücke Enter für nächste Demo...")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            demos[int(choice) - 1][1]()
        else:
            print("Ungültige Eingabe")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'workflow':
            demo_trading_workflow()
        elif sys.argv[1] == 'backtest':
            demo_backtesting()
        elif sys.argv[1] == 'risk':
            demo_risk_scenarios()
    else:
        run_interactive_menu()
