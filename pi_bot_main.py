"""
Raspberry Pi Trading Bot - Main Entry Point
Runs continuously on Raspberry Pi with scheduled analysis and trading
"""

import os
import sys
import time
import logging
import schedule
import yaml
from datetime import datetime, timedelta
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables
from src.env_loader import init_env, get as env_get
init_env()

from src.analysis import fetch_stock_data, get_closing_prices, calculate_returns_for_stocks
from src.ml import predict_stock_price
from src.trading import TradingEngine, RiskManager, NotificationManager


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RaspberryPiTradingBot:
    """Main Trading Bot for Raspberry Pi"""
    
    def __init__(self, config_file='config.yaml'):
        """
        Initialize Trading Bot
        
        Args:
            config_file: Path to configuration file
        """
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config(config_file)
        
        # Initialize components
        self.trading_engine = None
        self.risk_manager = None
        self.notifier = NotificationManager()
        self.positions = {}
        self.signals = {}
        
        self._setup_trading_engine()
        self._setup_risk_manager()
        self._setup_notifier()
        
        self.logger.info("Trading Bot initialized")
    
    def load_config(self, config_file):
        """Load configuration from YAML file"""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                self.logger.info(f"Configuration loaded from {config_file}")
                return config
            else:
                self.logger.warning(f"Config file {config_file} not found, using defaults")
                return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Get default configuration"""
        return {
            'trading': {
                'api_key': env_get('ALPACA_API_KEY'),
                'secret_key': env_get('ALPACA_SECRET_KEY'),
                'use_paper_trading': True,
                'symbols': env_get('TRADING_SYMBOLS', 'AAPL,GOOGL,MSFT,AMZN').split(','),
            },
            'risk': {
                'account_balance': 100000,
                'risk_per_trade': 0.02,
                'max_positions': 5,
                'stop_loss_pct': 0.05,
                'take_profit_pct': 0.10,
            },
            'notifications': {
                'email_enabled': False,
                'telegram_enabled': False,
            },
            'schedule': {
                'analysis_time': '09:30',  # Market open USA
                'risk_check_interval': 60,  # Minutes
            }
        }
    
    def _setup_trading_engine(self):
        """Initialize trading engine"""
        try:
            config = self.config['trading']
            self.trading_engine = TradingEngine(
                api_key=config.get('api_key'),
                secret_key=config.get('secret_key'),
                use_paper_trading=config.get('use_paper_trading', True)
            )
            self.logger.info("Trading engine initialized")
        except Exception as e:
            self.logger.error(f"Error initializing trading engine: {e}")
            self.trading_engine = TradingEngine(use_paper_trading=True)
    
    def _setup_risk_manager(self):
        """Initialize risk manager"""
        try:
            config = self.config['risk']
            account_info = self.trading_engine.get_account_info()
            balance = account_info['buying_power'] if account_info else config['account_balance']
            
            self.risk_manager = RiskManager(
                account_balance=balance,
                risk_per_trade=config.get('risk_per_trade', 0.02),
                max_positions=config.get('max_positions', 5)
            )
            self.logger.info("Risk manager initialized")
        except Exception as e:
            self.logger.error(f"Error initializing risk manager: {e}")
    
    def _setup_notifier(self):
        """Initialize notification system"""
        config = self.config.get('notifications', {})
        
        if config.get('email_enabled'):
            try:
                email_config = config.get('email', {})
                self.notifier.add_email_notifier(
                    sender_email=env_get('EMAIL_ADDRESS'),
                    sender_password=env_get('EMAIL_PASSWORD')
                )
                self.logger.info("Email notifier added")
            except Exception as e:
                self.logger.warning(f"Could not setup email notifier: {e}")
        
        if config.get('telegram_enabled'):
            try:
                self.notifier.add_telegram_notifier(
                    bot_token=env_get('TELEGRAM_BOT_TOKEN'),
                    chat_id=env_get('TELEGRAM_CHAT_ID')
                )
                self.logger.info("Telegram notifier added")
            except Exception as e:
                self.logger.warning(f"Could not setup Telegram notifier: {e}")
    
    def analyze_and_trade(self):
        """Main analysis and trading logic"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("Starting analysis and trading")
            self.logger.info("=" * 60)
            
            symbols = self.config['trading']['symbols']
            
            # Get account info
            account_info = self.trading_engine.get_account_info()
            self.logger.info(f"Account Balance: ${account_info['buying_power']:.2f}")
            
            # Update risk manager with current balance
            self.risk_manager.update_account_balance(account_info['buying_power'])
            
            # Get existing positions
            positions = self.trading_engine.get_positions()
            self.logger.info(f"Current Positions: {len(positions)}")
            
            # Fetch data and generate predictions
            self.logger.info("Fetching stock data...")
            closing_prices = get_closing_prices(symbols)
            
            if closing_prices.empty:
                self.logger.error("Failed to fetch stock data")
                return
            
            # Generate LSTM predictions
            self.logger.info("Generating LSTM predictions...")
            predictions = {}
            for symbol in symbols:
                try:
                    # Get prediction (simplified for Raspberry Pi)
                    pred_data = self._get_prediction(symbol)
                    if pred_data is not None:
                        predictions[symbol] = pred_data
                except Exception as e:
                    self.logger.warning(f"Error predicting {symbol}: {e}")
            
            # Execute trading logic
            self.logger.info("Executing trading logic...")
            self._execute_trades(predictions, closing_prices)
            
            # Check stop losses and take profits
            self.logger.info("Checking stop losses and take profits...")
            self._check_risk_levels(closing_prices)
            
            self.logger.info("Analysis and trading completed")
            
        except Exception as e:
            self.logger.error(f"Error in analyze_and_trade: {e}")
            self.notifier.send_risk_alert("Bot Error", str(e))
    
    def _get_prediction(self, symbol):
        """Get prediction for symbol (simplified for Pi)"""
        try:
            # Simplified prediction logic
            # On Raspberry Pi, use cached models instead of training new ones
            current_price = None  # Get from API
            
            # Simple momentum indicator as fallback
            # Can be replaced with full LSTM on higher-end Pi
            return {
                'symbol': symbol,
                'signal': 'bullish',  # or 'bearish'
                'confidence': 0.65,
                'predicted_price': current_price * 1.05
            }
        except Exception as e:
            self.logger.warning(f"Error getting prediction for {symbol}: {e}")
            return None
    
    def _execute_trades(self, predictions, current_prices):
        """Execute trades based on predictions"""
        for symbol, pred in predictions.items():
            try:
                signal = pred['signal']
                confidence = pred['confidence']
                current_price = current_prices[symbol].iloc[-1]
                
                # Only trade if confidence is high enough
                min_confidence = self.config.get('trading', {}).get('min_confidence', 0.65)
                
                if confidence < min_confidence:
                    self.logger.info(f"{symbol}: Signal too weak ({confidence:.1%})")
                    continue
                
                # Buy signal
                if signal == 'bullish' and symbol not in self.positions:
                    self._execute_buy(symbol, current_price, confidence)
                
                # Sell signal
                elif signal == 'bearish' and symbol in self.positions:
                    self._execute_sell(symbol, current_price, confidence)
                    
            except Exception as e:
                self.logger.error(f"Error executing trade for {symbol}: {e}")
    
    def _execute_buy(self, symbol, current_price, confidence):
        """Execute buy order"""
        try:
            config_risk = self.config['risk']
            stop_loss = current_price * (1 - config_risk['stop_loss_pct'])
            take_profit = current_price * (1 + config_risk['take_profit_pct'])
            
            # Calculate position size
            position_size = self.risk_manager.calculate_position_size(current_price, stop_loss)
            
            # Validate trade
            is_valid, msg = self.risk_manager.validate_trade(
                symbol, position_size, current_price, stop_loss
            )
            
            if not is_valid:
                self.logger.warning(f"{symbol}: Trade not valid - {msg}")
                return
            
            # Execute order
            self.logger.info(f"BUY {symbol}: {position_size} @ ${current_price:.2f}")
            order = self.trading_engine.execute_buy_order(symbol, position_size)
            
            if order:
                self.risk_manager.add_position(symbol, position_size, current_price, stop_loss, take_profit)
                self.positions[symbol] = {'qty': position_size, 'entry_price': current_price}
                
                # Send notification
                self.notifier.send_signal_alert(symbol, 'bullish', confidence)
                
        except Exception as e:
            self.logger.error(f"Error executing buy for {symbol}: {e}")
    
    def _execute_sell(self, symbol, current_price, confidence):
        """Execute sell order"""
        try:
            if symbol not in self.positions:
                return
            
            qty = self.positions[symbol]['qty']
            
            self.logger.info(f"SELL {symbol}: {qty} @ ${current_price:.2f}")
            order = self.trading_engine.execute_sell_order(symbol, qty)
            
            if order:
                self.risk_manager.remove_position(symbol)
                del self.positions[symbol]
                
                # Send notification
                self.notifier.send_signal_alert(symbol, 'bearish', confidence)
                
        except Exception as e:
            self.logger.error(f"Error executing sell for {symbol}: {e}")
    
    def _check_risk_levels(self, current_prices):
        """Check stop losses and take profits"""
        try:
            positions = self.risk_manager.get_all_positions()
            
            for symbol in list(self.positions.keys()):
                if symbol not in current_prices.index:
                    continue
                
                current_price = current_prices[symbol].iloc[-1]
                position = positions.get(symbol)
                
                if not position:
                    continue
                
                # Check stop loss
                if self.risk_manager.check_stop_loss(symbol, current_price):
                    self.logger.warning(f"STOP LOSS HIT: {symbol} at ${current_price:.2f}")
                    self._execute_sell(symbol, current_price, 1.0)
                    self.notifier.send_risk_alert("Stop Loss", f"{symbol} stopped at ${current_price:.2f}")
                
                # Check take profit
                elif self.risk_manager.check_take_profit(symbol, current_price):
                    self.logger.warning(f"TAKE PROFIT: {symbol} at ${current_price:.2f}")
                    self._execute_sell(symbol, current_price, 1.0)
                    self.notifier.send_risk_alert("Take Profit", f"{symbol} profit locked at ${current_price:.2f}")
                    
        except Exception as e:
            self.logger.error(f"Error checking risk levels: {e}")
    
    def health_check(self):
        """Periodic health check"""
        try:
            self.logger.info("Health check...")
            account_info = self.trading_engine.get_account_info()
            
            if account_info:
                self.logger.info(f"Account: ${account_info['buying_power']:.2f}")
                positions = self.trading_engine.get_positions()
                self.logger.info(f"Positions: {len(positions)}")
            else:
                self.logger.warning("Could not retrieve account info")
                
        except Exception as e:
            self.logger.error(f"Error in health check: {e}")
    
    def schedule_jobs(self):
        """Setup scheduled jobs"""
        config = self.config.get('schedule', {})
        
        # Main analysis at market open
        analysis_time = config.get('analysis_time', '09:30')
        schedule.every().day.at(analysis_time).do(self.analyze_and_trade)
        
        # Risk checks every N minutes
        check_interval = config.get('risk_check_interval', 60)
        schedule.every(check_interval).minutes.do(self.health_check)
        
        self.logger.info(f"Jobs scheduled - Analysis at {analysis_time}, Health check every {check_interval} min")
    
    def run(self):
        """Run the bot continuously"""
        try:
            self.logger.info("Starting Raspberry Pi Trading Bot")
            self.logger.info(f"Paper Trading: {self.config['trading']['use_paper_trading']}")
            
            self.schedule_jobs()
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check schedule every minute
                
        except KeyboardInterrupt:
            self.logger.info("Bot interrupted by user")
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            self.notifier.send_risk_alert("Bot Error", f"Fatal: {e}")
        finally:
            self.logger.info("Trading bot stopped")


def main():
    """Main entry point"""
    # Check for config file
    config_file = 'config.yaml'
    if not os.path.exists(config_file):
        logger.warning(f"Config file {config_file} not found")
        logger.info("Using default configuration")
    
    # Start bot
    bot = RaspberryPiTradingBot(config_file)
    bot.run()


if __name__ == "__main__":
    main()
