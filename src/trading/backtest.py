"""
Backtest Module
Backtests trading strategy on historical data
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class BacktestEngine:
    """
    Backtest trading strategy on historical data
    """
    
    def __init__(self, initial_balance=100000, risk_per_trade=0.02):
        """
        Initialize Backtest Engine
        
        Args:
            initial_balance: Starting account balance
            risk_per_trade: Risk percentage per trade
        """
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.risk_per_trade = risk_per_trade
        
        self.logger = logging.getLogger(__name__)
        self.trades = []
        self.positions = {}
        self.daily_balances = [initial_balance]
        self.daily_returns = []
    
    def run_backtest(self, symbol, price_data, signals):
        """
        Run backtest on historical data
        
        Args:
            symbol: Stock symbol
            price_data: DataFrame with OHLCV data
            signals: DataFrame with trading signals
        
        Returns:
            Backtest results dictionary
        """
        self.logger.info(f"Starting backtest for {symbol}")
        
        # Align data and signals
        aligned_data = price_data[price_data.index.isin(signals.index)]
        aligned_signals = signals[signals.index.isin(aligned_data.index)]
        
        for i in range(len(aligned_data)):
            date = aligned_data.index[i]
            close_price = float(aligned_data.iloc[i]['Close'])
            signal = aligned_signals.iloc[i] if i < len(aligned_signals) else None
            
            # Process signal
            if signal is not None:
                if signal == 'BUY' and symbol not in self.positions:
                    self._execute_buy(symbol, date, close_price)
                elif signal == 'SELL' and symbol in self.positions:
                    self._execute_sell(symbol, date, close_price)
            
            # Check stop loss/take profit
            self._check_exits(symbol, date, close_price)
            
            # Record daily balance
            self.daily_balances.append(self.current_balance)
        
        return self._calculate_metrics()
    
    def _execute_buy(self, symbol, date, price):
        """Execute buy order in backtest"""
        risk_amount = self.current_balance * self.risk_per_trade
        qty = int(risk_amount / (price * 0.05))  # Assume 5% stop loss
        
        if qty <= 0:
            return
        
        cost = qty * price
        if cost > self.current_balance * 0.9:  # Keep 10% cash
            qty = int((self.current_balance * 0.9) / price)
        
        if qty > 0:
            self.positions[symbol] = {
                'qty': qty,
                'entry_price': price,
                'entry_date': date,
                'stop_loss': price * 0.95,
                'take_profit': price * 1.10
            }
            
            self.current_balance -= qty * price
            self.logger.info(f"{date.date()}: BUY {symbol} {qty} @ ${price:.2f}")
    
    def _execute_sell(self, symbol, date, price):
        """Execute sell order in backtest"""
        if symbol not in self.positions:
            return
        
        position = self.positions[symbol]
        qty = position['qty']
        entry_price = position['entry_price']
        
        profit = (price - entry_price) * qty
        profit_pct = (price - entry_price) / entry_price * 100
        
        self.current_balance += qty * price
        
        trade = {
            'symbol': symbol,
            'entry_date': position['entry_date'],
            'entry_price': entry_price,
            'exit_date': date,
            'exit_price': price,
            'qty': qty,
            'profit': profit,
            'profit_pct': profit_pct,
            'days_held': (date - position['entry_date']).days
        }
        
        self.trades.append(trade)
        del self.positions[symbol]
        
        self.logger.info(f"{date.date()}: SELL {symbol} {qty} @ ${price:.2f} | Profit: ${profit:.2f} ({profit_pct:.2f}%)")
    
    def _check_exits(self, symbol, date, price):
        """Check for stop loss and take profit hits"""
        if symbol not in self.positions:
            return
        
        position = self.positions[symbol]
        
        # Check stop loss
        if price <= position['stop_loss']:
            self.logger.warning(f"{date.date()}: STOP LOSS {symbol} @ ${price:.2f}")
            self._execute_sell(symbol, date, price)
        
        # Check take profit
        elif price >= position['take_profit']:
            self.logger.info(f"{date.date()}: TAKE PROFIT {symbol} @ ${price:.2f}")
            self._execute_sell(symbol, date, price)
    
    def _calculate_metrics(self):
        """Calculate backtest metrics"""
        if not self.trades:
            self.logger.warning("No trades executed in backtest")
            return None
        
        trades_df = pd.DataFrame(self.trades)
        
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['profit'] > 0])
        losing_trades = len(trades_df[trades_df['profit'] < 0])
        win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
        
        total_profit = trades_df['profit'].sum()
        avg_profit = trades_df['profit'].mean()
        max_profit = trades_df['profit'].max()
        max_loss = trades_df['profit'].min()
        
        profit_factor = (trades_df[trades_df['profit'] > 0]['profit'].sum() / 
                        abs(trades_df[trades_df['profit'] < 0]['profit'].sum())
                        if len(trades_df[trades_df['profit'] < 0]) > 0 else 0)
        
        avg_hold_days = trades_df['days_held'].mean()
        
        # Calculate Sharpe Ratio approximation
        daily_returns = np.diff(self.daily_balances) / self.daily_balances[:-1]
        sharpe_ratio = (np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)
                       if np.std(daily_returns) > 0 else 0)
        
        # Calculate Drawdown
        cumulative_balance = np.array(self.daily_balances)
        running_max = np.maximum.accumulate(cumulative_balance)
        drawdown = (cumulative_balance - running_max) / running_max
        max_drawdown = np.min(drawdown) * 100
        
        final_balance = self.current_balance
        total_return = (final_balance - self.initial_balance) / self.initial_balance * 100
        
        metrics = {
            'initial_balance': self.initial_balance,
            'final_balance': final_balance,
            'total_profit': total_profit,
            'total_return_pct': total_return,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate_pct': win_rate,
            'avg_profit': avg_profit,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'profit_factor': profit_factor,
            'avg_hold_days': avg_hold_days,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown_pct': max_drawdown,
            'trades': trades_df
        }
        
        return metrics
    
    def print_metrics(self, metrics):
        """Print backtest metrics"""
        if metrics is None:
            print("No metrics to display")
            return
        
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)
        print(f"Initial Balance:     ${metrics['initial_balance']:,.2f}")
        print(f"Final Balance:       ${metrics['final_balance']:,.2f}")
        print(f"Total Profit:        ${metrics['total_profit']:,.2f}")
        print(f"Total Return:        {metrics['total_return_pct']:.2f}%")
        print()
        print(f"Total Trades:        {metrics['total_trades']}")
        print(f"Winning Trades:      {metrics['winning_trades']}")
        print(f"Losing Trades:       {metrics['losing_trades']}")
        print(f"Win Rate:            {metrics['win_rate_pct']:.2f}%")
        print()
        print(f"Avg Profit/Trade:    ${metrics['avg_profit']:,.2f}")
        print(f"Max Profit:          ${metrics['max_profit']:,.2f}")
        print(f"Max Loss:            ${metrics['max_loss']:,.2f}")
        print(f"Profit Factor:       {metrics['profit_factor']:.2f}")
        print()
        print(f"Avg Hold Days:       {metrics['avg_hold_days']:.1f}")
        print(f"Sharpe Ratio:        {metrics['sharpe_ratio']:.2f}")
        print(f"Max Drawdown:        {metrics['max_drawdown_pct']:.2f}%")
        print("="*60 + "\n")
        
        # Print top trades
        trades = metrics['trades']
        print("TOP 5 WINNING TRADES:")
        top_winners = trades.nlargest(5, 'profit')[['entry_date', 'symbol', 'entry_price', 
                                                      'exit_price', 'profit', 'profit_pct']]
        print(top_winners.to_string())
        print()
        
        print("TOP 5 LOSING TRADES:")
        top_losers = trades.nsmallest(5, 'profit')[['entry_date', 'symbol', 'entry_price', 
                                                     'exit_price', 'profit', 'profit_pct']]
        print(top_losers.to_string())
    
    def export_results(self, filename='backtest_results.csv'):
        """Export backtest results to CSV"""
        try:
            trades_df = pd.DataFrame(self.trades)
            trades_df.to_csv(filename, index=False)
            self.logger.info(f"Results exported to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting results: {e}")
            return False


class MultiSymbolBacktest:
    """Backtest multiple symbols simultaneously"""
    
    def __init__(self, initial_balance=100000, risk_per_trade=0.02):
        """Initialize multi-symbol backtest"""
        self.engine = BacktestEngine(initial_balance, risk_per_trade)
        self.results = {}
    
    def run_backtest_multiple(self, data_dict, signals_dict):
        """
        Run backtest for multiple symbols
        
        Args:
            data_dict: Dictionary of {symbol: price_data}
            signals_dict: Dictionary of {symbol: signals}
        
        Returns:
            Dictionary of results for each symbol
        """
        for symbol in data_dict.keys():
            if symbol in signals_dict:
                results = self.engine.run_backtest(
                    symbol,
                    data_dict[symbol],
                    signals_dict[symbol]
                )
                self.results[symbol] = results
        
        return self.results
    
    def print_summary(self):
        """Print summary of all backtests"""
        print("\n" + "="*60)
        print("BACKTEST SUMMARY - MULTIPLE SYMBOLS")
        print("="*60)
        
        for symbol, metrics in self.results.items():
            if metrics:
                print(f"\n{symbol}:")
                print(f"  Return: {metrics['total_return_pct']:>7.2f}%")
                print(f"  Trades: {metrics['total_trades']:>7}")
                print(f"  Win %:  {metrics['win_rate_pct']:>7.2f}%")
                print(f"  Sharpe: {metrics['sharpe_ratio']:>7.2f}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    engine = BacktestEngine(initial_balance=100000)
    
    # Create sample data
    dates = pd.date_range('2023-01-01', periods=100)
    prices = 150 + np.cumsum(np.random.randn(100))
    price_data = pd.DataFrame({'Close': prices}, index=dates)
    
    # Create sample signals
    signals = pd.Series(['BUY' if i % 20 == 0 else ('SELL' if i % 10 == 0 else None) 
                        for i in range(100)], index=dates)
    
    # Run backtest
    results = engine.run_backtest('AAPL', price_data, signals)
    engine.print_metrics(results)
