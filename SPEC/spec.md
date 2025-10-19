# BTC Indicators Library - Specification

## Project Structure

```
btc-indicators/
├── btc_indicators/         # Core library
│   ├── __init__.py
│   ├── data.py            # Data fetching & persistence
│   ├── indicators.py      # Indicator calculations
│   └── plotting.py        # Visualization
├── tests/                 # Unit tests
├── utils/                 # CLI utilities
│   ├── fetchdata.py       # Fetch & update data
│   └── drawplots.py       # Generate plots
├── data/                  # Year-based CSV storage
├── tmp/                   # Generated plots
├── examples/              # Usage examples
└── pyproject.toml         # Package config
```

## Core Modules

### Data Module (`btc_indicators/data.py`)

**Functions:**
- `fetch_btc_data(start_date, end_date, interval='1d')` - Fetch BTC-USD data from Yahoo Finance
  - Defaults to last 30 days if dates not provided
  - No range limit (entire BTC history available)
  - Year-based CSV persistence: `2023.csv`, `2024.csv`, etc.
  - Intelligent patching: merges new data, removes duplicates
  - Returns pandas DataFrame with OHLCV data

- `load_data_from_csv(start_date, end_date, data_dir='data')` - Load from local CSV files

### Indicators Module (`btc_indicators/indicators.py`)

**Functions:**
- `calculate_mayer_multiple(data, window=200)` - Price / 200-day MA
  - Returns columns: `200_MA`, `Mayer_Multiple`, `Mayer_Multiple_Avg`
  - `Mayer_Multiple_Avg` contains the mean of all Mayer Multiple values
- `calculate_macd(data, fast=12, slow=26, signal=9)` - MACD indicator
- `calculate_rsi(data, period=14)` - Relative Strength Index
- `add_all_indicators(data)` - Calculate all indicators at once

### Plotting Module (`btc_indicators/plotting.py`)

**Functions:**
- `plot_mayer_multiple(data, save_path, show=True)` - Multi-panel plot with:
  - Panel 1: Price, 200-day MA, and price levels for MM 0.8, 1.3, 2.4 thresholds
  - Panel 2: Mayer Multiple with reference lines (0.8, 1.0, 2.4) and average line
- `plot_macd(data, save_path, show=True)` - Price and MACD with signal line & histogram
- `plot_rsi(data, save_path, show=True)` - Price and RSI with overbought/oversold zones
- `plot_all_indicators(data, save_dir, show=True)` - Generate all plots

## Utility Scripts

### fetchdata.py

Fetch BTC-USD data and update local CSV files.

**Arguments:**
- `--start DATE` - Start date (YYYY-MM-DD)
- `--end DATE` - End date (YYYY-MM-DD)
- `--data-dir DIR` - CSV directory (default: 'data')

**Behavior:**
- No args: Auto-fetch from last data point to today
- With args: Fetch specified date range

```bash
python utils/fetchdata.py
python utils/fetchdata.py --start 2020-01-01 --end 2023-12-31
```

### drawplots.py

Generate indicator plots from local CSV data.

**Arguments:**
- `--start DATE` - Start date (default: 1 year ago)
- `--end DATE` - End date (default: today)
- `--data-dir DIR` - CSV directory (default: 'data')
- `--save-dir DIR` - Save directory (default: 'tmp')
- `--display` - Show plots interactively (default: False)

**Behavior:**
- Always saves plots (Mayer Multiple, MACD, RSI)
- Only displays if `--display` flag provided

```bash
python utils/drawplots.py
python utils/drawplots.py --display
python utils/drawplots.py --save-dir plots/ --display
```

## Example Usage

```python
from btc_indicators import (
    fetch_btc_data,
    calculate_mayer_multiple,
    plot_mayer_multiple
)

# Fetch data
data = fetch_btc_data(start_date="2020-01-01")

# Calculate indicator
data = calculate_mayer_multiple(data)

# Plot
plot_mayer_multiple(data, save_path="mayer.png")
```

## Installation

```bash
pip install .              # Install package
pip install -e .           # Development mode
pipenv install --dev       # With pipenv
```
