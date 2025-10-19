# BTC Indicators

A Python library for calculating and plotting Bitcoin technical indicators with intelligent data management.

## Features

- **Data Management**: Year-based CSV persistence with smart patching
- **Technical Indicators**: Mayer Multiple, MACD, RSI
- **Visualizations**: Publication-quality matplotlib plots
- **CLI Utilities**: Scripts for data fetching and plotting
- **Full History**: Access entire BTC history since 2014

## Installation

```bash
git clone https://github.com/yourusername/btc-indicators.git
cd btc-indicators
pip install -e .              # Development mode
# or
pip install .                 # Standard install
```

**Requirements:** Python >= 3.8, yfinance, pandas, matplotlib, numpy

## Quick Start

### Library Usage

```python
from btc_indicators import fetch_btc_data, calculate_mayer_multiple, plot_mayer_multiple

# Fetch data
data = fetch_btc_data(start_date="2022-01-01", end_date="2024-12-31")

# Calculate indicator
data = calculate_mayer_multiple(data)

# Plot
plot_mayer_multiple(data, save_path="mayer_multiple.png")
```

### CLI Usage

```bash
# Fetch latest data
python utils/fetchdata.py

# Fetch specific range
python utils/fetchdata.py --start 2020-01-01 --end 2023-12-31

# Generate plots (saves to tmp/)
python utils/drawplots.py

# Display plots interactively
python utils/drawplots.py --display
```

## API Reference

### Data Functions

**`fetch_btc_data(start_date=None, end_date=None, interval='1d', data_dir='data')`**
- Fetches BTC-USD data from Yahoo Finance
- Persists as year-based CSV files (2023.csv, 2024.csv, etc.)
- Intelligently patches existing data
- Returns: pandas DataFrame with OHLCV data

**`load_data_from_csv(start_date=None, end_date=None, data_dir='data')`**
- Loads data from local CSV files without API call
- Returns: pandas DataFrame

### Indicator Functions

**`calculate_mayer_multiple(data, window=200)`**
- Calculates Price / 200-day MA
- Adds columns: '200_MA', 'Mayer_Multiple'

**`calculate_macd(data, fast=12, slow=26, signal=9, price_col='Close')`**
- Calculates MACD indicator
- Adds columns: 'MACD', 'MACD_Signal', 'MACD_Histogram'

**`calculate_rsi(data, period=14, price_col='Close')`**
- Calculates Relative Strength Index
- Adds column: 'RSI'

**`add_all_indicators(data, ...)`**
- Calculates all indicators at once
- Returns DataFrame with all indicator columns

### Plotting Functions

**`plot_mayer_multiple(data, save_path=None, show=True)`**
- Multi-panel plot: Price + 200-day MA, Mayer Multiple ratio

**`plot_macd(data, save_path=None, show=True)`**
- Multi-panel plot: Price, MACD with signal line & histogram

**`plot_rsi(data, save_path=None, show=True)`**
- Multi-panel plot: Price, RSI with overbought/oversold zones

**`plot_all_indicators(data, save_dir=None, show=True)`**
- Generates all indicator plots

## CLI Utilities

### fetchdata.py

Fetch and update BTC data in local CSV files.

```bash
python utils/fetchdata.py [--start DATE] [--end DATE] [--data-dir DIR]
```

- No args: Auto-fetch from last data point to today
- `--start DATE`: Start date (YYYY-MM-DD)
- `--end DATE`: End date (YYYY-MM-DD)
- `--data-dir DIR`: CSV directory (default: 'data')

### drawplots.py

Generate indicator plots from CSV data.

```bash
python utils/drawplots.py [--start DATE] [--end DATE] [--save-dir DIR] [--display]
```

- Default: Saves plots to tmp/ without displaying
- `--display`: Show plots interactively
- `--save-dir DIR`: Save directory (default: 'tmp')
- `--start/--end DATE`: Date range (default: last year)

## Examples

### Complete Analysis Workflow

```python
from btc_indicators import fetch_btc_data, add_all_indicators, plot_all_indicators

# Fetch data
data = fetch_btc_data(start_date="2020-01-01")

# Calculate all indicators
data = add_all_indicators(data)

# Generate plots
plot_all_indicators(data, save_dir="plots/", show=True)

# Print latest values
latest = data.iloc[-1]
print(f"BTC Price: ${latest['Close']:,.2f}")
print(f"Mayer Multiple: {latest['Mayer_Multiple']:.2f}")
print(f"RSI: {latest['RSI']:.1f}")
print(f"MACD: {latest['MACD']:.2f}")
```

### MACD Trading Signals

```python
from btc_indicators import fetch_btc_data, calculate_macd

data = fetch_btc_data(start_date="2023-01-01")
data = calculate_macd(data)

# Identify crossovers
data['Signal'] = 0
data.loc[data['MACD'] > data['MACD_Signal'], 'Signal'] = 1   # Bullish
data.loc[data['MACD'] < data['MACD_Signal'], 'Signal'] = -1  # Bearish

# Recent signals
print(data[data['Signal'].diff() != 0][['Close', 'MACD', 'Signal']].tail())
```

## Testing

```bash
pip install -e ".[dev]"       # Install with dev dependencies
pytest                        # Run tests
pytest --cov=btc_indicators   # Run with coverage
```

## Data Storage

- **Location**: `data/` directory
- **Format**: Year-based CSV files (2023.csv, 2024.csv, etc.)
- **Features**: Automatic patching, no duplicates, incremental updates

## License

MIT License - see LICENSE file for details.

## Disclaimer

**Educational purposes only. Not financial advice.** Always do your own research before making investment decisions.

## Acknowledgments

- Data: [Yahoo Finance](https://finance.yahoo.com/) via [yfinance](https://github.com/ranaroussi/yfinance)
- Mayer Multiple: Concept by Trace Mayer
