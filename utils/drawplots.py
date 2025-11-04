#!/usr/bin/env python3
"""
Utility script to generate indicator plots from local CSV data.

This script loads BTC data from CSV files, calculates all available indicators,
and generates visualizations. By default, plots are saved to tmp/ directory
and are NOT displayed unless --display flag is specified.
"""

import sys
import os
import argparse
from datetime import datetime, timedelta

# Add parent directory to path to import btc_indicators
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from btc_indicators import (
    load_data_from_csv,
    add_all_indicators,
    plot_all_indicators,
    calculate_power_law,
    plot_power_law
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate BTC indicator plots from local CSV data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and save plots to tmp/ (no display)
  python drawplots.py
  
  # Generate, save to tmp/, and display plots
  python drawplots.py --display
  
  # Save to custom directory without displaying
  python drawplots.py --save-dir plots/
  
  # Display and save to custom directory
  python drawplots.py --save-dir plots/ --display
  
  # Plot specific date range
  python drawplots.py --start 2020-01-01 --end 2023-12-31 --display
  
  # Use custom data directory
  python drawplots.py --data-dir custom_data/ --display
        """
    )
    
    parser.add_argument(
        '--start',
        type=str,
        default=None,
        help='Start date (YYYY-MM-DD). Default: 1 year ago'
    )
    
    parser.add_argument(
        '--end',
        type=str,
        default=None,
        help='End date (YYYY-MM-DD). Default: today'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data',
        help='Directory containing CSV data files. Default: data/'
    )
    
    parser.add_argument(
        '--save-dir',
        type=str,
        default='tmp',
        help='Directory to save plots. Default: tmp/'
    )
    
    parser.add_argument(
        '--display',
        action='store_true',
        help='Display plots interactively (default: False, only save)'
    )
    
    return parser.parse_args()


def main():
    """Main function to generate indicator plots."""
    args = parse_args()
    
    print("=" * 70)
    print("BTC Indicator Plots Generator")
    print("=" * 70)
    print()
    
    # Set default dates
    if args.end is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        end_date = args.end
    
    if args.start is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    else:
        start_date = args.start
    
    print(f"Loading data from {start_date} to {end_date}...")
    print(f"Data directory: {args.data_dir}")
    print()
    
    # Load data
    try:
        data = load_data_from_csv(
            start_date=start_date,
            end_date=end_date,
            data_dir=args.data_dir
        )
        
        if data.empty:
            print("ERROR: No data found in CSV files for the specified date range.")
            print()
            print("Please run fetchdata.py first to download BTC data:")
            print("  python utils/fetchdata.py")
            sys.exit(1)
        
        print(f"Loaded {len(data)} records")
        print(f"Date range: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}")
        print()
        
    except Exception as e:
        print(f"ERROR: Failed to load data: {e}")
        sys.exit(1)
    
    # Calculate indicators
    print("Calculating indicators...")
    try:
        data = add_all_indicators(data)
        # Add power law curves for plotting
        try:
            data = calculate_power_law(data)
        except Exception as e:
            print(f"Warning: Could not calculate Power Law: {e}")
        print("✓ All indicators calculated")
        print()
    except Exception as e:
        print(f"ERROR: Failed to calculate indicators: {e}")
        sys.exit(1)
    
    # Generate plots
    print("Generating plots...")
    print(f"Save directory: {args.save_dir}")
    print(f"Display plots: {'Yes' if args.display else 'No'}")
    print()
    
    try:
        plot_all_indicators(
            data,
            save_dir=args.save_dir,
            show=args.display
        )

        # Ensure power law plot includes the entire history from earliest available price
        try:
            # Reload full history irrespective of --start to ensure earliest available price is included
            full_data = load_data_from_csv(
                start_date='2009-01-01',
                end_date=end_date,
                data_dir=args.data_dir
            )
            pl_data = calculate_power_law(full_data)
            save_path = os.path.join(args.save_dir, 'power_law.png') if args.save_dir else None
            plot_power_law(
                pl_data,
                save_path=save_path,
                show=args.display,
                show_future=True,
                years_ahead=10.0,
                future_points=500
            )
        except Exception as e:
            print(f"Warning: Could not render Power Law with full history: {e}")
        
        print()
        print(f"✓ Plots saved to {args.save_dir}/")
        print(f"  - mayer_multiple.png")
        print(f"  - macd.png")
        print(f"  - rsi.png")
        print(f"  - power_law.png")
        
        if args.display:
            print("✓ Plots displayed interactively")
        
        print()
        print("=" * 70)
        print("Plot generation completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"ERROR: Failed to generate plots: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

