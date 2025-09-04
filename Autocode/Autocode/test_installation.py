#!/usr/bin/env python3
"""
Test script to verify datamodel_profiler installation and basic functionality.
"""

import sys
import pandas as pd
import tempfile
import os

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from datamodel_profiler import DataProfiler, SchemaInferencer, KeyDetector, ConstraintSuggester
        from datamodel_profiler.io import DataFormat, DataLoader
        from datamodel_profiler.utils.types import ProfilingConfig
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality with sample data."""
    print("\nTesting basic functionality...")
    
    try:
        from datamodel_profiler import DataProfiler
        from datamodel_profiler.io import DataFormat
        from datamodel_profiler.utils.types import ProfilingConfig
        
        # Create sample data
        sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'david@example.com', 'eve@example.com'],
            'age': [25, 30, 35, 40, 45]
        })
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            # Test profiling
            config = ProfilingConfig()
            profiler = DataProfiler(config)
            profile = profiler.profile(temp_file, DataFormat.CSV)
            
            # Verify results
            assert profile.row_count == 5
            assert profile.column_count == 4
            assert profile.quality_score > 0
            assert len(profile.columns) == 4
            
            print("✓ Data profiling works")
            
            # Test schema inference
            from datamodel_profiler import SchemaInferencer
            inferencer = SchemaInferencer(config)
            schema = inferencer.infer_schema(temp_file, "test_table", DataFormat.CSV)
            
            assert schema.table_name == "test_table"
            assert len(schema.columns) == 4
            
            print("✓ Schema inference works")
            
            # Test key detection
            from datamodel_profiler import KeyDetector
            detector = KeyDetector(config)
            candidates = detector.detect_keys(temp_file, DataFormat.CSV)
            
            assert len(candidates) > 0
            
            print("✓ Key detection works")
            
            # Test constraint suggestions
            from datamodel_profiler import ConstraintSuggester
            suggester = ConstraintSuggester(config)
            constraints = suggester.suggest_constraints(temp_file, DataFormat.CSV)
            
            assert len(constraints) > 0
            
            print("✓ Constraint suggestions work")
            
            return True
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_cli():
    """Test CLI functionality."""
    print("\nTesting CLI...")
    
    try:
        from datamodel_profiler.cli import main
        print("✓ CLI module imports successfully")
        return True
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("DataModel Profiler - Installation Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_cli
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DataModel Profiler is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
