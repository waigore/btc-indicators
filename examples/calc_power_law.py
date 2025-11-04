import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Define constants from the power law model on https://b1m.io/curve
GENESIS_DATE = datetime(2009, 1, 3)
A = 10 ** (-1.847796462)  # Scaling factor
B = 5.616314045           # Exponent
DAYS_PER_YEAR = 365.25    # Accounts for leap years
LOWER_MULTIPLIER = 0.5    # Lower band
UPPER_MULTIPLIER = 3.0    # Upper band

# Download historical daily Bitcoin prices (BTC-USD)
# yfinance provides data from 2014-09-17 onwards
data = yf.download('BTC-USD', period='max', interval='1d')
data = data.dropna()  # Ensure no missing data
data['Close'].replace(0, np.nan, inplace=True)  # Avoid zero prices if any
data = data.dropna(subset=['Close'])

# Calculate days since Genesis Block
data['Date'] = data.index
data['Days'] = (data['Date'] - GENESIS_DATE).dt.days
data = data[data['Days'] >= 0].copy()  # Filter to post-genesis

# Normalized time
data['t'] = data['Days'] / DAYS_PER_YEAR

# Compute power law fair price
data['Fair_Price'] = A * (data['t'] ** B)

# Compute bands
data['Lower_Band'] = LOWER_MULTIPLIER * data['Fair_Price']
data['Upper_Band'] = UPPER_MULTIPLIER * data['Fair_Price']

# Prepare for log-log plot (use Close prices > 0)
plot_data = data[data['Close'] > 0].copy()
x = plot_data['t']
y = plot_data['Close']

# Create log-log plot
plt.figure(figsize=(12, 8))
plt.loglog(x, y, label='Historical BTC Price', color='black', linewidth=1)
plt.loglog(x, plot_data['Fair_Price'], label='Power Law Fair Price', color='blue', linestyle='--')
plt.loglog(x, plot_data['Lower_Band'], label='Lower Band (0.5x)', color='green', linestyle=':')
plt.loglog(x, plot_data['Upper_Band'], label='Upper Band (3x)', color='red', linestyle=':')

# Add labels, title, and grid
plt.xlabel('Time since Genesis (years, log scale)')
plt.ylabel('Bitcoin Price (USD, log scale)')
plt.title('Bitcoin Price Power Law Curve (Log-Log Plot)')
plt.legend()
plt.grid(True, which='both', ls='--', alpha=0.5)

# Optional: Extend the curve into the future (e.g., next 10 years)
current_t = data['t'].iloc[-1]
future_years = np.linspace(current_t, current_t + 10, 500)
future_fair = A * (future_years ** B)
future_lower = LOWER_MULTIPLIER * future_fair
future_upper = UPPER_MULTIPLIER * future_fair

plt.loglog(future_years, future_fair, color='blue', linestyle='--', alpha=0.7)
plt.loglog(future_years, future_lower, color='green', linestyle=':', alpha=0.7)
plt.loglog(future_years, future_upper, color='red', linestyle=':', alpha=0.7)

plt.show()