"""
Stock Correlation Analysis Module
Analyzes correlations between different stocks
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tkinter errors
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_returns_for_stocks(closingprice_df):
    """
    Calculate daily percentage returns for all stocks
    
    Args:
        closingprice_df: DataFrame with closing prices for multiple stocks
    
    Returns:
        DataFrame with daily returns
    """
    return closingprice_df.pct_change()


def plot_stock_comparison(tech_returns, stock1, stock2, kind='scatter', color='skyblue', height=8):
    """
    Plot comparison between two stocks
    
    Args:
        tech_returns: DataFrame with returns for all stocks
        stock1: First stock symbol
        stock2: Second stock symbol
        kind: Type of plot ('scatter', 'hex', 'reg')
        color: Color for the plot
        height: Height of the plot
    """
    sns.jointplot(x=stock1, y=stock2, data=tech_returns, kind=kind, height=height, color=color)
    plt.show()


def plot_pairplot(tech_returns, size=3):
    """
    Create pairplot for all stocks
    
    Args:
        tech_returns: DataFrame with returns for all stocks
        size: Size of each subplot
    """
    sns.pairplot(tech_returns.dropna(), height=size)
    plt.show()


def plot_custom_pairgrid(data, data_type='returns'):
    """
    Create custom PairGrid with different plots
    
    Args:
        data: DataFrame with stock data
        data_type: Type of data ('returns' or 'prices')
    """
    fig = sns.PairGrid(data.dropna())
    fig.map_upper(plt.scatter, color='purple')
    fig.map_lower(sns.kdeplot, cmap='cool_d')
    fig.map_diag(plt.hist, bins=30)
    plt.suptitle(f'Stock {data_type.capitalize()} Correlation Analysis', y=1.02)
    plt.show()


def plot_correlation_heatmap(data, data_type='returns', cmap='YlGnBu'):
    """
    Plot correlation heatmap
    
    Args:
        data: DataFrame with stock data
        data_type: Type of data for title
        cmap: Colormap for heatmap
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, fmt=".3g", cmap=cmap)
    plt.title(f'Stock {data_type.capitalize()} Correlation Matrix')
    plt.show()


def analyze_correlations(tech_returns, closingprice_df):
    """
    Perform complete correlation analysis
    
    Args:
        tech_returns: DataFrame with returns for all stocks
        closingprice_df: DataFrame with closing prices
    """
    print("=== Correlation Analysis ===\n")
    
    # Returns correlation
    print("Returns Correlation Matrix:")
    print(tech_returns.corr())
    print("\n")
    
    # Closing prices correlation
    print("Closing Prices Correlation Matrix:")
    print(closingprice_df.corr())
    print("\n")
    
    # Plot heatmaps
    plot_correlation_heatmap(tech_returns, 'returns')
    plot_correlation_heatmap(closingprice_df, 'closing prices')


if __name__ == "__main__":
    from data_fetching import get_closing_prices
    
    # Example usage
    tech_list = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    
    # Get closing prices
    closingprice_df = get_closing_prices(tech_list)
    
    # Calculate returns
    tech_returns = calculate_returns_for_stocks(closingprice_df)
    
    # Analyze correlations
    analyze_correlations(tech_returns, closingprice_df)
    
    # Plot specific stock comparisons
    plot_stock_comparison(tech_returns, 'GOOGL', 'AMZN', kind='scatter')
    plot_stock_comparison(tech_returns, 'AAPL', 'MSFT', kind='reg')
    
    # Create pairplot
    plot_pairplot(tech_returns)
