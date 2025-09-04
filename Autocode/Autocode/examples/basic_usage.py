#!/usr/bin/env python3
"""
Basic usage example for datamodel_profiler.
"""

import pandas as pd
import tempfile
import os
from pathlib import Path

from datamodel_profiler import DataProfiler, SchemaInferencer, KeyDetector, ConstraintSuggester
from datamodel_profiler.io import DataFormat
from datamodel_profiler.utils.types import ProfilingConfig


def create_sample_data():
    """Create sample data for demonstration."""
    data = pd.DataFrame({
        'user_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'username': ['alice', 'bob', 'charlie', 'david', 'eve', 'frank', 'grace', 'henry', 'ivy', 'jack'],
        'email': [
            'alice@example.com', 'bob@example.com', 'charlie@example.com',
            'david@example.com', 'eve@example.com', 'frank@example.com',
            'grace@example.com', 'henry@example.com', 'ivy@example.com', 'jack@example.com'
        ],
        'age': [25, 30, 35, 40, 45, 28, 32, 38, 42, 29],
        'salary': [50000, 60000, 70000, 80000, 90000, 55000, 65000, 75000, 85000, 58000],
        'department': ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Marketing', 'IT', 'Finance', 'HR'],
        'is_active': [True, True, False, True, True, True, False, True, True, False],
        'hire_date': pd.to_datetime([
            '2020-01-15', '2019-03-22', '2021-07-10', '2018-11-05',
            '2022-02-14', '2020-09-30', '2021-12-01', '2019-06-18',
            '2020-04-12', '2021-08-25'
        ])
    })
    return data


def main():
    """Main demonstration function."""
    print("DataModel Profiler - Basic Usage Example")
    print("=" * 50)
    
    # Create sample data
    print("\n1. Creating sample data...")
    sample_data = create_sample_data()
    print(f"   Created dataset with {len(sample_data)} rows and {len(sample_data.columns)} columns")
    
    # Save to temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        sample_data.to_csv(f.name, index=False)
        temp_file = f.name
    
    try:
        # Initialize profiler
        print("\n2. Initializing profiler...")
        config = ProfilingConfig(engine="pandas")
        profiler = DataProfiler(config)
        
        # Profile the data
        print("\n3. Profiling data...")
        profile = profiler.profile(temp_file, DataFormat.CSV)
        
        print(f"   Rows: {profile.row_count:,}")
        print(f"   Columns: {profile.column_count}")
        print(f"   Quality Score: {profile.quality_score:.2f}")
        print(f"   Profiling Time: {profile.profiling_time_seconds:.2f} seconds")
        
        # Show column statistics
        print("\n4. Column Statistics:")
        for name, col in profile.columns.items():
            print(f"   {name}:")
            print(f"     Type: {col.data_type.value} ({col.semantic_type.value})")
            print(f"     Nulls: {col.null_count} ({col.null_percentage:.1f}%)")
            print(f"     Distinct: {col.distinct_count} ({col.distinct_percentage:.1f}%)")
            if col.min_value is not None and col.max_value is not None:
                print(f"     Range: {col.min_value} to {col.max_value}")
            if col.mean_value is not None:
                print(f"     Mean: {col.mean_value:.2f} (std: {col.std_dev:.2f})")
        
        # Show primary key candidates
        print("\n5. Primary Key Candidates:")
        for i, candidate in enumerate(profile.primary_key_candidates[:3], 1):
            print(f"   {i}. {', '.join(candidate['column'])} (score: {candidate['overall_score']:.3f})")
            print(f"      {candidate['rationale']}")
        
        # Schema inference
        print("\n6. Inferring schema...")
        inferencer = SchemaInferencer(config)
        schema = inferencer.infer_schema(temp_file, "users", DataFormat.CSV)
        
        print(f"   Table: {schema.table_name}")
        print(f"   Columns: {len(schema.columns)}")
        
        # Show schema details
        print("\n7. Schema Details:")
        for col in schema.columns:
            nullable = "NULL" if col.nullable else "NOT NULL"
            print(f"   {col.name}: {col.data_type} {nullable}")
            if col.description:
                print(f"     {col.description}")
        
        # Key detection
        print("\n8. Detecting primary keys...")
        detector = KeyDetector(config)
        key_candidates = detector.detect_keys(temp_file, DataFormat.CSV)
        
        print(f"   Found {len(key_candidates)} key candidates")
        if key_candidates:
            top_candidate = key_candidates[0]
            print(f"   Top candidate: {', '.join(top_candidate.columns)}")
            print(f"   Score: {top_candidate.overall_score:.3f}")
            print(f"   Rationale: {top_candidate.rationale}")
        
        # Constraint suggestions
        print("\n9. Suggesting constraints...")
        suggester = ConstraintSuggester(config)
        constraints = suggester.suggest_constraints(temp_file, DataFormat.CSV)
        
        print(f"   Generated {len(constraints)} constraint suggestions")
        
        # Show some constraint examples
        print("\n10. Sample Constraints:")
        constraint_types = {}
        for constraint in constraints:
            constraint_type = constraint.constraint_type
            if constraint_type not in constraint_types:
                constraint_types[constraint_type] = []
            constraint_types[constraint_type].append(constraint)
        
        for constraint_type, examples in list(constraint_types.items())[:3]:
            print(f"   {constraint_type}:")
            for constraint in examples[:2]:  # Show first 2 examples
                print(f"     Column: {constraint.column_name}")
                print(f"     Confidence: {constraint.confidence:.1%}")
                print(f"     Rationale: {constraint.rationale}")
        
        print("\n" + "=" * 50)
        print("Example completed successfully!")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.unlink(temp_file)


if __name__ == "__main__":
    main()
