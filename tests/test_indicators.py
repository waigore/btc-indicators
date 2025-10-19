"""
Unit tests for btc_indicators.indicators module.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from btc_indicators.indicators import (
    calculate_mayer_multiple,
    calculate_macd,
    calculate_rsi,
    add_all_indicators
)


class TestCalculateMayerMultiple:
    """Tests for calculate_mayer_multiple function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Create sample data
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        self.data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
    
    def test_calculate_mayer_multiple(self):
        """Test basic Mayer Multiple calculation."""
        result = calculate_mayer_multiple(self.data)
        
        assert '200_MA' in result.columns
        assert 'Mayer_Multiple' in result.columns
        assert 'Mayer_Multiple_Avg' in result.columns
        
        # Check that calculations are correct
        ma_200 = result['Close'].rolling(window=200).mean()
        expected_mm = result['Close'] / ma_200
        
        # Compare non-NaN values
        valid_mask = ~result['Mayer_Multiple'].isna()
        pd.testing.assert_series_equal(
            result['Mayer_Multiple'][valid_mask],
            expected_mm[valid_mask],
            check_names=False
        )
        
        # Check that average is calculated correctly
        expected_avg = result['Mayer_Multiple'].mean()
        assert result['Mayer_Multiple_Avg'].iloc[0] == pytest.approx(expected_avg)
        
        # Check that average is consistent across all rows
        assert result['Mayer_Multiple_Avg'].nunique() == 1
    
    def test_insufficient_data(self):
        """Test that insufficient data raises ValueError."""
        short_data = self.data.iloc[:100]
        
        with pytest.raises(ValueError, match="Insufficient data"):
            calculate_mayer_multiple(short_data)
    
    def test_missing_close_column(self):
        """Test that missing Close column raises ValueError."""
        bad_data = self.data.drop('Close', axis=1)
        
        with pytest.raises(ValueError, match="must contain 'Close' column"):
            calculate_mayer_multiple(bad_data)
    
    def test_custom_window(self):
        """Test Mayer Multiple with custom window."""
        window = 50
        result = calculate_mayer_multiple(self.data, window=window)
        
        assert f'{window}_MA' in result.columns
        assert 'Mayer_Multiple' in result.columns
        
        # First 49 values should be NaN
        assert result['Mayer_Multiple'].iloc[:window-1].isna().all()
        
        # Values after window should not be NaN
        assert not result['Mayer_Multiple'].iloc[window:].isna().all()
    
    def test_original_data_not_modified(self):
        """Test that original DataFrame is not modified."""
        original_cols = set(self.data.columns)
        result = calculate_mayer_multiple(self.data)
        
        # Original should not have new columns
        assert set(self.data.columns) == original_cols
        
        # Result should have new columns
        assert '200_MA' in result.columns
        assert 'Mayer_Multiple' in result.columns


class TestCalculateMACD:
    """Tests for calculate_macd function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        self.data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
    
    def test_calculate_macd(self):
        """Test basic MACD calculation."""
        result = calculate_macd(self.data)
        
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
        
        # Check histogram calculation
        expected_hist = result['MACD'] - result['MACD_Signal']
        pd.testing.assert_series_equal(
            result['MACD_Histogram'],
            expected_hist,
            check_names=False
        )
    
    def test_custom_parameters(self):
        """Test MACD with custom parameters."""
        result = calculate_macd(self.data, fast=5, slow=13, signal=5)
        
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
    
    def test_insufficient_data(self):
        """Test that insufficient data raises ValueError."""
        short_data = self.data.iloc[:20]
        
        with pytest.raises(ValueError, match="Insufficient data"):
            calculate_macd(short_data)
    
    def test_missing_close_column(self):
        """Test that missing Close column raises ValueError."""
        bad_data = self.data.drop('Close', axis=1)
        
        with pytest.raises(ValueError, match="must contain 'Close' column"):
            calculate_macd(bad_data)
    
    def test_invalid_parameters(self):
        """Test that invalid parameters raise ValueError."""
        with pytest.raises(ValueError, match="Fast period .* must be less than slow period"):
            calculate_macd(self.data, fast=26, slow=12)
    
    def test_custom_price_column(self):
        """Test MACD with custom price column."""
        result = calculate_macd(self.data, price_col='High')
        
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
    
    def test_original_data_not_modified(self):
        """Test that original DataFrame is not modified."""
        original_cols = set(self.data.columns)
        result = calculate_macd(self.data)
        
        assert set(self.data.columns) == original_cols
        assert 'MACD' in result.columns


class TestCalculateRSI:
    """Tests for calculate_rsi function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        self.data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
    
    def test_calculate_rsi(self):
        """Test basic RSI calculation."""
        result = calculate_rsi(self.data)
        
        assert 'RSI' in result.columns
        
        # RSI should be between 0 and 100
        valid_rsi = result['RSI'].dropna()
        assert (valid_rsi >= 0).all()
        assert (valid_rsi <= 100).all()
    
    def test_custom_period(self):
        """Test RSI with custom period."""
        period = 7
        result = calculate_rsi(self.data, period=period)
        
        assert 'RSI' in result.columns
        
        # First few values should be NaN
        assert result['RSI'].iloc[:period].isna().any()
    
    def test_insufficient_data(self):
        """Test that insufficient data raises ValueError."""
        short_data = self.data.iloc[:10]
        
        with pytest.raises(ValueError, match="Insufficient data"):
            calculate_rsi(short_data)
    
    def test_missing_close_column(self):
        """Test that missing Close column raises ValueError."""
        bad_data = self.data.drop('Close', axis=1)
        
        with pytest.raises(ValueError, match="must contain 'Close' column"):
            calculate_rsi(bad_data)
    
    def test_custom_price_column(self):
        """Test RSI with custom price column."""
        result = calculate_rsi(self.data, price_col='High')
        
        assert 'RSI' in result.columns
    
    def test_original_data_not_modified(self):
        """Test that original DataFrame is not modified."""
        original_cols = set(self.data.columns)
        result = calculate_rsi(self.data)
        
        assert set(self.data.columns) == original_cols
        assert 'RSI' in result.columns


class TestAddAllIndicators:
    """Tests for add_all_indicators function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        self.data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
    
    def test_add_all_indicators(self):
        """Test adding all indicators at once."""
        result = add_all_indicators(self.data)
        
        # Check that all indicator columns are present
        assert '200_MA' in result.columns
        assert 'Mayer_Multiple' in result.columns
        assert 'Mayer_Multiple_Avg' in result.columns
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns
        assert 'RSI' in result.columns
    
    def test_with_insufficient_data(self):
        """Test that function handles insufficient data gracefully."""
        short_data = self.data.iloc[:100]
        
        # Should not raise, but should print warnings
        result = add_all_indicators(short_data)
        
        # Should still return a DataFrame
        assert isinstance(result, pd.DataFrame)
    
    def test_original_data_not_modified(self):
        """Test that original DataFrame is not modified."""
        original_cols = set(self.data.columns)
        result = add_all_indicators(self.data)
        
        assert set(self.data.columns) == original_cols

