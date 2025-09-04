"""
Tests for the data profiler.
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path

from datamodel_profiler.core.profiler import DataProfiler
from datamodel_profiler.utils.types import ProfilingConfig, DataFormat


class TestDataProfiler:
    """Test cases for DataProfiler."""
    
    def setup_method(self):
        """Set up test data."""
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'david@example.com', 'eve@example.com'],
            'age': [25, 30, 35, 40, 45],
            'salary': [50000.0, 60000.0, 70000.0, 80000.0, 90000.0],
            'is_active': [True, True, False, True, False]
        })
        
        self.config = ProfilingConfig()
        self.profiler = DataProfiler(self.config)
    
    def test_profile_dataframe(self):
        """Test profiling a DataFrame."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            # Profile the data
            result = self.profiler.profile(temp_path, DataFormat.CSV)
            
            # Check basic statistics
            assert result.row_count == 5
            assert result.column_count == 6
            assert result.quality_score > 0
            
            # Check column statistics
            assert 'id' in result.columns
            assert 'name' in result.columns
            assert 'email' in result.columns
            
            # Check ID column (should be unique)
            id_col = result.columns['id']
            assert id_col.distinct_count == 5
            assert id_col.distinct_percentage == 100.0
            
            # Check email column (should detect semantic type)
            email_col = result.columns['email']
            assert email_col.semantic_type.value == 'email'
            
        finally:
            os.unlink(temp_path)
    
    def test_profile_with_nulls(self):
        """Test profiling data with null values."""
        # Create data with nulls
        data_with_nulls = self.test_data.copy()
        data_with_nulls.loc[0, 'age'] = None
        data_with_nulls.loc[1, 'name'] = None
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            data_with_nulls.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            result = self.profiler.profile(temp_path, DataFormat.CSV)
            
            # Check null statistics
            age_col = result.columns['age']
            assert age_col.null_count == 1
            assert age_col.null_percentage == 20.0
            
            name_col = result.columns['name']
            assert name_col.null_count == 1
            assert name_col.null_percentage == 20.0
            
        finally:
            os.unlink(temp_path)
    
    def test_primary_key_detection(self):
        """Test primary key detection."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            result = self.profiler.profile(temp_path, DataFormat.CSV)
            
            # Should detect 'id' as a primary key candidate
            assert len(result.primary_key_candidates) > 0
            
            # Check if 'id' is the top candidate
            top_candidate = result.primary_key_candidates[0]
            assert 'id' in top_candidate['column']
            assert top_candidate['overall_score'] > 0.8
            
        finally:
            os.unlink(temp_path)
    
    def test_semantic_type_detection(self):
        """Test semantic type detection."""
        # Test email detection
        email_data = pd.DataFrame({
            'email': ['test@example.com', 'user@domain.org', 'admin@site.net']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            email_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            result = self.profiler.profile(temp_path, DataFormat.CSV)
            email_col = result.columns['email']
            assert email_col.semantic_type.value == 'email'
            
        finally:
            os.unlink(temp_path)
    
    def test_outlier_detection(self):
        """Test outlier detection."""
        # Create data with outliers
        outlier_data = pd.DataFrame({
            'values': [1, 2, 3, 4, 5, 100]  # 100 is an outlier
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            outlier_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            result = self.profiler.profile(temp_path, DataFormat.CSV)
            values_col = result.columns['values']
            assert values_col.is_outlier_prone == True
            
        finally:
            os.unlink(temp_path)
