"""
BTC Indicators - A Python library for Bitcoin technical indicators and visualization.

This library provides tools to fetch BTC-USD historical data, calculate technical
indicators (Mayer Multiple, MACD, RSI), and create professional visualizations.
"""

__version__ = "0.3.0"
__author__ = "BTC Indicators Contributors"

# Import main functions from modules
from btc_indicators.data import (
    fetch_btc_data,
    load_data_from_csv
)

from btc_indicators.indicators import (
    calculate_mayer_multiple,
    calculate_macd,
    calculate_rsi,
    add_all_indicators
)

from btc_indicators.plotting import (
    plot_mayer_multiple,
    plot_macd,
    plot_rsi,
    plot_all_indicators
)

# Define public API
__all__ = [
    # Data functions
    'fetch_btc_data',
    'load_data_from_csv',
    
    # Indicator functions
    'calculate_mayer_multiple',
    'calculate_macd',
    'calculate_rsi',
    'add_all_indicators',
    
    # Plotting functions
    'plot_mayer_multiple',
    'plot_macd',
    'plot_rsi',
    'plot_all_indicators',
    
    # Metadata
    '__version__',
]

