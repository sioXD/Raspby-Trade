#!/usr/bin/env python3
"""Test API connection"""

from src.env_loader import init_env, get as env_get
from pi_bot_main import RaspberryPiTradingBot

init_env()
bot = RaspberryPiTradingBot()

# Check if config was loaded correctly
config = bot.config['trading']
api_key = config.get('api_key')
secret_key = config.get('secret_key')

print(f'API Key from config: {api_key[:10]}...' if api_key else 'NO API KEY')
print(f'Secret Key from config: {secret_key[:10]}...' if secret_key else 'NO SECRET KEY')

# Check if trading engine has API connection
print(f'Trading Engine API connected: {bot.trading_engine.api is not None}')

if bot.trading_engine.api:
    account_info = bot.trading_engine.get_account_info()
    print(f'Account: {account_info}')
    
    # Try to execute a test order
    print("\nExecuting TEST order...")
    order = bot.trading_engine.execute_buy_order('AAPL', 1)
    print(f'Order Result: {order}')
else:
    print('ERROR: Trading engine is NOT connected!')
