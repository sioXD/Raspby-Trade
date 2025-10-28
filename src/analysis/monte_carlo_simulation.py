"""
Monte Carlo Simulation Module
Implements Monte Carlo simulation for stock price prediction and VaR calculation
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tkinter errors
import matplotlib.pyplot as plt


def stock_monte_carlo(start_price, days, mu, sigma):
    """
    Simulate stock price using Monte Carlo method with Geometric Brownian Motion
    
    Args:
        start_price: Starting stock price
        days: Number of days to simulate
        mu: Expected return (drift)
        sigma: Volatility (standard deviation)
    
    Returns:
        Array of simulated prices
    """
    dt = 1 / days
    price = np.zeros(days)
    price[0] = start_price
    
    shock = np.zeros(days)
    drift = np.zeros(days)
    
    for x in range(1, days):
        shock[x] = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))
        drift[x] = mu * dt
        price[x] = price[x-1] + (price[x-1] * (drift[x] + shock[x]))
    
    return price


def plot_monte_carlo_simulations(start_price, days, mu, sigma, num_runs=100, stock_name='Stock'):
    """
    Plot multiple Monte Carlo simulation runs
    
    Args:
        start_price: Starting stock price
        days: Number of days to simulate
        mu: Expected return
        sigma: Volatility
        num_runs: Number of simulation runs
        stock_name: Name of stock for title
    """
    plt.figure(figsize=(12, 6))
    
    for run in range(num_runs):
        plt.plot(stock_monte_carlo(start_price, days, mu, sigma))
    
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.title(f'Monte Carlo Analysis for {stock_name}')
    plt.grid(True)
    plt.show()


def monte_carlo_var_analysis(start_price, days, mu, sigma, runs=10000, confidence_level=0.01, stock_name='Stock'):
    """
    Perform Monte Carlo VaR analysis
    
    Args:
        start_price: Starting stock price
        days: Number of days to simulate
        mu: Expected return
        sigma: Volatility
        runs: Number of simulation runs
        confidence_level: Confidence level for VaR (default 0.01 for 99%)
        stock_name: Name of stock for title
    
    Returns:
        Tuple of (VaR value, mean final price, quantile price)
    """
    simulations = np.zeros(runs)
    
    for run in range(runs):
        simulations[run] = stock_monte_carlo(start_price, days, mu, sigma)[days-1]
    
    q = np.percentile(simulations, confidence_level * 100)
    var = start_price - q
    mean_final_price = simulations.mean()
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.hist(simulations, bins=200)
    
    plt.figtext(0.6, 0.8, s='Start Price: $%.2f' % start_price)
    plt.figtext(0.6, 0.7, s='Mean Final Price: $%.2f' % mean_final_price)
    plt.figtext(0.6, 0.6, s='VaR(0.99): $%.2f' % var)
    plt.figtext(0.15, 0.6, s="q(0.99): $%.2f" % q)
    
    plt.axvline(x=q, linewidth=4, color='r')
    plt.title(f"Final price distribution for {stock_name} after {days} days", weight='bold')
    plt.xlabel('Final Price')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
    
    return var, mean_final_price, q


def monte_carlo_simulation_for_data(stock_data, num_simulations=100, num_days=365):
    """
    Run Monte Carlo simulation based on historical stock data
    
    Args:
        stock_data: DataFrame with stock data
        num_simulations: Number of simulation runs
        num_days: Number of days to simulate
    
    Returns:
        Array of simulated prices for all runs
    """
    close_prices = stock_data['Close'].values
    log_returns = np.log(1 + stock_data['Close'].pct_change().dropna())
    mu = log_returns.mean()
    sigma = log_returns.std()
    last_price = close_prices[-1]
    
    simulated_prices = np.zeros((num_simulations, num_days))
    for i in range(num_simulations):
        daily_returns = np.random.normal(mu, sigma, num_days - 1)
        price_path = np.zeros(num_days)
        price_path[0] = last_price
        for j in range(1, num_days):
            price_path[j] = price_path[j - 1] * np.exp(daily_returns[j - 1])
        simulated_prices[i] = price_path
    
    return simulated_prices


if __name__ == "__main__":
    from data_fetching import get_closing_prices
    from correlation_analysis import calculate_returns_for_stocks
    
    # Example usage
    tech_list = ['GOOGL', 'AMZN', 'AAPL', 'MSFT']
    
    # Get data
    closingprice_df = get_closing_prices(tech_list)
    tech_returns = calculate_returns_for_stocks(closingprice_df)
    rets = tech_returns.dropna()
    
    # Calculate parameters for GOOGL
    days = 365
    mu = rets.mean()['GOOGL']
    sigma = rets.std()['GOOGL']
    
    # Run simulations for each stock
    stock_params = {
        'GOOGL': 830.09,
        'AMZN': 824.95,
        'AAPL': 117.10,
        'MSFT': 59.94
    }
    
    for stock, start_price in stock_params.items():
        print(f"\n=== {stock} Monte Carlo Analysis ===")
        plot_monte_carlo_simulations(start_price, days, mu, sigma, num_runs=100, stock_name=stock)
        var, mean_price, q = monte_carlo_var_analysis(start_price, days, mu, sigma, runs=10000, stock_name=stock)
        print(f"VaR (99%): ${var:.2f}")
        print(f"Mean Final Price: ${mean_price:.2f}")
