"""
Data fetching and persistence module for BTC-USD historical data.
"""

import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


def fetch_btc_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = "1d",
    data_dir: str = "data"
) -> pd.DataFrame:
    """
    Fetch BTC-USD historical data from Yahoo Finance and persist as year-based CSVs.
    
    This function intelligently manages local CSV files organized by year (e.g., 2015.csv, 
    2016.csv). It loads existing data when available and patches it with newly fetched data,
    avoiding unnecessary API calls and preserving historical data.
    
    Args:
        start_date: Start date in 'YYYY-MM-DD' format. Defaults to one month ago.
        end_date: End date in 'YYYY-MM-DD' format. Defaults to today.
        interval: Data interval ('1d', '1h', etc.). Default is '1d'.
        data_dir: Directory to store CSV files. Default is 'data'.
        
    Returns:
        pandas.DataFrame: OHLCV data with DatetimeIndex
        
    Examples:
        >>> # Fetch last month of data (default)
        >>> data = fetch_btc_data()
        
        >>> # Fetch specific date range
        >>> data = fetch_btc_data(start_date="2020-01-01", end_date="2023-12-31")
    """
    # Set default dates
    if end_date is None:
        end_date_dt = datetime.now()
    else:
        end_date_dt = pd.to_datetime(end_date)
    
    if start_date is None:
        start_date_dt = end_date_dt - timedelta(days=30)
    else:
        start_date_dt = pd.to_datetime(start_date)
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Determine which years we need
    years_needed = range(start_date_dt.year, end_date_dt.year + 1)
    
    # Load existing data and identify gaps
    all_data = []
    fetch_start = start_date_dt
    fetch_end = end_date_dt
    
    for year in years_needed:
        csv_path = os.path.join(data_dir, f"{year}.csv")
        if os.path.exists(csv_path):
            try:
                year_data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                all_data.append(year_data)
            except Exception as e:
                print(f"Warning: Could not load {csv_path}: {e}")
    
    # Combine existing data
    if all_data:
        existing_df = pd.concat(all_data).sort_index()
        # Remove duplicates, keeping last
        existing_df = existing_df[~existing_df.index.duplicated(keep='last')]
    else:
        existing_df = pd.DataFrame()
    
    # Fetch new data from Yahoo Finance
    print(f"Fetching BTC-USD data from {start_date_dt.date()} to {end_date_dt.date()}...")
    btc = yf.Ticker("BTC-USD")
    new_data = btc.history(
        start=start_date_dt.strftime('%Y-%m-%d'),
        end=end_date_dt.strftime('%Y-%m-%d'),
        interval=interval
    )
    
    if new_data.empty:
        print("Warning: No new data fetched from Yahoo Finance.")
        if not existing_df.empty:
            # Filter existing data to requested range
            # Handle timezone compatibility
            filter_start = start_date_dt
            filter_end = end_date_dt
            
            if existing_df.index.tz is not None:
                # Convert datetime.datetime to pd.Timestamp if needed
                if not isinstance(filter_start, pd.Timestamp):
                    filter_start = pd.Timestamp(filter_start)
                if not isinstance(filter_end, pd.Timestamp):
                    filter_end = pd.Timestamp(filter_end)
                
                if filter_start.tz is None:
                    filter_start = filter_start.tz_localize('UTC')
                if filter_end.tz is None:
                    filter_end = filter_end.tz_localize('UTC')
            
            mask = (existing_df.index >= filter_start) & (existing_df.index <= filter_end)
            return existing_df[mask]
        return pd.DataFrame()
    
    # Combine existing and new data
    if not existing_df.empty:
        combined_df = pd.concat([existing_df, new_data])
        # Remove duplicates, keeping last (newer data)
        combined_df = combined_df[~combined_df.index.duplicated(keep='last')]
        combined_df.sort_index(inplace=True)
    else:
        combined_df = new_data
    
    # Save data by year
    for year in years_needed:
        year_start = pd.Timestamp(f"{year}-01-01", tz='UTC')
        year_end = pd.Timestamp(f"{year}-12-31 23:59:59", tz='UTC')
        
        # Handle timezone-aware and naive indices
        if combined_df.index.tz is None:
            year_start = year_start.tz_localize(None)
            year_end = year_end.tz_localize(None)
        
        year_mask = (combined_df.index >= year_start) & (combined_df.index <= year_end)
        year_data = combined_df[year_mask]
        
        if not year_data.empty:
            csv_path = os.path.join(data_dir, f"{year}.csv")
            year_data.to_csv(csv_path)
            print(f"Saved {len(year_data)} records to {csv_path}")
    
    # Return data for requested range
    # Handle timezone compatibility
    if combined_df.index.tz is not None:
        # Convert datetime.datetime to pd.Timestamp if needed
        if not isinstance(start_date_dt, pd.Timestamp):
            start_date_dt = pd.Timestamp(start_date_dt)
        if not isinstance(end_date_dt, pd.Timestamp):
            end_date_dt = pd.Timestamp(end_date_dt)
        
        if start_date_dt.tz is None:
            start_date_dt = start_date_dt.tz_localize('UTC')
        if end_date_dt.tz is None:
            end_date_dt = end_date_dt.tz_localize('UTC')
    
    mask = (combined_df.index >= start_date_dt) & (combined_df.index <= end_date_dt)
    result_df = combined_df[mask]
    
    print(f"Returned {len(result_df)} records from {result_df.index.min().date()} to {result_df.index.max().date()}")
    return result_df


def load_data_from_csv(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    data_dir: str = "data"
) -> pd.DataFrame:
    """
    Load BTC-USD data from local CSV files without fetching from API.
    
    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        data_dir: Directory containing CSV files
        
    Returns:
        pandas.DataFrame: OHLCV data with DatetimeIndex
    """
    # Set default dates if not provided
    if end_date is None:
        end_date_dt = datetime.now()
    else:
        end_date_dt = pd.to_datetime(end_date)
    
    if start_date is None:
        start_date_dt = end_date_dt - timedelta(days=30)
    else:
        start_date_dt = pd.to_datetime(start_date)
    
    # Determine which years we need
    years_needed = range(start_date_dt.year, end_date_dt.year + 1)
    
    # Load data from CSV files
    all_data = []
    for year in years_needed:
        csv_path = os.path.join(data_dir, f"{year}.csv")
        if os.path.exists(csv_path):
            try:
                year_data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                all_data.append(year_data)
            except Exception as e:
                print(f"Warning: Could not load {csv_path}: {e}")
    
    if not all_data:
        return pd.DataFrame()
    
    # Combine and filter
    df = pd.concat(all_data).sort_index()
    df = df[~df.index.duplicated(keep='last')]
    
    # Filter to requested range
    # Handle timezone compatibility
    if df.index.tz is not None:
        # Convert datetime.datetime to pd.Timestamp if needed
        if not isinstance(start_date_dt, pd.Timestamp):
            start_date_dt = pd.Timestamp(start_date_dt)
        if not isinstance(end_date_dt, pd.Timestamp):
            end_date_dt = pd.Timestamp(end_date_dt)
        
        if start_date_dt.tz is None:
            start_date_dt = start_date_dt.tz_localize('UTC')
        if end_date_dt.tz is None:
            end_date_dt = end_date_dt.tz_localize('UTC')
    
    mask = (df.index >= start_date_dt) & (df.index <= end_date_dt)
    return df[mask]

