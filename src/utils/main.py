"""
Main Script for Stock Market Trend Analysis and Prediction
Combines all modules to perform complete analysis and prediction
"""

import warnings
warnings.filterwarnings('ignore')

from ..analysis.data_fetching import fetch_stock_data, get_closing_prices
from ..analysis.stock_analysis import (
    calculate_moving_averages, 
    calculate_daily_returns,
    plot_closing_price,
    plot_volume,
    plot_moving_averages,
    plot_daily_returns,
    plot_returns_histogram
)
from ..analysis.correlation_analysis import (
    calculate_returns_for_stocks,
    plot_stock_comparison,
    plot_correlation_heatmap,
    analyze_correlations
)
from ..analysis.risk_analysis import (
    plot_risk_return_scatter,
    calculate_var_for_all_stocks,
    interpret_var
)
from ..analysis.monte_carlo_simulation import (
    plot_monte_carlo_simulations,
    monte_carlo_var_analysis
)
from ..ml.lstm_prediction import predict_stock_price, check_compute_resources


def run_basic_analysis(tech_list):
    """
    Run basic stock analysis
    
    Args:
        tech_list: List of stock ticker symbols
    """
    print("\n" + "="*60)
    print("SECTION 1: BASIC STOCK ANALYSIS")
    print("="*60 + "\n")
    
    # Fetch stock data
    stock_data = fetch_stock_data(tech_list)
    
    if 'AAPL' in stock_data:
        aapl = stock_data['AAPL']
        
        # Calculate moving averages
        aapl = calculate_moving_averages(aapl)
        
        # Calculate daily returns
        aapl = calculate_daily_returns(aapl)
        
        print("\nAAPL Stock Summary:")
        print(aapl.describe())
        
        # Plot analysis
        plot_closing_price(aapl, 'AAPL')
        plot_volume(aapl, 'AAPL')
        plot_moving_averages(aapl, stock_name='AAPL')
        plot_daily_returns(aapl, 'AAPL')
        plot_returns_histogram(aapl, stock_name='AAPL')
    
    return stock_data


def run_correlation_analysis(tech_list):
    """
    Run correlation analysis
    
    Args:
        tech_list: List of stock ticker symbols
    """
    print("\n" + "="*60)
    print("SECTION 2: CORRELATION ANALYSIS")
    print("="*60 + "\n")
    
    # Get closing prices
    closingprice_df = get_closing_prices(tech_list)
    
    # Calculate returns
    tech_returns = calculate_returns_for_stocks(closingprice_df)
    
    # Analyze correlations
    analyze_correlations(tech_returns, closingprice_df)
    
    # Plot specific comparisons
    print("\nGenerating stock comparison plots...")
    plot_stock_comparison(tech_returns, 'GOOGL', 'AMZN', kind='scatter')
    plot_stock_comparison(tech_returns, 'AAPL', 'MSFT', kind='reg')
    
    return closingprice_df, tech_returns


def run_risk_analysis(tech_list, tech_returns, closingprice_df):
    """
    Run risk analysis
    
    Args:
        tech_list: List of stock ticker symbols
        tech_returns: DataFrame with returns
        closingprice_df: DataFrame with closing prices
    """
    print("\n" + "="*60)
    print("SECTION 3: RISK ANALYSIS")
    print("="*60 + "\n")
    
    # Plot risk vs return
    plot_risk_return_scatter(tech_returns)
    
    # Calculate VaR using Bootstrap method
    print("\nValue at Risk (Bootstrap Method):")
    var_results = calculate_var_for_all_stocks(tech_returns, tech_list)
    
    # Interpret VaR
    print("\n--- VaR Interpretation for $1,000,000 investment ---")
    for stock, var in var_results.items():
        dollar_var = interpret_var(var, 1000000)
        print(f"{stock}: ${dollar_var:,.2f} (95% confidence)")


def run_monte_carlo_analysis(tech_returns):
    """
    Run Monte Carlo simulation analysis
    
    Args:
        tech_returns: DataFrame with returns
    """
    print("\n" + "="*60)
    print("SECTION 4: MONTE CARLO SIMULATION")
    print("="*60 + "\n")
    
    rets = tech_returns.dropna()
    days = 365
    mu = rets.mean()['GOOGL']
    sigma = rets.std()['GOOGL']
    
    stock_params = {
        'GOOGL': 830.09,
        'AMZN': 824.95,
        'AAPL': 117.10,
        'MSFT': 59.94
    }
    
    for stock, start_price in stock_params.items():
        print(f"\n--- {stock} Monte Carlo Analysis ---")
        plot_monte_carlo_simulations(start_price, days, mu, sigma, num_runs=100, stock_name=stock)
        var, mean_price, q = monte_carlo_var_analysis(start_price, days, mu, sigma, runs=10000, stock_name=stock)
        print(f"VaR (99%): ${var:.2f}")
        print(f"Mean Final Price: ${mean_price:.2f}")


def run_lstm_prediction(stocks_list):
    """
    Run LSTM prediction
    
    Args:
        stocks_list: List of stock ticker symbols to predict
    """
    print("\n" + "="*60)
    print("SECTION 5: LSTM STOCK PRICE PREDICTION")
    print("="*60 + "\n")
    
    # Check compute resources
    check_compute_resources()
    
    # Predict for each stock
    for stock in stocks_list:
        print(f"\n{'='*60}")
        print(f"Predicting {stock}")
        print('='*60)
        predict_stock_price(stock)


def main():
    """
    Main function to run complete analysis
    """
    print("\n" + "="*70)
    print("STOCK MARKET TREND ANALYSIS AND PREDICTION")
    print("="*70)
    
    # Define stock list
    tech_list = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    prediction_list = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']
    
    # Run all analyses
    try:
        # 1. Basic Analysis
        stock_data = run_basic_analysis(tech_list)
        
        # 2. Correlation Analysis
        closingprice_df, tech_returns = run_correlation_analysis(tech_list)
        
        # 3. Risk Analysis
        run_risk_analysis(tech_list, tech_returns, closingprice_df)
        
        # 4. Monte Carlo Simulation
        run_monte_carlo_analysis(tech_returns)
        
        # 5. LSTM Prediction
        run_lstm_prediction(prediction_list)
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nError during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
