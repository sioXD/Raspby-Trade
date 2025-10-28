"""
Risk Manager Module
Manages position sizing, stop losses, and risk controls
"""

import logging
import numpy as np
from datetime import datetime


class RiskManager:
    """
    Manages risk for trading strategy
    - Position sizing
    - Stop loss/Take profit levels
    - Maximum loss per trade
    - Portfolio risk limits
    """
    
    def __init__(self, account_balance, risk_per_trade=0.02, max_positions=5):
        """
        Initialize Risk Manager
        
        Args:
            account_balance: Total account balance in dollars
            risk_per_trade: Risk percentage per trade (default 2%)
            max_positions: Maximum number of open positions
        """
        self.account_balance = account_balance
        self.risk_per_trade = risk_per_trade
        self.max_positions = max_positions
        self.open_positions = {}
        self.total_risk_exposure = 0.0
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Risk Manager initialized. Account: ${account_balance:.2f}, Risk/Trade: {risk_per_trade*100}%")
    
    def calculate_position_size(self, entry_price, stop_loss_price):
        """
        Calculate position size based on risk
        
        Args:
            entry_price: Entry price
            stop_loss_price: Stop loss price
        
        Returns:
            Position size (number of shares)
        """
        risk_amount = self.account_balance * self.risk_per_trade
        price_risk = abs(entry_price - stop_loss_price)
        
        if price_risk == 0:
            self.logger.warning("Price risk is 0, returning 0 position size")
            return 0
        
        position_size = int(risk_amount / price_risk)
        
        self.logger.info(f"Position Size: {position_size} shares (Risk: ${risk_amount:.2f})")
        return position_size
    
    def calculate_stop_loss(self, entry_price, stop_loss_pct=0.05):
        """
        Calculate stop loss price
        
        Args:
            entry_price: Entry price
            stop_loss_pct: Stop loss percentage (default 5%)
        
        Returns:
            Stop loss price
        """
        stop_loss = entry_price * (1 - stop_loss_pct)
        self.logger.info(f"Stop Loss: ${stop_loss:.2f} ({stop_loss_pct*100}%)")
        return stop_loss
    
    def calculate_take_profit(self, entry_price, take_profit_pct=0.10):
        """
        Calculate take profit price
        
        Args:
            entry_price: Entry price
            take_profit_pct: Take profit percentage (default 10%)
        
        Returns:
            Take profit price
        """
        take_profit = entry_price * (1 + take_profit_pct)
        self.logger.info(f"Take Profit: ${take_profit:.2f} ({take_profit_pct*100}%)")
        return take_profit
    
    def can_open_position(self, symbol):
        """
        Check if we can open a new position
        
        Args:
            symbol: Stock symbol
        
        Returns:
            True if position can be opened, False otherwise
        """
        # Check if max positions reached
        if len(self.open_positions) >= self.max_positions:
            self.logger.warning(f"Max positions ({self.max_positions}) reached")
            return False
        
        # Check if symbol already has open position
        if symbol in self.open_positions:
            self.logger.warning(f"Position in {symbol} already exists")
            return False
        
        return True
    
    def add_position(self, symbol, qty, entry_price, stop_loss, take_profit):
        """
        Add a new open position
        
        Args:
            symbol: Stock symbol
            qty: Quantity
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
        """
        position = {
            'symbol': symbol,
            'qty': qty,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'entry_time': datetime.now(),
            'initial_balance': self.account_balance,
            'max_loss': qty * (entry_price - stop_loss)
        }
        
        self.open_positions[symbol] = position
        risk = qty * (entry_price - stop_loss)
        self.total_risk_exposure += risk
        
        self.logger.info(f"Position added: {symbol}, Qty: {qty}, Entry: ${entry_price:.2f}, "
                        f"SL: ${stop_loss:.2f}, TP: ${take_profit:.2f}")
    
    def remove_position(self, symbol):
        """Remove a closed position"""
        if symbol in self.open_positions:
            position = self.open_positions[symbol]
            risk = position['qty'] * (position['entry_price'] - position['stop_loss'])
            self.total_risk_exposure -= risk
            del self.open_positions[symbol]
            self.logger.info(f"Position removed: {symbol}")
        else:
            self.logger.warning(f"Position {symbol} not found")
    
    def check_stop_loss(self, symbol, current_price):
        """
        Check if stop loss is hit
        
        Args:
            symbol: Stock symbol
            current_price: Current price
        
        Returns:
            True if stop loss hit, False otherwise
        """
        if symbol in self.open_positions:
            position = self.open_positions[symbol]
            if current_price <= position['stop_loss']:
                self.logger.warning(f"STOP LOSS HIT: {symbol} at ${current_price:.2f}")
                return True
        return False
    
    def check_take_profit(self, symbol, current_price):
        """
        Check if take profit is reached
        
        Args:
            symbol: Stock symbol
            current_price: Current price
        
        Returns:
            True if take profit reached, False otherwise
        """
        if symbol in self.open_positions:
            position = self.open_positions[symbol]
            if current_price >= position['take_profit']:
                self.logger.warning(f"TAKE PROFIT REACHED: {symbol} at ${current_price:.2f}")
                return True
        return False
    
    def get_position_info(self, symbol):
        """Get information about a position"""
        if symbol in self.open_positions:
            return self.open_positions[symbol]
        return None
    
    def get_all_positions(self):
        """Get all open positions"""
        return self.open_positions
    
    def get_risk_exposure(self):
        """Get total risk exposure"""
        risk_pct = (self.total_risk_exposure / self.account_balance) * 100
        self.logger.info(f"Total Risk Exposure: ${self.total_risk_exposure:.2f} ({risk_pct:.2f}%)")
        return {
            'total_risk': self.total_risk_exposure,
            'risk_percentage': risk_pct,
            'account_balance': self.account_balance,
            'max_allowed_risk': self.account_balance * self.risk_per_trade * self.max_positions
        }
    
    def update_account_balance(self, new_balance):
        """Update account balance"""
        self.account_balance = new_balance
        self.logger.info(f"Account balance updated: ${new_balance:.2f}")
    
    def get_drawdown(self):
        """Calculate current drawdown"""
        if not self.open_positions:
            return 0.0
        
        total_unrealized_loss = 0
        for position in self.open_positions.values():
            loss = position['max_loss']
            total_unrealized_loss += loss
        
        drawdown_pct = (total_unrealized_loss / self.account_balance) * 100
        return drawdown_pct
    
    def validate_trade(self, symbol, qty, entry_price, stop_loss_price):
        """
        Validate if a trade meets risk criteria
        
        Args:
            symbol: Stock symbol
            qty: Quantity
            entry_price: Entry price
            stop_loss_price: Stop loss price
        
        Returns:
            Tuple (is_valid, message)
        """
        # Check if position can be opened
        if not self.can_open_position(symbol):
            return False, f"Cannot open position in {symbol}"
        
        # Check risk per trade
        risk_amount = qty * abs(entry_price - stop_loss_price)
        max_risk = self.account_balance * self.risk_per_trade
        
        if risk_amount > max_risk:
            return False, f"Risk (${risk_amount:.2f}) exceeds max (${max_risk:.2f})"
        
        # Check total exposure
        total_risk = self.total_risk_exposure + risk_amount
        max_total_risk = self.account_balance * self.risk_per_trade * self.max_positions
        
        if total_risk > max_total_risk:
            return False, f"Total risk would exceed maximum"
        
        return True, "Trade validated"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    rm = RiskManager(account_balance=100000, risk_per_trade=0.02)
    
    # Calculate position size
    pos_size = rm.calculate_position_size(entry_price=150, stop_loss_price=142.5)
    
    # Calculate stops
    sl = rm.calculate_stop_loss(entry_price=150, stop_loss_pct=0.05)
    tp = rm.calculate_take_profit(entry_price=150, take_profit_pct=0.10)
    
    # Validate trade
    is_valid, msg = rm.validate_trade('AAPL', pos_size, 150, sl)
    print(f"Trade valid: {is_valid}, Message: {msg}")
    
    # Add position
    if is_valid:
        rm.add_position('AAPL', pos_size, 150, sl, tp)
    
    # Check risk exposure
    exposure = rm.get_risk_exposure()
    print(f"Risk Exposure: {exposure}")
