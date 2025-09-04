"""
Tests for key detection.
"""

import pytest
import pandas as pd
import tempfile
import os
import json

from datamodel_profiler.core.key_detection import KeyDetector
from datamodel_profiler.utils.types import ProfilingConfig, DataFormat


class TestKeyDetector:
    """Test cases for KeyDetector."""
    
    def setup_method(self):
        """Set up test data."""
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'david@example.com', 'eve@example.com'],
            'department': ['IT', 'HR', 'IT', 'Finance', 'HR'],
            'employee_code': ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005']
        })
        
        self.config = ProfilingConfig()
        self.detector = KeyDetector(self.config)
    
    def test_detect_single_keys(self):
        """Test single column key detection."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            candidates = self.detector.detect_keys(temp_path, DataFormat.CSV)
            
            # Should find key candidates
            assert len(candidates) > 0
            
            # 'id' should be a top candidate
            id_candidate = next((c for c in candidates if 'id' in c.columns), None)
            assert id_candidate is not None
            assert id_candidate.overall_score > 0.7
            assert not id_candidate.is_composite
            
        finally:
            os.unlink(temp_path)
    
    def test_detect_composite_keys(self):
        """Test composite key detection."""
        # Create data where combination of columns is unique
        composite_data = pd.DataFrame({
            'department': ['IT', 'IT', 'HR', 'HR', 'Finance'],
            'employee_code': ['EMP001', 'EMP002', 'EMP001', 'EMP002', 'EMP001'],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            composite_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            candidates = self.detector.detect_keys(temp_path, DataFormat.CSV, max_composite_size=2)
            
            # Should find composite key candidates
            composite_candidates = [c for c in candidates if c.is_composite]
            assert len(composite_candidates) > 0
            
            # Check that composite keys have multiple columns
            for candidate in composite_candidates:
                assert len(candidate.columns) > 1
                assert candidate.is_composite == True
            
        finally:
            os.unlink(temp_path)
    
    def test_key_scoring(self):
        """Test key scoring algorithm."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            candidates = self.detector.detect_keys(temp_path, DataFormat.CSV)
            
            # Check that candidates are sorted by score
            scores = [c.overall_score for c in candidates]
            assert scores == sorted(scores, reverse=True)
            
            # Check score components
            for candidate in candidates:
                assert 0 <= candidate.uniqueness_score <= 1
                assert 0 <= candidate.nullability_score <= 1
                assert 0 <= candidate.stability_score <= 1
                assert 0 <= candidate.overall_score <= 1
                
        finally:
            os.unlink(temp_path)
    
    def test_export_key_candidates(self):
        """Test exporting key candidates."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            candidates = self.detector.detect_keys(temp_path, DataFormat.CSV)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                output_path = f.name
            
            try:
                exported_path = self.detector.export_key_candidates(candidates, output_path)
                
                # Check that file was created
                assert os.path.exists(exported_path)
                
                # Check file contents
                with open(exported_path, 'r') as f:
                    data = json.load(f)
                    assert 'key_candidates' in data
                    assert 'summary' in data
                    assert len(data['key_candidates']) == len(candidates)
                    
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)
            
        finally:
            os.unlink(temp_path)
    
    def test_name_based_scoring(self):
        """Test name-based scoring heuristics."""
        # Create data with ID-like column names
        id_data = pd.DataFrame({
            'user_id': [1, 2, 3, 4, 5],
            'product_key': ['PK001', 'PK002', 'PK003', 'PK004', 'PK005'],
            'customer_name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            id_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            candidates = self.detector.detect_keys(temp_path, DataFormat.CSV)
            
            # ID-like columns should have higher name scores
            user_id_candidate = next((c for c in candidates if 'user_id' in c.columns), None)
            name_candidate = next((c for c in candidates if 'customer_name' in c.columns), None)
            
            if user_id_candidate and name_candidate:
                # This is a bit indirect since we don't expose name_score directly
                # but we can check that ID-like columns rank higher
                user_id_rank = candidates.index(user_id_candidate)
                name_rank = candidates.index(name_candidate)
                assert user_id_rank < name_rank  # Lower rank = higher score
            
        finally:
            os.unlink(temp_path)
