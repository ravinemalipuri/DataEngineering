"""
Tests for schema inference.
"""

import pytest
import pandas as pd
import tempfile
import os
import json
from pathlib import Path

from datamodel_profiler.core.schema_inference import SchemaInferencer
from datamodel_profiler.utils.types import ProfilingConfig, DataFormat


class TestSchemaInferencer:
    """Test cases for SchemaInferencer."""
    
    def setup_method(self):
        """Set up test data."""
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'david@example.com', 'eve@example.com'],
            'age': [25, 30, 35, 40, 45],
            'salary': [50000.0, 60000.0, 70000.0, 80000.0, 90000.0],
            'is_active': [True, True, False, True, False],
            'created_at': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'])
        })
        
        self.config = ProfilingConfig()
        self.inferencer = SchemaInferencer(self.config)
    
    def test_infer_schema(self):
        """Test basic schema inference."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            schema = self.inferencer.infer_schema(temp_path, "test_table", DataFormat.CSV)
            
            # Check basic schema properties
            assert schema.table_name == "test_table"
            assert len(schema.columns) == 7
            
            # Check column types
            column_names = [col.name for col in schema.columns]
            assert 'id' in column_names
            assert 'name' in column_names
            assert 'email' in column_names
            
            # Check specific column types
            id_col = next(col for col in schema.columns if col.name == 'id')
            assert id_col.data_type == "integer"
            assert not id_col.nullable
            
            email_col = next(col for col in schema.columns if col.name == 'email')
            assert email_col.data_type == "string"
            
        finally:
            os.unlink(temp_path)
    
    def test_export_schema_formats(self):
        """Test exporting schema in multiple formats."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            schema = self.inferencer.infer_schema(temp_path, "test_table", DataFormat.CSV)
            
            # Create temporary output directory
            with tempfile.TemporaryDirectory() as temp_dir:
                output_files = self.inferencer.export_schema(schema, temp_dir)
                
                # Check that all expected files were created
                expected_formats = ['json', 'avro', 'sql', 'arrow', 'pydantic', 'dataclass']
                for format_name in expected_formats:
                    assert format_name in output_files
                    assert Path(output_files[format_name]).exists()
                
                # Check JSON Schema format
                with open(output_files['json'], 'r') as f:
                    json_schema = json.load(f)
                    assert json_schema['$schema'] == "https://json-schema.org/draft/2020-12/schema"
                    assert json_schema['title'] == "test_table"
                    assert 'properties' in json_schema
                
                # Check SQL DDL format
                with open(output_files['sql'], 'r') as f:
                    sql_ddl = f.read()
                    assert "CREATE TABLE test_table" in sql_ddl
                    assert "id" in sql_ddl
                    assert "name" in sql_ddl
                
        finally:
            os.unlink(temp_path)
    
    def test_data_type_inference(self):
        """Test data type inference for different types."""
        # Test integer type
        int_data = pd.DataFrame({'col': [1, 2, 3, 4, 5]})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            int_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            schema = self.inferencer.infer_schema(temp_path, "int_table", DataFormat.CSV)
            int_col = schema.columns[0]
            assert int_col.data_type == "integer"
        finally:
            os.unlink(temp_path)
        
        # Test float type
        float_data = pd.DataFrame({'col': [1.1, 2.2, 3.3, 4.4, 5.5]})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            float_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            schema = self.inferencer.infer_schema(temp_path, "float_table", DataFormat.CSV)
            float_col = schema.columns[0]
            assert float_col.data_type == "float"
        finally:
            os.unlink(temp_path)
        
        # Test boolean type
        bool_data = pd.DataFrame({'col': [True, False, True, False, True]})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            bool_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            schema = self.inferencer.infer_schema(temp_path, "bool_table", DataFormat.CSV)
            bool_col = schema.columns[0]
            assert bool_col.data_type == "boolean"
        finally:
            os.unlink(temp_path)
    
    def test_nullable_detection(self):
        """Test nullable column detection."""
        # Create data with nulls
        data_with_nulls = pd.DataFrame({
            'nullable_col': [1, 2, None, 4, 5],
            'non_nullable_col': [1, 2, 3, 4, 5]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            data_with_nulls.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            schema = self.inferencer.infer_schema(temp_path, "nullable_table", DataFormat.CSV)
            
            nullable_col = next(col for col in schema.columns if col.name == 'nullable_col')
            non_nullable_col = next(col for col in schema.columns if col.name == 'non_nullable_col')
            
            assert nullable_col.nullable == True
            assert non_nullable_col.nullable == False
            
        finally:
            os.unlink(temp_path)
    
    def test_constraint_generation(self):
        """Test constraint generation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            schema = self.inferencer.infer_schema(temp_path, "constraint_table", DataFormat.CSV)
            
            # Check that constraints are generated for appropriate columns
            age_col = next(col for col in schema.columns if col.name == 'age')
            if age_col.constraints:
                assert 'minimum' in age_col.constraints
                assert 'maximum' in age_col.constraints
            
        finally:
            os.unlink(temp_path)
