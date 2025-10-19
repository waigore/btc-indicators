#!/usr/bin/env python3
"""
Utility script to fetch BTC-USD data and update CSV files.

This script can fetch data in two modes:
1. Auto mode (default): Fetches from the last recorded data point to today
2. Manual mode: Fetches data between arbitrary date ranges using --start and --end flags

Examples:
    # Fetch latest data (from last data point to today)
    python fetchdata.py
    
    # Fetch specific date range
    python fetchdata.py --start 2020-01-01 --end 2023-12-31
    
    # Fetch from specific start date to today
    python fetchdata.py --start 2023-01-01
    
    # Fetch up to specific end date
    python fetchdata.py --end 2024-12-31
"""

import sys
import os
import argparse
from datetime import datetime, timedelta

# Add parent directory to path to import btc_indicators
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from btc_indicators import fetch_btc_data, load_data_from_csv


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Fetch BTC-USD data and update local CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch latest data (from last data point to today)
  python fetchdata.py
  
  # Fetch specific date range
  python fetchdata.py --start 2020-01-01 --end 2023-12-31
  
  # Fetch from specific start date to today
  python fetchdata.py --start 2023-01-01
  
  # Fetch up to specific end date
  python fetchdata.py --end 2024-12-31
  
  # Use custom data directory
  python fetchdata.py --data-dir custom_data/
        """
    )
    
    parser.add_argument(
        '--start',
        type=str,
        default=None,
        help='Start date in YYYY-MM-DD format'
    )
    
    parser.add_argument(
        '--end',
        type=str,
        default=None,
        help='End date in YYYY-MM-DD format'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data',
        help='Directory for CSV data files. Default: data/'
    )
    
    return parser.parse_args()


def main():
    """Main function to fetch and update BTC data."""
    args = parse_args()
    
    print("=" * 70)
    print("BTC Data Fetcher - Update Local CSV Database")
    print("=" * 70)
    print()
    
    # Determine start and end dates
    start_date = args.start
    end_date = args.end
    
    # If no dates provided, use auto mode (fetch from last data point)
    if start_date is None and end_date is None:
        print("Mode: AUTO (fetching from last data point to today)")
        print()
        
        # Try to determine the last data point
        try:
            # Load the most recent data
            existing_data = load_data_from_csv(
                start_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                end_date=datetime.now().strftime('%Y-%m-%d'),
                data_dir=args.data_dir
            )
            
            if not existing_data.empty:
                last_date = existing_data.index.max()
                print(f"Last recorded data point: {last_date.strftime('%Y-%m-%d')}")
                
                # Fetch from the day after last recorded date
                start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                print("No existing data found. Fetching last 30 days...")
                start_date = None
        except Exception as e:
            print(f"Could not determine last data point: {e}")
            print("Fetching last 30 days...")
            start_date = None
        
        # Default end date to today
        end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        print("Mode: MANUAL (custom date range)")
        print()
        
        # If only end date provided, try to get from last data point or 30 days ago
        if start_date is None:
            try:
                existing_data = load_data_from_csv(
                    start_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                    end_date=end_date,
                    data_dir=args.data_dir
                )
                
                if not existing_data.empty:
                    last_date = existing_data.index.max()
                    print(f"Last recorded data point: {last_date.strftime('%Y-%m-%d')}")
                    start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    # No existing data, use 30 days before end date
                    if end_date:
                        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                        start_date = (end_dt - timedelta(days=30)).strftime('%Y-%m-%d')
                    else:
                        start_date = None
            except Exception as e:
                print(f"Could not determine start date: {e}")
                start_date = None
        
        # If only start date provided, default end to today
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
    
    print()
    print("Fetching BTC-USD data...")
    print(f"Data directory: {args.data_dir}")
    print(f"Start date: {start_date if start_date else 'Last 30 days'}")
    print(f"End date: {end_date}")
    print()
    
    try:
        data = fetch_btc_data(
            start_date=start_date,
            end_date=end_date,
            data_dir=args.data_dir
        )
        
        print()
        print("=" * 70)
        print("Fetch completed successfully!")
        print(f"Total records in returned dataset: {len(data)}")
        
        if not data.empty:
            print(f"Date range: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}")
            print(f"Latest BTC price: ${data['Close'].iloc[-1]:,.2f}")
        else:
            print("No data returned (possibly already up to date)")
        
        print("=" * 70)
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"ERROR: Failed to fetch data: {e}")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()

