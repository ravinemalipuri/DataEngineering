"""
Primary key detection engine with scoring algorithms.
"""

import itertools
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path
import pandas as pd
import numpy as np

from ..io.data_loader import DataLoader, DataFormat
from ..utils.types import (
    DataType, SemanticType, ColumnStats, DatasetProfile, 
    ProfilingConfig, KeyCandidate
)


class KeyDetector:
    """Primary key detection engine."""
    
    def __init__(self, config: Optional[ProfilingConfig] = None):
        """
        Initialize key detector.
        
        Args:
            config: Profiling configuration
        """
        self.config = config or ProfilingConfig()
        self.data_loader = DataLoader(self.config.engine)
    
    def detect_keys(
        self,
        path: Union[str, Path],
        format_type: DataFormat = DataFormat.AUTO,
        max_composite_size: int = 3,
        **kwargs
    ) -> List[KeyCandidate]:
        """
        Detect primary key candidates.
        
        Args:
            path: File or directory path
            format_type: Data format
            max_composite_size: Maximum number of columns in composite keys
            **kwargs: Additional options
            
        Returns:
            List of key candidates with scores
        """
        # Load data
        data_chunks = self.data_loader.load_data(path, format_type, **kwargs)
        first_chunk = next(data_chunks)
        
        # Get column statistics
        column_stats = self._analyze_columns(first_chunk)
        
        # Detect single column keys
        single_keys = self._detect_single_keys(column_stats)
        
        # Detect composite keys
        composite_keys = self._detect_composite_keys(
            first_chunk, column_stats, max_composite_size
        )
        
        # Combine and rank all candidates
        all_candidates = single_keys + composite_keys
        all_candidates.sort(key=lambda x: x.overall_score, reverse=True)
        
        return all_candidates[:10]  # Return top 10 candidates
    
    def _analyze_columns(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Analyze columns for key characteristics."""
        column_stats = {}
        
        for col_name in df.columns:
            col_data = df[col_name]
            
            # Basic statistics
            null_count = col_data.isnull().sum()
            total_count = len(col_data)
            null_percentage = (null_count / total_count) * 100
            
            # Uniqueness analysis
            unique_count = col_data.nunique()
            uniqueness_percentage = (unique_count / total_count) * 100
            
            # Data type analysis
            data_type = self._infer_data_type(col_data)
            
            # Stability analysis (how consistent the data type is)
            stability_score = self._calculate_stability_score(col_data, data_type)
            
            # Name-based heuristics
            name_score = self._calculate_name_score(col_name)
            
            column_stats[col_name] = {
                'null_count': null_count,
                'null_percentage': null_percentage,
                'unique_count': unique_count,
                'uniqueness_percentage': uniqueness_percentage,
                'data_type': data_type,
                'stability_score': stability_score,
                'name_score': name_score,
                'total_count': total_count
            }
        
        return column_stats
    
    def _infer_data_type(self, col_data: pd.Series) -> str:
        """Infer data type from column data."""
        if pd.api.types.is_integer_dtype(col_data):
            return "integer"
        elif pd.api.types.is_float_dtype(col_data):
            return "float"
        elif pd.api.types.is_bool_dtype(col_data):
            return "boolean"
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            return "datetime"
        elif pd.api.types.is_string_dtype(col_data):
            return "string"
        else:
            return "string"
    
    def _calculate_stability_score(self, col_data: pd.Series, data_type: str) -> float:
        """Calculate stability score for a column."""
        non_null_data = col_data.dropna()
        
        if len(non_null_data) == 0:
            return 0.0
        
        # Type consistency score
        if data_type == "integer":
            # Check if all values are actually integers
            try:
                pd.to_numeric(non_null_data, errors='raise')
                return 1.0
            except (ValueError, TypeError):
                return 0.5
        elif data_type == "string":
            # Check for consistent string patterns
            sample_values = non_null_data.head(100)
            if len(sample_values) > 0:
                # Check if all values have similar length
                lengths = sample_values.astype(str).str.len()
                length_std = lengths.std()
                if length_std == 0:
                    return 1.0
                elif length_std < lengths.mean() * 0.1:
                    return 0.8
                else:
                    return 0.6
            return 0.5
        else:
            return 0.7
    
    def _calculate_name_score(self, col_name: str) -> float:
        """Calculate score based on column name patterns."""
        col_name_lower = col_name.lower()
        
        # High score for common ID patterns
        if any(pattern in col_name_lower for pattern in ['id', 'key', 'pk']):
            return 1.0
        
        # Medium score for other identifier patterns
        if any(pattern in col_name_lower for pattern in ['code', 'num', 'no', 'ref']):
            return 0.7
        
        # Low score for descriptive names
        if any(pattern in col_name_lower for pattern in ['name', 'desc', 'title', 'label']):
            return 0.3
        
        return 0.5
    
    def _detect_single_keys(self, column_stats: Dict[str, Dict[str, Any]]) -> List[KeyCandidate]:
        """Detect single column primary key candidates."""
        candidates = []
        
        for col_name, stats in column_stats.items():
            # Calculate individual scores
            uniqueness_score = min(stats['uniqueness_percentage'] / 100, 1.0)
            nullability_score = 1 - (stats['null_percentage'] / 100)
            stability_score = stats['stability_score']
            name_score = stats['name_score']
            
            # Weighted overall score
            overall_score = (
                uniqueness_score * 0.4 +
                nullability_score * 0.3 +
                stability_score * 0.2 +
                name_score * 0.1
            )
            
            # Only consider candidates with reasonable scores
            if overall_score > 0.5:
                rationale = self._generate_rationale(
                    col_name, stats, uniqueness_score, nullability_score, 
                    stability_score, name_score
                )
                
                candidate = KeyCandidate(
                    columns=[col_name],
                    uniqueness_score=uniqueness_score,
                    nullability_score=nullability_score,
                    stability_score=stability_score,
                    overall_score=overall_score,
                    rationale=rationale,
                    is_composite=False
                )
                candidates.append(candidate)
        
        return candidates
    
    def _detect_composite_keys(
        self,
        df: pd.DataFrame,
        column_stats: Dict[str, Dict[str, Any]],
        max_size: int
    ) -> List[KeyCandidate]:
        """Detect composite primary key candidates."""
        candidates = []
        
        # Get candidate columns (those with decent individual scores)
        candidate_columns = [
            col for col, stats in column_stats.items()
            if stats['uniqueness_percentage'] > 50 and stats['null_percentage'] < 50
        ]
        
        # Generate combinations
        for size in range(2, min(max_size + 1, len(candidate_columns) + 1)):
            for combo in itertools.combinations(candidate_columns, size):
                candidate = self._evaluate_composite_key(df, combo, column_stats)
                if candidate and candidate.overall_score > 0.6:
                    candidates.append(candidate)
        
        return candidates
    
    def _evaluate_composite_key(
        self,
        df: pd.DataFrame,
        columns: Tuple[str, ...],
        column_stats: Dict[str, Dict[str, Any]]
    ) -> Optional[KeyCandidate]:
        """Evaluate a composite key candidate."""
        # Check if combination is unique
        combination_data = df[list(columns)]
        unique_combinations = combination_data.drop_duplicates()
        uniqueness_score = len(unique_combinations) / len(combination_data)
        
        if uniqueness_score < 0.95:  # Not unique enough
            return None
        
        # Calculate nullability score (all columns should have low nulls)
        null_scores = [1 - (column_stats[col]['null_percentage'] / 100) for col in columns]
        nullability_score = min(null_scores)
        
        # Calculate stability score (average of individual stability scores)
        stability_scores = [column_stats[col]['stability_score'] for col in columns]
        stability_score = sum(stability_scores) / len(stability_scores)
        
        # Calculate name score (average of individual name scores)
        name_scores = [column_stats[col]['name_score'] for col in columns]
        name_score = sum(name_scores) / len(name_scores)
        
        # Weighted overall score
        overall_score = (
            uniqueness_score * 0.4 +
            nullability_score * 0.3 +
            stability_score * 0.2 +
            name_score * 0.1
        )
        
        rationale = self._generate_composite_rationale(
            columns, column_stats, uniqueness_score, nullability_score,
            stability_score, name_score
        )
        
        return KeyCandidate(
            columns=list(columns),
            uniqueness_score=uniqueness_score,
            nullability_score=nullability_score,
            stability_score=stability_score,
            overall_score=overall_score,
            rationale=rationale,
            is_composite=True
        )
    
    def _generate_rationale(
        self,
        col_name: str,
        stats: Dict[str, Any],
        uniqueness_score: float,
        nullability_score: float,
        stability_score: float,
        name_score: float
    ) -> str:
        """Generate rationale for single column key candidate."""
        rationale_parts = []
        
        # Uniqueness
        if uniqueness_score > 0.9:
            rationale_parts.append("highly unique")
        elif uniqueness_score > 0.7:
            rationale_parts.append("mostly unique")
        else:
            rationale_parts.append("moderately unique")
        
        # Nullability
        if nullability_score > 0.9:
            rationale_parts.append("no null values")
        elif nullability_score > 0.7:
            rationale_parts.append("few null values")
        else:
            rationale_parts.append("some null values")
        
        # Stability
        if stability_score > 0.8:
            rationale_parts.append("stable data type")
        else:
            rationale_parts.append("variable data type")
        
        # Name
        if name_score > 0.8:
            rationale_parts.append("ID-like name")
        
        return f"Column '{col_name}' is {', '.join(rationale_parts)}. " \
               f"Uniqueness: {uniqueness_score:.2f}, Nullability: {nullability_score:.2f}, " \
               f"Stability: {stability_score:.2f}, Name: {name_score:.2f}"
    
    def _generate_composite_rationale(
        self,
        columns: Tuple[str, ...],
        column_stats: Dict[str, Dict[str, Any]],
        uniqueness_score: float,
        nullability_score: float,
        stability_score: float,
        name_score: float
    ) -> str:
        """Generate rationale for composite key candidate."""
        col_names = " + ".join(columns)
        
        rationale_parts = []
        
        # Uniqueness
        if uniqueness_score > 0.99:
            rationale_parts.append("completely unique")
        elif uniqueness_score > 0.95:
            rationale_parts.append("highly unique")
        else:
            rationale_parts.append("mostly unique")
        
        # Nullability
        null_percentages = [column_stats[col]['null_percentage'] for col in columns]
        max_null_pct = max(null_percentages)
        if max_null_pct < 1:
            rationale_parts.append("no null values")
        elif max_null_pct < 5:
            rationale_parts.append("minimal null values")
        else:
            rationale_parts.append("some null values")
        
        # Stability
        if stability_score > 0.8:
            rationale_parts.append("stable data types")
        else:
            rationale_parts.append("variable data types")
        
        return f"Composite key ({col_names}) is {', '.join(rationale_parts)}. " \
               f"Uniqueness: {uniqueness_score:.2f}, Nullability: {nullability_score:.2f}, " \
               f"Stability: {stability_score:.2f}, Name: {name_score:.2f}"
    
    def export_key_candidates(
        self,
        candidates: List[KeyCandidate],
        output_path: Union[str, Path]
    ) -> Path:
        """
        Export key candidates to JSON file.
        
        Args:
            candidates: List of key candidates
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        output_path = Path(output_path)
        
        # Convert to serializable format
        export_data = {
            "key_candidates": [
                {
                    "columns": candidate.columns,
                    "uniqueness_score": candidate.uniqueness_score,
                    "nullability_score": candidate.nullability_score,
                    "stability_score": candidate.stability_score,
                    "overall_score": candidate.overall_score,
                    "rationale": candidate.rationale,
                    "is_composite": candidate.is_composite
                }
                for candidate in candidates
            ],
            "summary": {
                "total_candidates": len(candidates),
                "single_column_candidates": len([c for c in candidates if not c.is_composite]),
                "composite_candidates": len([c for c in candidates if c.is_composite]),
                "top_candidate": candidates[0].columns if candidates else None
            }
        }
        
        import json
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return output_path
