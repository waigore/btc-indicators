"""
Unit tests for btc_indicators.data module.
"""

import pytest
import pandas as pd
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from btc_indicators.data import fetch_btc_data, load_data_from_csv


class TestFetchBTCData:
    """Tests for fetch_btc_data function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_fetch_default_dates(self):
        """Test fetching with default date range (last month)."""
        data = fetch_btc_data(data_dir=self.test_dir)
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert 'Close' in data.columns
        assert 'Open' in data.columns
        assert 'High' in data.columns
        assert 'Low' in data.columns
        assert 'Volume' in data.columns
    
    def test_fetch_custom_date_range(self):
        """Test fetching with custom date range."""
        start = "2023-01-01"
        end = "2023-12-31"
        
        data = fetch_btc_data(
            start_date=start,
            end_date=end,
            data_dir=self.test_dir
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert data.index.min().year == 2023
        assert data.index.max().year == 2023
    
    def test_csv_persistence(self):
        """Test that data is saved as year-based CSV files."""
        start = "2023-01-01"
        end = "2023-12-31"
        
        fetch_btc_data(
            start_date=start,
            end_date=end,
            data_dir=self.test_dir
        )
        
        # Check that 2023.csv was created
        csv_path = os.path.join(self.test_dir, "2023.csv")
        assert os.path.exists(csv_path)
        
        # Check that we can load the CSV
        df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        assert not df.empty
        assert 'Close' in df.columns
    
    def test_multiple_years_csv(self):
        """Test that data spanning multiple years creates multiple CSV files."""
        start = "2022-06-01"
        end = "2023-06-30"
        
        fetch_btc_data(
            start_date=start,
            end_date=end,
            data_dir=self.test_dir
        )
        
        # Check that both year files were created
        assert os.path.exists(os.path.join(self.test_dir, "2022.csv"))
        assert os.path.exists(os.path.join(self.test_dir, "2023.csv"))
    
    def test_data_patching(self):
        """Test that existing CSV data is patched rather than replaced."""
        # First fetch
        start1 = "2023-01-01"
        end1 = "2023-06-30"
        data1 = fetch_btc_data(
            start_date=start1,
            end_date=end1,
            data_dir=self.test_dir
        )
        
        csv_path = os.path.join(self.test_dir, "2023.csv")
        df1 = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        records1 = len(df1)
        
        # Second fetch with overlapping range
        start2 = "2023-06-01"
        end2 = "2023-12-31"
        data2 = fetch_btc_data(
            start_date=start2,
            end_date=end2,
            data_dir=self.test_dir
        )
        
        # Check that CSV was updated, not replaced
        df2 = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        records2 = len(df2)
        
        # Should have more records after patching
        assert records2 > records1
        
        # Should not have duplicates
        assert not df2.index.duplicated().any()
    
    def test_interval_parameter(self):
        """Test that interval parameter is respected."""
        start = "2024-01-01"
        end = "2024-01-31"
        
        # Should work with daily interval
        data = fetch_btc_data(
            start_date=start,
            end_date=end,
            interval="1d",
            data_dir=self.test_dir
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty


class TestLoadDataFromCSV:
    """Tests for load_data_from_csv function."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create sample CSV files
        dates_2022 = pd.date_range('2022-01-01', '2022-12-31', freq='D')
        dates_2023 = pd.date_range('2023-01-01', '2023-12-31', freq='D')
        
        df_2022 = pd.DataFrame({
            'Open': range(len(dates_2022)),
            'High': range(len(dates_2022)),
            'Low': range(len(dates_2022)),
            'Close': range(len(dates_2022)),
            'Volume': range(len(dates_2022)),
        }, index=dates_2022)
        
        df_2023 = pd.DataFrame({
            'Open': range(len(dates_2023)),
            'High': range(len(dates_2023)),
            'Low': range(len(dates_2023)),
            'Close': range(len(dates_2023)),
            'Volume': range(len(dates_2023)),
        }, index=dates_2023)
        
        df_2022.to_csv(os.path.join(self.test_dir, '2022.csv'))
        df_2023.to_csv(os.path.join(self.test_dir, '2023.csv'))
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_load_single_year(self):
        """Test loading data for a single year."""
        data = load_data_from_csv(
            start_date="2022-01-01",
            end_date="2022-12-31",
            data_dir=self.test_dir
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert data.index.min().year == 2022
        assert data.index.max().year == 2022
    
    def test_load_multiple_years(self):
        """Test loading data spanning multiple years."""
        data = load_data_from_csv(
            start_date="2022-06-01",
            end_date="2023-06-30",
            data_dir=self.test_dir
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert data.index.min().year == 2022
        assert data.index.max().year == 2023
    
    def test_load_default_dates(self):
        """Test loading with default dates (last month)."""
        data = load_data_from_csv(data_dir=self.test_dir)
        
        # Should return data, possibly empty if no recent data exists
        assert isinstance(data, pd.DataFrame)
    
    def test_load_nonexistent_year(self):
        """Test loading data for year without CSV file."""
        data = load_data_from_csv(
            start_date="2020-01-01",
            end_date="2020-12-31",
            data_dir=self.test_dir
        )
        
        # Should return empty DataFrame
        assert isinstance(data, pd.DataFrame)
        assert data.empty
    
    def test_no_duplicates(self):
        """Test that loaded data has no duplicate indices."""
        data = load_data_from_csv(
            start_date="2022-01-01",
            end_date="2023-12-31",
            data_dir=self.test_dir
        )
        
        assert not data.index.duplicated().any()

