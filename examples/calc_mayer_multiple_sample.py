"""
Example script demonstrating Mayer Multiple calculation using btc-indicators library.

This is an updated version of the original sample that uses the btc-indicators library
instead of directly calling yfinance.
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import btc_indicators
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from btc_indicators import fetch_btc_data, calculate_mayer_multiple, plot_mayer_multiple


def main():
    """Calculate and display Mayer Multiple for BTC."""
    print("=" * 70)
    print("BTC Mayer Multiple Calculator")
    print("=" * 70)
    print()
    
    # Fetch 10 years of daily BTC-USD data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 10 + 3)  # Approx 10 years + buffer
    
    print(f"Fetching BTC-USD data from {start_date.date()} to {end_date.date()}...")
    
    try:
        data = fetch_btc_data(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            data_dir='data'
        )
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    
    # Ensure we have enough data for 200-day MA
    if len(data) < 200:
        print(f"Error: Not enough data for 200-day moving average.")
        print(f"Need at least 200 days, got {len(data)} days.")
        sys.exit(1)
    
    print(f"Fetched {len(data)} days of data")
    print()
    
    # Calculate the Mayer Multiple
    print("Calculating Mayer Multiple...")
    data = calculate_mayer_multiple(data)
    
    # Get the latest values
    latest_data = data.iloc[-1]
    current_price = latest_data['Close']
    ma_200 = latest_data['200_MA']
    mayer_multiple = latest_data['Mayer_Multiple']
    
    # Display results
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Date: {data.index[-1].strftime('%Y-%m-%d')}")
    print(f"Current BTC Price (USD): ${current_price:,.2f}")
    print(f"200-day Moving Average (USD): ${ma_200:,.2f}")
    print(f"Mayer Multiple: {mayer_multiple:.2f}")
    print()
    
    # Interpretation
    print("Interpretation:")
    if mayer_multiple > 2.4:
        print("  ⚠️  Potentially OVERBOUGHT (MM > 2.4)")
    elif mayer_multiple < 0.8:
        print("  ✓ Potentially OVERSOLD (MM < 0.8)")
    else:
        print("  → Normal range (0.8 < MM < 2.4)")
    
    print("=" * 70)
    print()
    
    # Save the data with Mayer Multiple
    output_file = "btc_mayer_multiple.csv"
    data[['Close', '200_MA', 'Mayer_Multiple']].to_csv(output_file)
    print(f"Data saved to {output_file}")
    
    # Ask if user wants to plot
    try:
        response = input("\nGenerate Mayer Multiple plot? (y/n): ").strip().lower()
        if response == 'y':
            print("Generating plot...")
            plot_mayer_multiple(data, save_path="mayer_multiple_plot.png", show=True)
            print("Plot saved as mayer_multiple_plot.png")
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Could not generate plot: {e}")


if __name__ == "__main__":
    main()

