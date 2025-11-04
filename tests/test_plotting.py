"""
Unit tests for btc_indicators.plotting module.
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from btc_indicators.plotting import (
    plot_mayer_multiple,
    plot_macd,
    plot_rsi,
    plot_all_indicators,
    plot_power_law
)
from btc_indicators.indicators import (
    calculate_mayer_multiple,
    calculate_macd,
    calculate_rsi,
    calculate_power_law
)


class TestPlotMayerMultiple:
    """Tests for plot_mayer_multiple function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Create sample data with indicators
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
        
        self.data = calculate_mayer_multiple(data)
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        plt.close('all')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_plot_without_save(self):
        """Test plotting without saving."""
        # Should not raise
        plot_mayer_multiple(self.data, show=False)
    
    def test_plot_with_save(self):
        """Test plotting with saving to file."""
        save_path = os.path.join(self.test_dir, 'mayer_multiple.png')
        plot_mayer_multiple(self.data, save_path=save_path, show=False)
        
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 0
    
    def test_missing_columns(self):
        """Test that missing columns raise ValueError."""
        bad_data = self.data.drop('Mayer_Multiple', axis=1)
        
        with pytest.raises(ValueError, match="Missing required columns"):
            plot_mayer_multiple(bad_data, show=False)
    
    def test_empty_data_after_dropna(self):
        """Test that all-NaN data raises ValueError."""
        bad_data = self.data.copy()
        bad_data['Mayer_Multiple'] = np.nan
        
        with pytest.raises(ValueError, match="No valid data to plot"):
            plot_mayer_multiple(bad_data, show=False)
    
    def test_custom_figsize(self):
        """Test plotting with custom figure size."""
        plot_mayer_multiple(self.data, figsize=(10, 8), show=False)


class TestPlotMACD:
    """Tests for plot_macd function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
        
        self.data = calculate_macd(data)
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        plt.close('all')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_plot_without_save(self):
        """Test plotting without saving."""
        plot_macd(self.data, show=False)
    
    def test_plot_with_save(self):
        """Test plotting with saving to file."""
        save_path = os.path.join(self.test_dir, 'macd.png')
        plot_macd(self.data, save_path=save_path, show=False)
        
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 0
    
    def test_missing_columns(self):
        """Test that missing columns raise ValueError."""
        bad_data = self.data.drop('MACD', axis=1)
        
        with pytest.raises(ValueError, match="Missing required columns"):
            plot_macd(bad_data, show=False)
    
    def test_custom_figsize(self):
        """Test plotting with custom figure size."""
        plot_macd(self.data, figsize=(10, 8), show=False)


class TestPlotRSI:
    """Tests for plot_rsi function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
        
        self.data = calculate_rsi(data)
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        plt.close('all')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_plot_without_save(self):
        """Test plotting without saving."""
        plot_rsi(self.data, show=False)
    
    def test_plot_with_save(self):
        """Test plotting with saving to file."""
        save_path = os.path.join(self.test_dir, 'rsi.png')
        plot_rsi(self.data, save_path=save_path, show=False)
        
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 0
    
    def test_missing_columns(self):
        """Test that missing columns raise ValueError."""
        bad_data = self.data.drop('RSI', axis=1)
        
        with pytest.raises(ValueError, match="Missing required columns"):
            plot_rsi(bad_data, show=False)
    
    def test_custom_figsize(self):
        """Test plotting with custom figure size."""
        plot_rsi(self.data, figsize=(10, 8), show=False)


class TestPlotAllIndicators:
    """Tests for plot_all_indicators function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
        data = pd.DataFrame({
            'Open': np.random.uniform(20000, 60000, len(dates)),
            'High': np.random.uniform(20000, 60000, len(dates)),
            'Low': np.random.uniform(20000, 60000, len(dates)),
            'Close': np.random.uniform(20000, 60000, len(dates)),
            'Volume': np.random.uniform(1e9, 5e9, len(dates)),
        }, index=dates)
        
        # Add all indicators and power law
        from btc_indicators.indicators import add_all_indicators
        tmp = add_all_indicators(data)
        self.data = calculate_power_law(tmp)
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        plt.close('all')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_plot_all_without_save(self):
        """Test plotting all indicators without saving."""
        plot_all_indicators(self.data, show=False)
    
    def test_plot_all_with_save_dir(self):
        """Test plotting all indicators with save directory."""
        plot_all_indicators(self.data, save_dir=self.test_dir, show=False)
        
        # Check that all plots were saved
        assert os.path.exists(os.path.join(self.test_dir, 'mayer_multiple.png'))
        assert os.path.exists(os.path.join(self.test_dir, 'macd.png'))
        assert os.path.exists(os.path.join(self.test_dir, 'rsi.png'))
        assert os.path.exists(os.path.join(self.test_dir, 'power_law.png'))
    
    def test_plot_all_partial_indicators(self):
        """Test plotting when only some indicators are available."""
        # Data with only MACD
        partial_data = calculate_macd(self.data[['Open', 'High', 'Low', 'Close', 'Volume']])
        
        # Should not raise, just skip unavailable plots
        plot_all_indicators(partial_data, show=False)


class TestPlotPowerLaw:
    """Tests for plot_power_law function."""

    def setup_method(self):
        dates = pd.date_range('2011-01-01', periods=400, freq='D')
        data = pd.DataFrame({
            'Open': np.linspace(1, 100, len(dates)),
            'High': np.linspace(1, 100, len(dates)) + 0.5,
            'Low': np.linspace(1, 100, len(dates)) - 0.5,
            'Close': np.linspace(1, 100, len(dates)),
            'Volume': np.linspace(1e6, 2e6, len(dates)),
        }, index=dates)
        self.data = calculate_power_law(data)
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        plt.close('all')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_plot_without_save(self):
        plot_power_law(self.data, show=False)

    def test_plot_with_save(self):
        save_path = os.path.join(self.test_dir, 'power_law.png')
        plot_power_law(self.data, save_path=save_path, show=False)
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 0

    def test_plot_with_future(self):
        save_path = os.path.join(self.test_dir, 'power_law_future.png')
        plot_power_law(self.data, save_path=save_path, show=False, show_future=True, years_ahead=1)
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 0

