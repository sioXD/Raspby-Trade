"""
LSTM Stock Price Prediction Module
Implements Bi-LSTM model for stock price prediction using Monte Carlo simulated data
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tkinter errors
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Bidirectional, Dense, Dropout
import tensorflow as tf
import os
import psutil

# Suppress TensorFlow warnings about retracing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')
import warnings
warnings.filterwarnings('ignore', category=Warning)


def check_compute_resources():
    """
    Check available compute resources (GPU/CPU)
    """
    physical_devices = tf.config.list_physical_devices()
    if not physical_devices:
        print("No devices found, using CPU.")
    else:
        for device in physical_devices:
            print(f"Device: {device.device_type}, Name: {device.name}")
    
    if tf.config.list_physical_devices('GPU'):
        print("\n✅ Using GPU")
        for gpu in tf.config.experimental.list_physical_devices('GPU'):
            details = tf.config.experimental.get_device_details(gpu)
            print(f"GPU Name: {details.get('device_name', 'Unknown')}")
    else:
        print("\n✅ Using CPU")
    
    print(f"\nCPU Cores: {os.cpu_count()}")
    print(f"Physical Cores: {psutil.cpu_count(logical=False)}")
    print(f"Logical Cores: {psutil.cpu_count(logical=True)}")


def monte_carlo_simulation(stock_data, num_simulations=100, num_days=365):
    """
    Run Monte Carlo simulation for stock prices
    
    Args:
        stock_data: DataFrame with historical stock data
        num_simulations: Number of simulation runs
        num_days: Number of days to simulate
    
    Returns:
        Array of simulated price paths
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


def prepare_lstm_data_from_mc(simulated_prices, lookback_window, prediction_window):
    """
    Prepare training data from Monte Carlo simulations for LSTM
    
    Args:
        simulated_prices: Array of simulated price paths
        lookback_window: Number of past days to use as input
        prediction_window: Number of future days to predict
    
    Returns:
        Tuple of (X_train, y_train) arrays
    """
    all_X = []
    all_y = []
    
    for path in simulated_prices:
        data = path.reshape(-1, 1)
        for i in range(len(data) - lookback_window - prediction_window + 1):
            all_X.append(data[i : i + lookback_window])
            all_y.append(data[i + lookback_window : i + lookback_window + prediction_window])
    
    return np.array(all_X), np.array(all_y)


def train_bi_lstm_from_mc(X_train, y_train, lookback_window, prediction_window, 
                          epochs=20, batch_size=32, validation_split=0.2):
    """
    Train Bi-LSTM model on Monte Carlo simulated data
    
    Args:
        X_train: Training input data
        y_train: Training target data
        lookback_window: Number of input time steps
        prediction_window: Number of output time steps
        epochs: Number of training epochs
        batch_size: Batch size for training
        validation_split: Validation split ratio
    
    Returns:
        Tuple of (trained_model, scaler_x, scaler_y)
    """
    scaler_x = MinMaxScaler()
    X_train_scaled = scaler_x.fit_transform(X_train.reshape(-1, 1)).reshape(X_train.shape)
    
    scaler_y = MinMaxScaler()
    y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, prediction_window)).reshape(y_train.shape)
    
    model = Sequential([
        Bidirectional(LSTM(50, return_sequences=True, input_shape=(lookback_window, 1))),
        Dropout(0.2),
        Bidirectional(LSTM(50, return_sequences=False)),
        Dropout(0.2),
        Dense(prediction_window)
    ])
    
    # Compile with run_eagerly=False for better performance and less retracing
    model.compile(optimizer='adam', loss='mean_squared_error', run_eagerly=False)
    model.fit(X_train_scaled, y_train_scaled, epochs=epochs, batch_size=batch_size, 
              validation_split=validation_split, verbose=1)
    
    return model, scaler_x, scaler_y


def predict_future_bi_lstm_from_mc(model, last_real_prices, scaler_x, prediction_window, lookback_window):
    """
    Predict future prices using trained Bi-LSTM model
    
    Args:
        model: Trained LSTM model
        last_real_prices: Last N days of actual prices
        scaler_x: Scaler used for input normalization
        prediction_window: Number of days to predict
        lookback_window: Number of input days
    
    Returns:
        Array of predicted prices
    """
    scaled_last_real_prices = scaler_x.transform(last_real_prices.reshape(-1, 1))
    input_sequence = scaled_last_real_prices.reshape(1, lookback_window, 1)
    
    # Use model(input) instead of predict() to avoid retracing warnings
    # Ensure input is a TensorFlow tensor with consistent shape
    input_tensor = tf.constant(input_sequence, dtype=tf.float32)
    predicted_scaled = model(input_tensor, training=False).numpy()
    
    predicted_prices = scaler_x.inverse_transform(predicted_scaled.reshape(-1, 1)).flatten()
    
    return predicted_prices


def predict_stock_price(stock_symbol):
    """
    Complete stock price prediction pipeline
    
    Args:
        stock_symbol: Stock ticker symbol
    """
    today = datetime.now()
    start_date = today - timedelta(days=365 * 5)
    
    # Fetch data
    print(f"Fetching data for {stock_symbol}...")
    data = yf.download(stock_symbol, start=start_date, end=today)
    if data.empty:
        print(f"Invalid stock symbol or no data available for {stock_symbol}.")
        return
    
    # Monte Carlo simulation
    print("Running Monte Carlo simulation...")
    num_simulations = 200
    num_days_simulate = 365
    simulated_prices = monte_carlo_simulation(data, num_simulations, num_days_simulate)
    
    # Prepare LSTM data
    print("Preparing LSTM training data...")
    lookback_window = 60
    prediction_window = 180
    X_train, y_train = prepare_lstm_data_from_mc(simulated_prices, lookback_window, prediction_window)
    
    # Train model
    print("Training Bi-LSTM model...")
    model, scaler_x, scaler_y = train_bi_lstm_from_mc(
        X_train, y_train, lookback_window, prediction_window, 
        epochs=20, batch_size=128, validation_split=0.1
    )
    
    # Predict future
    print("Generating predictions...")
    last_real_prices = data['Close'][-lookback_window:].values.reshape(-1, 1)
    future_predictions = predict_future_bi_lstm_from_mc(
        model, last_real_prices, scaler_x, prediction_window, lookback_window
    )
    
    # Create prediction DataFrame
    future_dates = pd.date_range(start=today, periods=prediction_window)
    pred_df = pd.DataFrame({'Date': future_dates, 'Predicted Price': future_predictions})
    pred_df = pred_df.resample('ME', on='Date').mean()
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Actual Prices')
    plt.plot(pred_df.index, pred_df['Predicted Price'], label='Monthly Predicted Prices', 
             linestyle='dashed', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title(f'{stock_symbol} Monthly Stock Price Prediction')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"\nPrediction complete for {stock_symbol}")
    return pred_df


if __name__ == "__main__":
    # Check compute resources
    check_compute_resources()
    
    # Predict stock prices
    stocks_to_predict = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']
    
    for stock in stocks_to_predict:
        print(f"\n{'='*60}")
        print(f"Predicting {stock}")
        print('='*60)
        predict_stock_price(stock)
