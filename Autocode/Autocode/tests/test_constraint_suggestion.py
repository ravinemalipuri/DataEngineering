"""
Tests for constraint suggestion.
"""

import pytest
import pandas as pd
import tempfile
import os
import json
from pathlib import Path

from datamodel_profiler.core.constraint_suggestion import ConstraintSuggester
from datamodel_profiler.utils.types import ProfilingConfig, DataFormat


class TestConstraintSuggester:
    """Test cases for ConstraintSuggester."""
    
    def setup_method(self):
        """Set up test data."""
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'david@example.com', 'eve@example.com'],
            'age': [25, 30, 35, 40, 45],
            'salary': [50000.0, 60000.0, 70000.0, 80000.0, 90000.0],
            'status': ['active', 'inactive', 'active', 'active', 'inactive'],
            'department': ['IT', 'HR', 'IT', 'Finance', 'HR']
        })
        
        self.config = ProfilingConfig()
        self.suggester = ConstraintSuggester(self.config)
    
    def test_suggest_constraints(self):
        """Test basic constraint suggestion."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            suggestions = self.suggester.suggest_constraints(temp_path, DataFormat.CSV)
            
            # Should generate some constraints
            assert len(suggestions) > 0
            
            # Check constraint types
            constraint_types = [s.constraint_type for s in suggestions]
            assert 'expect_column_values_to_be_of_type' in constraint_types
            
        finally:
            os.unlink(temp_path)
    
    def test_type_constraints(self):
        """Test type constraint suggestions."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            suggestions = self.suggester.suggest_constraints(temp_path, DataFormat.CSV)
            
            # Find type constraints
            type_constraints = [s for s in suggestions if s.constraint_type == 'expect_column_values_to_be_of_type']
            assert len(type_constraints) > 0
            
            # Check that type constraints have appropriate parameters
            for constraint in type_constraints:
                assert 'column' in constraint.parameters
                assert 'type_' in constraint.parameters
                assert constraint.confidence > 0
            
        finally:
            os.unlink(temp_path)
    
    def test_range_constraints(self):
        """Test range constraint suggestions."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            suggestions = self.suggester.suggest_constraints(temp_path, DataFormat.CSV)
            
            # Find range constraints
            range_constraints = [s for s in suggestions if s.constraint_type == 'expect_column_values_to_be_between']
            assert len(range_constraints) > 0
            
            # Check that range constraints have min/max values
            for constraint in range_constraints:
                assert 'min_value' in constraint.parameters
                assert 'max_value' in constraint.parameters
                assert constraint.parameters['min_value'] < constraint.parameters['max_value']
            
        finally:
            os.unlink(temp_path)
    
    def test_allowed_values_constraints(self):
        """Test allowed values constraint suggestions."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            suggestions = self.suggester.suggest_constraints(temp_path, DataFormat.CSV)
            
            # Find allowed values constraints
            allowed_constraints = [s for s in suggestions if s.constraint_type == 'expect_column_values_to_be_in_set']
            assert len(allowed_constraints) > 0
            
            # Check that allowed values constraints have value sets
            for constraint in allowed_constraints:
                assert 'value_set' in constraint.parameters
                assert isinstance(constraint.parameters['value_set'], list)
                assert len(constraint.parameters['value_set']) > 0
            
        finally:
            os.unlink(temp_path)
    
    def test_pattern_constraints(self):
        """Test pattern constraint suggestions."""
        # Create data with email addresses
        email_data = pd.DataFrame({
            'email': ['test@example.com', 'user@domain.org', 'admin@site.net']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            email_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            suggestions = self.suggester.suggest_constraints(temp_path, DataFormat.CSV)
            
            # Find pattern constraints
            pattern_constraints = [s for s in suggestions if s.constraint_type == 'expect_column_values_to_match_regex']
            assert len(pattern_constraints) > 0
            
            # Check that pattern constraints have regex patterns
            for constraint in pattern_constraints:
                assert 'regex' in constraint.parameters
                assert isinstance(constraint.parameters['regex'], str)
                assert len(constraint.parameters['regex']) > 0
            
        finally:
            os.unlink(temp_path)
    
    def test_foreign_key_constraints(self):
        """Test foreign key constraint suggestions."""
        # Create main data
        main_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'department_id': [1, 2, 1, 3, 2]
        })
        
        # Create lookup data
        lookup_data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['IT', 'HR', 'Finance']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            main_data.to_csv(f.name, index=False)
            main_path = f.name
        
        with tempfile.TemporaryDirectory() as temp_dir:
            lookup_path = Path(temp_dir) / "departments.csv"
            lookup_data.to_csv(lookup_path, index=False)
            
            try:
                suggestions = self.suggester.suggest_constraints(main_path, DataFormat.CSV, lookup_dir=temp_dir)
                
                # Should find foreign key constraints
                fk_constraints = [s for s in suggestions if 'foreign key' in s.rationale.lower()]
                assert len(fk_constraints) > 0
                
            finally:
                os.unlink(main_path)
    
    def test_export_constraints(self):
        """Test exporting constraints."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            suggestions = self.suggester.suggest_constraints(temp_path, DataFormat.CSV)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                output_path = f.name
            
            try:
                exported_path = self.suggester.export_constraints(suggestions, output_path)
                
                # Check that file was created
                assert os.path.exists(exported_path)
                
                # Check file contents
                with open(exported_path, 'r') as f:
                    data = json.load(f)
                    assert 'expectations' in data
                    assert 'summary' in data
                    assert len(data['expectations']) == len(suggestions)
                    
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)
            
        finally:
            os.unlink(temp_path)
    
    def test_markdown_report(self):
        """Test markdown report generation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            suggestions = self.suggester.suggest_constraints(temp_path, DataFormat.CSV)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                output_path = f.name
            
            try:
                exported_path = self.suggester.generate_markdown_report(suggestions, output_path)
                
                # Check that file was created
                assert os.path.exists(exported_path)
                
                # Check file contents
                with open(exported_path, 'r') as f:
                    content = f.read()
                    assert '# Data Quality Constraints Report' in content
                    assert 'Total Constraints' in content
                    
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)
            
        finally:
            os.unlink(temp_path)
