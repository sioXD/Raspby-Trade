"""
Stock Market Analysis Module
Provides functions for basic stock analysis including moving averages and daily returns
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tkinter errors
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')


def calculate_moving_averages(stock_data, ma_days=[10, 20, 50, 100]):
    """
    Calculate moving averages for stock data
    
    Args:
        stock_data: DataFrame with stock data
        ma_days: List of days for moving averages
    
    Returns:
        DataFrame with added moving average columns
    """
    df = stock_data.copy()
    
    for ma in ma_days:
        column_name = f"MA for {ma} days"
        df[column_name] = df['Close'].rolling(window=ma).mean()
    
    return df


def calculate_daily_returns(stock_data):
    """
    Calculate daily returns for stock data
    
    Args:
        stock_data: DataFrame with stock data
    
    Returns:
        DataFrame with added 'Daily Return' column
    """
    df = stock_data.copy()
    df['Daily Return'] = df['Close'].pct_change()
    return df


def plot_closing_price(stock_data, stock_name='Stock'):
    """
    Plot closing price over time
    
    Args:
        stock_data: DataFrame with stock data
        stock_name: Name of the stock for plot title
    """
    plt.figure(figsize=(10, 4))
    stock_data['Close'].plot(legend=True)
    plt.title(f'{stock_name} Closing Price')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.show()


def plot_volume(stock_data, stock_name='Stock'):
    """
    Plot trading volume over time
    
    Args:
        stock_data: DataFrame with stock data
        stock_name: Name of the stock for plot title
    """
    plt.figure(figsize=(10, 4))
    stock_data['Volume'].plot(legend=True)
    plt.title(f'{stock_name} Trading Volume')
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.show()


def plot_moving_averages(stock_data, ma_days=[10, 20, 50, 100], stock_name='Stock'):
    """
    Plot closing price with moving averages
    
    Args:
        stock_data: DataFrame with stock data and moving averages
        ma_days: List of days for moving averages to plot
        stock_name: Name of the stock for plot title
    """
    columns_to_plot = ['Close'] + [f'MA for {ma} days' for ma in ma_days]
    
    plt.figure(figsize=(10, 4))
    stock_data[columns_to_plot].plot(subplots=False)
    plt.title(f'{stock_name} Price with Moving Averages')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.show()


def plot_daily_returns(stock_data, stock_name='Stock'):
    """
    Plot daily returns
    
    Args:
        stock_data: DataFrame with stock data including daily returns
        stock_name: Name of the stock for plot title
    """
    plt.figure(figsize=(12, 4))
    stock_data['Daily Return'].plot(legend=True, linestyle='--', marker='o')
    plt.title(f'{stock_name} Daily Returns')
    plt.ylabel('Daily Return')
    plt.xlabel('Date')
    plt.show()


def plot_returns_histogram(stock_data, bins=100, stock_name='Stock'):
    """
    Plot histogram of daily returns
    
    Args:
        stock_data: DataFrame with stock data including daily returns
        bins: Number of bins for histogram
        stock_name: Name of the stock for plot title
    """
    plt.figure(figsize=(10, 6))
    stock_data['Daily Return'].hist(bins=bins)
    plt.title(f'{stock_name} Daily Returns Distribution')
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    plt.show()


def plot_returns_distribution(stock_data, bins=100, color='magenta', stock_name='Stock'):
    """
    Plot distribution of daily returns with KDE
    
    Args:
        stock_data: DataFrame with stock data including daily returns
        bins: Number of bins for histogram
        color: Color for the plot
        stock_name: Name of the stock for plot title
    """
    sns.displot(stock_data['Daily Return'].dropna(), bins=bins, color=color)
    plt.title(f'{stock_name} Daily Returns Distribution')
    plt.show()


if __name__ == "__main__":
    from data_fetching import fetch_stock_data
    
    # Example usage
    tech_list = ['AAPL']
    stock_data = fetch_stock_data(tech_list)
    
    if 'AAPL' in stock_data:
        aapl = stock_data['AAPL']
        
        # Calculate moving averages
        aapl = calculate_moving_averages(aapl)
        print("\nStock data with moving averages:")
        print(aapl.head())
        
        # Calculate daily returns
        aapl = calculate_daily_returns(aapl)
        
        # Plot analysis
        plot_closing_price(aapl, 'AAPL')
        plot_volume(aapl, 'AAPL')
        plot_moving_averages(aapl, stock_name='AAPL')
        plot_daily_returns(aapl, 'AAPL')
        plot_returns_histogram(aapl, stock_name='AAPL')
