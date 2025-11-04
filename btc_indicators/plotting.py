"""
Plotting and visualization module for BTC indicators.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from typing import Optional
import os
import numpy as np
from datetime import datetime


def plot_mayer_multiple(
    data: pd.DataFrame,
    save_path: Optional[str] = None,
    figsize: tuple = (14, 10),
    show: bool = True
) -> None:
    """
    Plot BTC price, 200-day MA, and Mayer Multiple indicator.
    
    Creates a multi-panel plot showing:
    - Panel 1: BTC price, 200-day moving average, and price levels for key Mayer Multiple thresholds
    - Panel 2: Mayer Multiple over time with reference lines and average
    
    Args:
        data: DataFrame with 'Close', '200_MA', 'Mayer_Multiple', 'Mayer_Multiple_Avg',
              'MM_0.8_Price', 'MM_1.3_Price', and 'MM_2.4_Price' columns
        save_path: Optional path to save the plot
        figsize: Figure size as (width, height) tuple
        show: Whether to display the plot
        
    Raises:
        ValueError: If required columns are missing
        
    Examples:
        >>> data = fetch_btc_data(start_date="2020-01-01")
        >>> data = calculate_mayer_multiple(data)
        >>> plot_mayer_multiple(data, save_path="mayer_multiple.png")
    """
    required_cols = ['Close', '200_MA', 'Mayer_Multiple', 'Mayer_Multiple_Avg', 
                     'MM_0.8_Price', 'MM_1.3_Price', 'MM_2.4_Price']
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Filter out NaN values
    plot_data = data[required_cols].dropna()
    
    if plot_data.empty:
        raise ValueError("No valid data to plot after removing NaN values")
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    fig.suptitle('Bitcoin Mayer Multiple Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Price and 200-day MA
    ax1.plot(plot_data.index, plot_data['Close'], label='BTC Price', color='#F7931A', linewidth=2)
    ax1.plot(plot_data.index, plot_data['200_MA'], label='200-day MA', color='#4A90E2', linewidth=2, linestyle='--')
    
    # Add price level lines for key Mayer Multiple thresholds
    ax1.plot(plot_data.index, plot_data['MM_0.8_Price'], label='MM 0.8 Price Level', 
             color='green', linewidth=1, linestyle=':', alpha=0.7)
    ax1.plot(plot_data.index, plot_data['MM_1.3_Price'], label='MM 1.3 Price Level', 
             color='orange', linewidth=1, linestyle=':', alpha=0.7)
    ax1.plot(plot_data.index, plot_data['MM_2.4_Price'], label='MM 2.4 Price Level', 
             color='red', linewidth=1, linestyle=':', alpha=0.7)
    
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('BTC Price vs 200-day Moving Average', fontsize=12, pad=10)
    
    # Format y-axis with commas
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Plot 2: Mayer Multiple
    ax2.plot(plot_data.index, plot_data['Mayer_Multiple'], label='Mayer Multiple', color='#50C878', linewidth=2)
    
    # Add reference lines
    ax2.axhline(y=1.0, color='gray', linestyle='-', linewidth=1, alpha=0.5, label='MM = 1.0')
    ax2.axhline(y=2.4, color='red', linestyle='--', linewidth=1, alpha=0.5, label='MM = 2.4 (Overbought)')
    ax2.axhline(y=0.8, color='green', linestyle='--', linewidth=1, alpha=0.5, label='MM = 0.8 (Oversold)')
    
    # Add average Mayer Multiple line
    avg_mm = plot_data['Mayer_Multiple_Avg'].iloc[0]
    ax2.axhline(y=avg_mm, color='purple', linestyle='-', linewidth=1.5, alpha=0.6, 
                label=f'Average MM = {avg_mm:.2f}')
    
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Mayer Multiple', fontsize=12)
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Mayer Multiple (Price / 200-day MA)', fontsize=12, pad=10)
    
    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    # Show if requested
    if show:
        plt.show()
    else:
        plt.close()


def plot_macd(
    data: pd.DataFrame,
    save_path: Optional[str] = None,
    figsize: tuple = (14, 10),
    show: bool = True
) -> None:
    """
    Plot BTC price and MACD indicator.
    
    Creates a multi-panel plot showing:
    - Panel 1: BTC price
    - Panel 2: MACD line, Signal line, and Histogram
    
    Args:
        data: DataFrame with 'Close', 'MACD', 'MACD_Signal', and 'MACD_Histogram' columns
        save_path: Optional path to save the plot
        figsize: Figure size as (width, height) tuple
        show: Whether to display the plot
        
    Raises:
        ValueError: If required columns are missing
        
    Examples:
        >>> data = fetch_btc_data(start_date="2020-01-01")
        >>> data = calculate_macd(data)
        >>> plot_macd(data, save_path="macd.png")
    """
    required_cols = ['Close', 'MACD', 'MACD_Signal', 'MACD_Histogram']
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Filter out NaN values
    plot_data = data[required_cols].dropna()
    
    if plot_data.empty:
        raise ValueError("No valid data to plot after removing NaN values")
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True, 
                                     gridspec_kw={'height_ratios': [2, 1]})
    fig.suptitle('Bitcoin MACD Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Price
    ax1.plot(plot_data.index, plot_data['Close'], label='BTC Price', color='#F7931A', linewidth=2)
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('BTC Price', fontsize=12, pad=10)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Plot 2: MACD
    ax2.plot(plot_data.index, plot_data['MACD'], label='MACD', color='#4A90E2', linewidth=2)
    ax2.plot(plot_data.index, plot_data['MACD_Signal'], label='Signal', color='#E94B3C', linewidth=2)
    
    # Plot histogram with colors
    colors = ['green' if val >= 0 else 'red' for val in plot_data['MACD_Histogram']]
    ax2.bar(plot_data.index, plot_data['MACD_Histogram'], label='Histogram', 
            color=colors, alpha=0.3, width=1)
    
    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('MACD Value', fontsize=12)
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_title('MACD (12, 26, 9)', fontsize=12, pad=10)
    
    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    # Show if requested
    if show:
        plt.show()
    else:
        plt.close()


def plot_rsi(
    data: pd.DataFrame,
    save_path: Optional[str] = None,
    figsize: tuple = (14, 10),
    show: bool = True
) -> None:
    """
    Plot BTC price and RSI indicator.
    
    Creates a multi-panel plot showing:
    - Panel 1: BTC price
    - Panel 2: RSI with overbought/oversold zones
    
    Args:
        data: DataFrame with 'Close' and 'RSI' columns
        save_path: Optional path to save the plot
        figsize: Figure size as (width, height) tuple
        show: Whether to display the plot
        
    Raises:
        ValueError: If required columns are missing
        
    Examples:
        >>> data = fetch_btc_data(start_date="2020-01-01")
        >>> data = calculate_rsi(data)
        >>> plot_rsi(data, save_path="rsi.png")
    """
    required_cols = ['Close', 'RSI']
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Filter out NaN values
    plot_data = data[required_cols].dropna()
    
    if plot_data.empty:
        raise ValueError("No valid data to plot after removing NaN values")
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True,
                                     gridspec_kw={'height_ratios': [2, 1]})
    fig.suptitle('Bitcoin RSI Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Price
    ax1.plot(plot_data.index, plot_data['Close'], label='BTC Price', color='#F7931A', linewidth=2)
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('BTC Price', fontsize=12, pad=10)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Plot 2: RSI
    ax2.plot(plot_data.index, plot_data['RSI'], label='RSI', color='#9B59B6', linewidth=2)
    
    # Add overbought/oversold zones
    ax2.axhline(y=70, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Overbought (70)')
    ax2.axhline(y=30, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Oversold (30)')
    ax2.fill_between(plot_data.index, 70, 100, alpha=0.1, color='red')
    ax2.fill_between(plot_data.index, 0, 30, alpha=0.1, color='green')
    
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('RSI', fontsize=12)
    ax2.set_ylim(0, 100)
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Relative Strength Index (14)', fontsize=12, pad=10)
    
    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    # Show if requested
    if show:
        plt.show()
    else:
        plt.close()


def plot_all_indicators(
    data: pd.DataFrame,
    save_dir: Optional[str] = None,
    show: bool = True
) -> None:
    """
    Generate all available indicator plots.
    
    Args:
        data: DataFrame with all indicator columns
        save_dir: Optional directory to save plots
        show: Whether to display the plots
    """
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
    
    # Plot Mayer Multiple if available
    if all(col in data.columns for col in ['Close', '200_MA', 'Mayer_Multiple', 'Mayer_Multiple_Avg']):
        save_path = os.path.join(save_dir, 'mayer_multiple.png') if save_dir else None
        try:
            plot_mayer_multiple(data, save_path=save_path, show=show)
        except Exception as e:
            print(f"Error plotting Mayer Multiple: {e}")
    
    # Plot MACD if available
    if all(col in data.columns for col in ['Close', 'MACD', 'MACD_Signal', 'MACD_Histogram']):
        save_path = os.path.join(save_dir, 'macd.png') if save_dir else None
        try:
            plot_macd(data, save_path=save_path, show=show)
        except Exception as e:
            print(f"Error plotting MACD: {e}")
    
    # Plot RSI if available
    if all(col in data.columns for col in ['Close', 'RSI']):
        save_path = os.path.join(save_dir, 'rsi.png') if save_dir else None
        try:
            plot_rsi(data, save_path=save_path, show=show)
        except Exception as e:
            print(f"Error plotting RSI: {e}")

    # Plot Power Law if available
    if all(col in data.columns for col in ['Close', 't', 'PowerLaw_Fair', 'PowerLaw_Lower', 'PowerLaw_Upper']):
        save_path = os.path.join(save_dir, 'power_law.png') if save_dir else None
        try:
            plot_power_law(data, save_path=save_path, show=show)
        except Exception as e:
            print(f"Error plotting Power Law: {e}")


def plot_power_law(
    data: pd.DataFrame,
    save_path: Optional[str] = None,
    figsize: tuple = (12, 8),
    show: bool = True,
    show_future: bool = False,
    years_ahead: float = 10.0,
    future_points: int = 500
) -> None:
    """
    Plot a log-log chart of BTC price vs time since genesis with power law curves.

    Renders a separate plot with historical Close prices against years since
    genesis (t), along with the power law fair value and bands. Optionally
    extends the fair value and bands into the future.

    Args:
        data: DataFrame with columns 'Close', 't', 'PowerLaw_Fair',
              'PowerLaw_Lower', 'PowerLaw_Upper'.
        save_path: Optional path to save the plot image.
        figsize: Figure size (width, height).
        show: Whether to display the plot.
        show_future: Whether to draw future projections.
        years_ahead: Number of years to project into the future (default 20).
        future_points: Number of points to use for future curves.

    Raises:
        ValueError: If required columns are missing or no data to plot.
    """
    required_cols = ['Close', 't', 'PowerLaw_Fair', 'PowerLaw_Lower', 'PowerLaw_Upper']
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Do not drop rows globally; instead mask each series to retain as much as possible from earliest date
    df = data[required_cols].copy()
    if df.empty:
        raise ValueError("No data available to plot")

    x_dates = df.index

    fig, ax = plt.subplots(figsize=figsize)
    # Close prices: show where available and > 0 on log scale
    close_mask = df['Close'].notna() & (df['Close'] > 0)
    ax.plot(x_dates[close_mask], df.loc[close_mask, 'Close'], label='Historical BTC Price', color='black', linewidth=1)
    # Power law curves: avoid zeros/negatives for log scale
    fair_mask = df['PowerLaw_Fair'].notna() & (df['PowerLaw_Fair'] > 0)
    lower_mask = df['PowerLaw_Lower'].notna() & (df['PowerLaw_Lower'] > 0)
    upper_mask = df['PowerLaw_Upper'].notna() & (df['PowerLaw_Upper'] > 0)
    ax.plot(x_dates[fair_mask], df.loc[fair_mask, 'PowerLaw_Fair'], label='Power Law Fair Price', color='blue', linestyle='--')
    ax.plot(x_dates[lower_mask], df.loc[lower_mask, 'PowerLaw_Lower'], label='Lower Band (0.5x)', color='green', linestyle=':')
    ax.plot(x_dates[upper_mask], df.loc[upper_mask, 'PowerLaw_Upper'], label='Upper Band (3x)', color='red', linestyle=':')
    ax.set_yscale('log')

    # Optional future projection using default constants (to match indicator defaults)
    if show_future:
        # Derive an approximate genesis date from current data and t
        days_per_year = 365.25
        t_series = df['t'].dropna()
        if not t_series.empty:
            first_date = t_series.index[0]
            first_t = float(t_series.iloc[0])
            try:
                genesis_dt = first_date - pd.to_timedelta(first_t * days_per_year, unit='D')
            except Exception:
                genesis_dt = first_date

            A = 10 ** (-1.847796462)
            B = 5.616314045
            current_t = float(t_series.iloc[-1])
            t_future = np.linspace(current_t, current_t + float(years_ahead), int(future_points))
            future_fair = A * (t_future ** B)
            future_lower = 0.5 * future_fair
            future_upper = 3.0 * future_fair
            future_dates = genesis_dt + pd.to_timedelta(t_future * days_per_year, unit='D')

            ax.plot(future_dates, future_fair, color='blue', linestyle='--', alpha=0.7)
            ax.plot(future_dates, future_lower, color='green', linestyle=':', alpha=0.7)
            ax.plot(future_dates, future_upper, color='red', linestyle=':', alpha=0.7)

    ax.set_xlabel('Date')
    ax.set_ylabel('Bitcoin Price (USD, log scale)')
    ax.set_title('Bitcoin Price Power Law Curve')
    ax.legend()
    ax.grid(True, which='both', ls='--', alpha=0.5)

    # Format x-axis as dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")

    if show:
        plt.show()
    else:
        plt.close()

