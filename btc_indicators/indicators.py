"""
Technical indicators calculation module for BTC-USD data.
"""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_mayer_multiple(data: pd.DataFrame, window: int = 200) -> pd.DataFrame:
    """
    Calculate the Mayer Multiple indicator.
    
    The Mayer Multiple is the ratio of the current price to its moving average.
    It's commonly used with a 200-day moving average for Bitcoin.
    
    Args:
        data: DataFrame with 'Close' column
        window: Moving average window (default: 200 days)
        
    Returns:
        DataFrame with added columns:
        - '200_MA': 200-day moving average
        - 'Mayer_Multiple': Price / 200-day MA ratio
        - 'Mayer_Multiple_Avg': Mean of all Mayer Multiple values
        - 'MM_0.8_Price': Price level at 0.8x the 200-day MA (oversold threshold)
        - 'MM_1.3_Price': Price level at 1.3x the 200-day MA
        - 'MM_2.4_Price': Price level at 2.4x the 200-day MA (overbought threshold)
        
    Raises:
        ValueError: If 'Close' column is missing or insufficient data
        
    Examples:
        >>> data = fetch_btc_data(start_date="2020-01-01")
        >>> data = calculate_mayer_multiple(data)
        >>> print(data[['Close', '200_MA', 'Mayer_Multiple']].tail())
    """
    if 'Close' not in data.columns:
        raise ValueError("DataFrame must contain 'Close' column")
    
    if len(data) < window:
        raise ValueError(
            f"Insufficient data for {window}-day moving average. "
            f"Need at least {window} days, got {len(data)} days."
        )
    
    # Create a copy to avoid modifying original
    result = data.copy()
    
    # Calculate moving average
    result[f'{window}_MA'] = result['Close'].rolling(window=window).mean()
    
    # Calculate Mayer Multiple
    result['Mayer_Multiple'] = result['Close'] / result[f'{window}_MA']
    
    # Calculate average Mayer Multiple (mean of non-NaN values)
    result['Mayer_Multiple_Avg'] = result['Mayer_Multiple'].mean()
    
    # Calculate price levels for key Mayer Multiple thresholds
    result['MM_0.8_Price'] = result[f'{window}_MA'] * 0.8
    result['MM_1.3_Price'] = result[f'{window}_MA'] * 1.3
    result['MM_2.4_Price'] = result[f'{window}_MA'] * 2.4
    
    return result


def calculate_macd(
    data: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
    price_col: str = 'Close'
) -> pd.DataFrame:
    """
    Calculate MACD (Moving Average Convergence Divergence) indicator.
    
    MACD is a trend-following momentum indicator that shows the relationship
    between two moving averages of a security's price.
    
    Args:
        data: DataFrame with price data
        fast: Fast EMA period (default: 12)
        slow: Slow EMA period (default: 26)
        signal: Signal line EMA period (default: 9)
        price_col: Column name for price (default: 'Close')
        
    Returns:
        DataFrame with added columns: 'MACD', 'MACD_Signal', 'MACD_Histogram'
        
    Raises:
        ValueError: If price column is missing or parameters are invalid
        
    Examples:
        >>> data = fetch_btc_data(start_date="2020-01-01")
        >>> data = calculate_macd(data)
        >>> print(data[['Close', 'MACD', 'MACD_Signal', 'MACD_Histogram']].tail())
    """
    if price_col not in data.columns:
        raise ValueError(f"DataFrame must contain '{price_col}' column")
    
    if fast >= slow:
        raise ValueError(f"Fast period ({fast}) must be less than slow period ({slow})")
    
    min_periods = slow + signal
    if len(data) < min_periods:
        raise ValueError(
            f"Insufficient data for MACD calculation. "
            f"Need at least {min_periods} periods, got {len(data)} periods."
        )
    
    # Create a copy to avoid modifying original
    result = data.copy()
    
    # Calculate EMAs
    ema_fast = result[price_col].ewm(span=fast, adjust=False).mean()
    ema_slow = result[price_col].ewm(span=slow, adjust=False).mean()
    
    # Calculate MACD line
    result['MACD'] = ema_fast - ema_slow
    
    # Calculate signal line
    result['MACD_Signal'] = result['MACD'].ewm(span=signal, adjust=False).mean()
    
    # Calculate histogram
    result['MACD_Histogram'] = result['MACD'] - result['MACD_Signal']
    
    return result


def calculate_rsi(
    data: pd.DataFrame,
    period: int = 14,
    price_col: str = 'Close'
) -> pd.DataFrame:
    """
    Calculate RSI (Relative Strength Index) indicator.
    
    RSI is a momentum oscillator that measures the speed and magnitude of price changes.
    Values range from 0 to 100, with readings above 70 typically considered overbought
    and below 30 oversold.
    
    Args:
        data: DataFrame with price data
        period: RSI period (default: 14)
        price_col: Column name for price (default: 'Close')
        
    Returns:
        DataFrame with added column: 'RSI'
        
    Raises:
        ValueError: If price column is missing or insufficient data
        
    Examples:
        >>> data = fetch_btc_data(start_date="2020-01-01")
        >>> data = calculate_rsi(data)
        >>> print(data[['Close', 'RSI']].tail())
    """
    if price_col not in data.columns:
        raise ValueError(f"DataFrame must contain '{price_col}' column")
    
    if len(data) < period + 1:
        raise ValueError(
            f"Insufficient data for RSI calculation. "
            f"Need at least {period + 1} periods, got {len(data)} periods."
        )
    
    # Create a copy to avoid modifying original
    result = data.copy()
    
    # Calculate price changes
    delta = result[price_col].diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0.0)
    losses = -delta.where(delta < 0, 0.0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    result['RSI'] = 100 - (100 / (1 + rs))
    
    return result


def add_all_indicators(
    data: pd.DataFrame,
    mayer_window: int = 200,
    macd_fast: int = 12,
    macd_slow: int = 26,
    macd_signal: int = 9,
    rsi_period: int = 14
) -> pd.DataFrame:
    """
    Calculate all available indicators at once.
    
    Args:
        data: DataFrame with OHLCV data
        mayer_window: Mayer Multiple MA window (default: 200)
        macd_fast: MACD fast EMA period (default: 12)
        macd_slow: MACD slow EMA period (default: 26)
        macd_signal: MACD signal line period (default: 9)
        rsi_period: RSI period (default: 14)
        
    Returns:
        DataFrame with all indicators added
    """
    result = data.copy()
    
    try:
        result = calculate_mayer_multiple(result, window=mayer_window)
    except ValueError as e:
        print(f"Warning: Could not calculate Mayer Multiple: {e}")
    
    try:
        result = calculate_macd(result, fast=macd_fast, slow=macd_slow, signal=macd_signal)
    except ValueError as e:
        print(f"Warning: Could not calculate MACD: {e}")
    
    try:
        result = calculate_rsi(result, period=rsi_period)
    except ValueError as e:
        print(f"Warning: Could not calculate RSI: {e}")
    
    return result

