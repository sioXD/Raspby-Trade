"""
Stock Risk Analysis Module
Analyzes risk using various metrics including VaR
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tkinter errors
import matplotlib.pyplot as plt
import seaborn as sns


def plot_risk_return_scatter(tech_returns):
    """
    Plot risk vs return scatter plot
    
    Args:
        tech_returns: DataFrame with returns for all stocks
    """
    rets = tech_returns.dropna()
    
    area = np.pi * 20
    
    plt.figure(figsize=(10, 6))
    plt.scatter(rets.mean(), rets.std(), s=area)
    
    plt.xlim([-0.0025, 0.0025])
    plt.ylim([0.001, 0.025])
    
    plt.xlabel('Expected Returns')
    plt.ylabel('Risk (Standard Deviation)')
    plt.title('Risk vs Expected Returns')
    
    for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
        plt.annotate(
            label,
            xy=(x, y), xytext=(50, 50),
            textcoords='offset points', ha='right', va='bottom',
            arrowprops=dict(arrowstyle='fancy', connectionstyle='arc3,rad=-0.3'))
    
    plt.grid(True)
    plt.show()


def calculate_var_bootstrap(returns, stock_symbol, confidence_level=0.05):
    """
    Calculate Value at Risk using Bootstrap method
    
    Args:
        returns: DataFrame with returns for all stocks
        stock_symbol: Stock symbol to calculate VaR for
        confidence_level: Confidence level (default 0.05 for 95% confidence)
    
    Returns:
        VaR value
    """
    rets = returns.dropna()
    var = rets[stock_symbol].quantile(confidence_level)
    return var


def plot_returns_distribution_with_var(stock_data, stock_symbol='Stock'):
    """
    Plot returns distribution
    
    Args:
        stock_data: DataFrame with daily returns
        stock_symbol: Name of stock for title
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(stock_data['Daily Return'].dropna(), bins=100, color='purple', kde=True)
    plt.title(f'{stock_symbol} Daily Returns Distribution')
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    plt.show()


def calculate_var_for_all_stocks(tech_returns, tech_list, confidence_level=0.05):
    """
    Calculate VaR for all stocks
    
    Args:
        tech_returns: DataFrame with returns for all stocks
        tech_list: List of stock symbols
        confidence_level: Confidence level
    
    Returns:
        Dictionary with VaR for each stock
    """
    var_dict = {}
    rets = tech_returns.dropna()
    
    for stock in tech_list:
        if stock in rets.columns:
            var = rets[stock].quantile(confidence_level)
            var_dict[stock] = var
            print(f"{stock} VaR (0.05): {var:.6f}")
    
    return var_dict


def interpret_var(var_value, investment=1000000):
    """
    Interpret VaR value in dollar terms
    
    Args:
        var_value: VaR percentage value
        investment: Investment amount in dollars
    
    Returns:
        Dollar amount at risk
    """
    dollar_var = abs(var_value) * investment
    return dollar_var


if __name__ == "__main__":
    from data_fetching import get_closing_prices, fetch_stock_data
    from stock_analysis import calculate_daily_returns
    from correlation_analysis import calculate_returns_for_stocks
    
    # Example usage
    tech_list = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    
    # Get closing prices and calculate returns
    closingprice_df = get_closing_prices(tech_list)
    tech_returns = calculate_returns_for_stocks(closingprice_df)
    
    # Plot risk vs return
    plot_risk_return_scatter(tech_returns)
    
    # Calculate VaR for all stocks
    print("\n=== Value at Risk (Bootstrap Method) ===")
    var_results = calculate_var_for_all_stocks(tech_returns, tech_list)
    
    # Interpret VaR for AAPL
    if 'AAPL' in var_results:
        aapl_var = var_results['AAPL']
        dollar_var = interpret_var(aapl_var, 1000000)
        print(f"\nFor a $1,000,000 investment in AAPL:")
        print(f"One-day 5% VaR: ${dollar_var:,.2f}")
        print(f"With 95% confidence, the worst daily loss will not exceed ${dollar_var:,.2f}")
