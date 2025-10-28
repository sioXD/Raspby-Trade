"""
Stock Market Data Fetching Module
Fetches stock data from Yahoo Finance using yfinance library
"""

import yfinance as yf
from datetime import datetime, timedelta
import time
import pandas as pd


def fetch_stock_data(tech_list, start=None, end=None):
    """
    Fetch stock data for a list of tickers
    
    Args:
        tech_list: List of stock ticker symbols
        start: Start date (default: 5 years ago)
        end: End date (default: today)
    
    Returns:
        Dictionary of stock data DataFrames
    """
    if end is None:
        end = datetime.now()
    if start is None:
        start = end - timedelta(days=365*5)
    
    stock_data = {}
    
    for stock in tech_list:
        success = False
        for attempt in range(3):
            try:
                print(f"Fetching data for {stock} (Attempt {attempt + 1})...")
                data = yf.download(stock, start=start, end=end, threads=False)
                if not data.empty:
                    stock_data[stock] = data
                    success = True
                    break
                else:
                    print(f"No data returned for {stock}, retrying...")
            except Exception as e:
                print(f"Error fetching data for {stock}: {e}")
            time.sleep(5)
        
        if not success:
            print(f"Failed to fetch data for {stock} after 3 attempts.")
    
    return stock_data


def get_closing_prices(tech_list, start=None, end=None):
    """
    Get closing prices for multiple stocks in a single DataFrame
    
    Args:
        tech_list: List of stock ticker symbols
        start: Start date (default: 5 years ago)
        end: End date (default: today)
    
    Returns:
        DataFrame with closing prices for all stocks
    """
    if end is None:
        end = datetime.now()
    if start is None:
        start = end - timedelta(days=365*5)
    
    closingprice_df = pd.DataFrame()
    
    for stock in tech_list:
        try:
            data = yf.download(stock, start=start, end=end)
            closingprice_df[stock] = data['Close']
        except Exception as e:
            print(f"Failed to fetch data for {stock}: {e}")
    
    return closingprice_df


if __name__ == "__main__":
    # Example usage
    tech_list = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    
    # Fetch stock data
    stock_data = fetch_stock_data(tech_list)
    
    # Display Apple stock data
    if 'AAPL' in stock_data:
        print("\nAAPL Stock Data:")
        print(stock_data['AAPL'].head())
    
    # Get closing prices
    closing_prices = get_closing_prices(tech_list)
    print("\nClosing Prices:")
    print(closing_prices.head())
