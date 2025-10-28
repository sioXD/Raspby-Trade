"""
Trading Engine Module
Handles all trading logic and order management with Alpaca API
"""

import os
import time
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

try:
    import alpaca_trade_api as tradeapi
    ALPACA_AVAILABLE = True
except ImportError:
    ALPACA_AVAILABLE = False
    logging.warning("Alpaca Trade API not installed. Using mock mode.")


class TradingEngine:
    """
    Main Trading Engine for executing trades based on predictions
    Supports both Paper Trading (simulated) and Real Trading
    """
    
    def __init__(self, api_key=None, secret_key=None, use_paper_trading=True):
        """
        Initialize Trading Engine
        
        Args:
            api_key: Alpaca API Key
            secret_key: Alpaca Secret Key
            use_paper_trading: Use paper trading (simulated) or real trading
        """
        self.use_paper_trading = use_paper_trading
        self.api = None
        self.account = None
        self.positions = {}
        self.trades_log = []
        
        self.logger = logging.getLogger(__name__)
        
        if ALPACA_AVAILABLE and api_key and secret_key:
            try:
                base_url = 'https://paper-api.alpaca.markets' if use_paper_trading \
                           else 'https://api.alpaca.markets'
                
                self.api = tradeapi.REST(
                    api_key,
                    secret_key,
                    base_url,
                    api_version='v2'
                )
                
                self.account = self.api.get_account()
                self.logger.info(f"Connected to Alpaca. Mode: {'Paper' if use_paper_trading else 'Real'}")
                self.logger.info(f"Account Balance: ${self.account.buying_power}")
                
            except Exception as e:
                self.logger.error(f"Failed to connect to Alpaca: {e}")
                self.api = None
        else:
            self.logger.warning("Using mock trading mode (no real orders will be executed)")
    
    def get_account_info(self):
        """Get current account information"""
        if self.api:
            try:
                self.account = self.api.get_account()
                return {
                    'buying_power': float(self.account.buying_power),
                    'portfolio_value': float(self.account.portfolio_value),
                    'cash': float(self.account.cash),
                    'buying_power': float(self.account.buying_power)
                }
            except Exception as e:
                self.logger.error(f"Error getting account info: {e}")
                return None
        else:
            return {
                'buying_power': 100000.0,  # Mock value
                'portfolio_value': 100000.0,
                'cash': 100000.0
            }
    
    def get_positions(self):
        """Get all open positions"""
        if self.api:
            try:
                positions = self.api.list_positions()
                self.positions = {p.symbol: {
                    'qty': int(p.qty),
                    'entry_price': float(p.avg_entry_price),
                    'current_price': float(p.current_price),
                    'unrealized_pl': float(p.unrealized_pl),
                    'unrealized_plpc': float(p.unrealized_plpc)
                } for p in positions}
                return self.positions
            except Exception as e:
                self.logger.error(f"Error getting positions: {e}")
                return {}
        return self.positions
    
    def execute_buy_order(self, symbol, qty, order_type='market', limit_price=None):
        """
        Execute a buy order
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            qty: Quantity to buy
            order_type: 'market' or 'limit'
            limit_price: Price limit for limit orders
        
        Returns:
            Order details or None if failed
        """
        try:
            self.logger.info(f"Executing BUY order: {qty} {symbol}")
            
            if self.api:
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side='buy',
                    type=order_type,
                    time_in_force='gtc',  # Good till cancelled
                    limit_price=limit_price if order_type == 'limit' else None
                )
                
                order_info = {
                    'id': order.id,
                    'symbol': order.symbol,
                    'qty': int(order.qty),
                    'side': order.side,
                    'price': float(order.filled_avg_price) if order.filled_avg_price else None,
                    'status': order.status,
                    'timestamp': datetime.now()
                }
                
                self.trades_log.append(order_info)
                self.logger.info(f"Order executed: {order_info}")
                return order_info
            else:
                # Mock order
                order_info = {
                    'id': f"mock_{symbol}_{datetime.now().timestamp()}",
                    'symbol': symbol,
                    'qty': qty,
                    'side': 'buy',
                    'price': limit_price if order_type == 'limit' else None,
                    'status': 'filled',
                    'timestamp': datetime.now()
                }
                self.trades_log.append(order_info)
                self.logger.info(f"Mock BUY order: {order_info}")
                return order_info
                
        except Exception as e:
            self.logger.error(f"Error executing buy order: {e}")
            return None
    
    def execute_sell_order(self, symbol, qty, order_type='market', limit_price=None):
        """
        Execute a sell order
        
        Args:
            symbol: Stock symbol
            qty: Quantity to sell
            order_type: 'market' or 'limit'
            limit_price: Price limit for limit orders
        
        Returns:
            Order details or None if failed
        """
        try:
            self.logger.info(f"Executing SELL order: {qty} {symbol}")
            
            if self.api:
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side='sell',
                    type=order_type,
                    time_in_force='gtc',
                    limit_price=limit_price if order_type == 'limit' else None
                )
                
                order_info = {
                    'id': order.id,
                    'symbol': order.symbol,
                    'qty': int(order.qty),
                    'side': order.side,
                    'price': float(order.filled_avg_price) if order.filled_avg_price else None,
                    'status': order.status,
                    'timestamp': datetime.now()
                }
                
                self.trades_log.append(order_info)
                self.logger.info(f"Order executed: {order_info}")
                return order_info
            else:
                # Mock order
                order_info = {
                    'id': f"mock_{symbol}_{datetime.now().timestamp()}",
                    'symbol': symbol,
                    'qty': qty,
                    'side': 'sell',
                    'price': limit_price if order_type == 'limit' else None,
                    'status': 'filled',
                    'timestamp': datetime.now()
                }
                self.trades_log.append(order_info)
                self.logger.info(f"Mock SELL order: {order_info}")
                return order_info
                
        except Exception as e:
            self.logger.error(f"Error executing sell order: {e}")
            return None
    
    def check_open_orders(self):
        """Check all open orders"""
        if self.api:
            try:
                orders = self.api.list_orders(status='open')
                return [{'symbol': o.symbol, 'qty': o.qty, 'side': o.side, 'status': o.status} 
                        for o in orders]
            except Exception as e:
                self.logger.error(f"Error checking orders: {e}")
                return []
        return []
    
    def cancel_order(self, order_id):
        """Cancel an open order"""
        if self.api:
            try:
                self.api.cancel_order(order_id)
                self.logger.info(f"Order {order_id} cancelled")
                return True
            except Exception as e:
                self.logger.error(f"Error cancelling order: {e}")
                return False
        return False
    
    def close_position(self, symbol):
        """Close a position by selling all shares"""
        try:
            positions = self.get_positions()
            if symbol in positions:
                qty = positions[symbol]['qty']
                return self.execute_sell_order(symbol, qty)
            else:
                self.logger.warning(f"No position in {symbol} to close")
                return None
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
            return None
    
    def get_trades_log(self):
        """Get log of all trades executed"""
        return self.trades_log
    
    def export_trades_to_csv(self, filename='trades.csv'):
        """Export trades log to CSV"""
        try:
            df = pd.DataFrame(self.trades_log)
            df.to_csv(filename, index=False)
            self.logger.info(f"Trades exported to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting trades: {e}")
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage (mock mode)
    engine = TradingEngine(use_paper_trading=True)
    
    # Get account info
    account = engine.get_account_info()
    print("Account Info:", account)
    
    # Execute mock trades
    buy_order = engine.execute_buy_order('AAPL', 10)
    print("Buy Order:", buy_order)
    
    sell_order = engine.execute_sell_order('AAPL', 5)
    print("Sell Order:", sell_order)
    
    # Get trades log
    trades = engine.get_trades_log()
    print("Trades Log:", trades)
