"""
Main data profiling engine.
"""

import time
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Union, Iterator
from pathlib import Path
from collections import defaultdict

from ..io.data_loader import DataLoader, DataFormat
from ..utils.types import (
    DataType, SemanticType, ColumnStats, DatasetProfile, ProfilingConfig
)
from ..utils.validators import SemanticTypeDetector


class DataProfiler:
    """Main data profiling engine."""
    
    def __init__(self, config: Optional[ProfilingConfig] = None):
        """
        Initialize profiler.
        
        Args:
            config: Profiling configuration
        """
        self.config = config or ProfilingConfig()
        self.data_loader = DataLoader(self.config.engine)
        self.semantic_detector = SemanticTypeDetector()
    
    def profile(
        self,
        path: Union[str, Path],
        format_type: DataFormat = DataFormat.AUTO,
        **kwargs
    ) -> DatasetProfile:
        """
        Profile a dataset.
        
        Args:
            path: File or directory path
            format_type: Data format
            **kwargs: Additional options
            
        Returns:
            Complete dataset profile
        """
        start_time = time.time()
        path = Path(path)
        
        # Get file info
        file_info = self.data_loader.get_file_info(path)
        
        # Load data in chunks
        data_chunks = self.data_loader.load_data(
            path, format_type, 
            chunksize=self.config.chunksize,
            **kwargs
        )
        
        # Initialize column stats
        column_stats = {}
        total_rows = 0
        
        # Process data in chunks
        for chunk_idx, chunk in enumerate(data_chunks):
            if self.config.sample_rows and total_rows >= self.config.sample_rows:
                break
            
            total_rows += len(chunk)
            
            # Update column statistics
            self._update_column_stats(column_stats, chunk)
            
            # Limit sample size if specified
            if self.config.sample_rows and total_rows >= self.config.sample_rows:
                break
        
        # Finalize column statistics
        for col_name, stats in column_stats.items():
            column_stats[col_name] = self._finalize_column_stats(stats, total_rows)
        
        # Detect primary key candidates
        key_candidates = self._detect_primary_keys(column_stats, total_rows)
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(column_stats)
        
        profiling_time = time.time() - start_time
        
        return DatasetProfile(
            row_count=total_rows,
            column_count=len(column_stats),
            file_size_bytes=file_info["size_bytes"],
            columns=column_stats,
            primary_key_candidates=key_candidates,
            quality_score=quality_score,
            profiling_time_seconds=profiling_time
        )
    
    def _update_column_stats(self, column_stats: Dict[str, Dict], chunk: pd.DataFrame):
        """Update column statistics with new chunk."""
        for col_name in chunk.columns:
            if col_name not in column_stats:
                column_stats[col_name] = {
                    'name': col_name,
                    'values': [],
                    'null_count': 0,
                    'distinct_values': set(),
                    'numeric_values': [],
                    'string_values': [],
                    'min_value': None,
                    'max_value': None,
                    'sum_value': 0,
                    'count': 0
                }
            
            col_data = chunk[col_name]
            stats = column_stats[col_name]
            
            # Update basic counts
            stats['count'] += len(col_data)
            stats['null_count'] += col_data.isnull().sum()
            
            # Collect non-null values
            non_null_data = col_data.dropna()
            if len(non_null_data) > 0:
                stats['values'].extend(non_null_data.tolist())
                stats['distinct_values'].update(non_null_data.unique())
                
                # Type-specific processing
                if pd.api.types.is_numeric_dtype(col_data):
                    numeric_vals = non_null_data.astype(float)
                    stats['numeric_values'].extend(numeric_vals.tolist())
                    stats['sum_value'] += numeric_vals.sum()
                    
                    # Update min/max
                    if stats['min_value'] is None:
                        stats['min_value'] = numeric_vals.min()
                        stats['max_value'] = numeric_vals.max()
                    else:
                        stats['min_value'] = min(stats['min_value'], numeric_vals.min())
                        stats['max_value'] = max(stats['max_value'], numeric_vals.max())
                else:
                    stats['string_values'].extend(non_null_data.astype(str).tolist())
    
    def _finalize_column_stats(self, stats: Dict, total_rows: int) -> ColumnStats:
        """Finalize column statistics."""
        col_name = stats['name']
        values = stats['values']
        
        # Calculate percentages
        null_percentage = (stats['null_count'] / total_rows) * 100 if total_rows > 0 else 0
        distinct_percentage = (len(stats['distinct_values']) / total_rows) * 100 if total_rows > 0 else 0
        
        # Infer data type
        data_type = self._infer_data_type(values, stats)
        
        # Detect semantic type
        semantic_type = self.semantic_detector.detect_semantic_type(values[:1000])
        
        # Calculate statistics for numeric columns
        mean_value = None
        median_value = None
        std_dev = None
        percentiles = {}
        
        if stats['numeric_values']:
            numeric_array = np.array(stats['numeric_values'])
            mean_value = float(np.mean(numeric_array))
            median_value = float(np.median(numeric_array))
            std_dev = float(np.std(numeric_array))
            
            # Calculate percentiles
            for p in [25, 50, 75, 90, 95, 99]:
                percentiles[p] = float(np.percentile(numeric_array, p))
        
        # Detect outliers (simple IQR method)
        is_outlier_prone = False
        if stats['numeric_values'] and len(stats['numeric_values']) > 10:
            q1 = np.percentile(stats['numeric_values'], 25)
            q3 = np.percentile(stats['numeric_values'], 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = [v for v in stats['numeric_values'] if v < lower_bound or v > upper_bound]
            outlier_percentage = len(outliers) / len(stats['numeric_values']) * 100
            is_outlier_prone = outlier_percentage > 5  # More than 5% outliers
        
        # Get sample values
        sample_values = list(stats['distinct_values'])[:10]
        
        # Generate regex pattern for string columns
        regex_pattern = None
        if stats['string_values'] and semantic_type != SemanticType.GENERIC:
            regex_pattern = self._generate_regex_pattern(stats['string_values'][:100])
        
        return ColumnStats(
            name=col_name,
            data_type=data_type,
            semantic_type=semantic_type,
            null_count=stats['null_count'],
            null_percentage=null_percentage,
            distinct_count=len(stats['distinct_values']),
            distinct_percentage=distinct_percentage,
            min_value=stats['min_value'],
            max_value=stats['max_value'],
            mean_value=mean_value,
            median_value=median_value,
            std_dev=std_dev,
            percentiles=percentiles,
            is_outlier_prone=is_outlier_prone,
            sample_values=sample_values,
            regex_pattern=regex_pattern
        )
    
    def _infer_data_type(self, values: List[Any], stats: Dict) -> DataType:
        """Infer the data type from values."""
        if not values:
            return DataType.NULL
        
        # Check if numeric
        if stats['numeric_values']:
            if all(isinstance(v, int) or (isinstance(v, float) and v.is_integer()) 
                   for v in stats['numeric_values'][:100]):
                return DataType.INTEGER
            else:
                return DataType.FLOAT
        
        # Check if boolean
        bool_values = {'true', 'false', '1', '0', 'yes', 'no', 'y', 'n'}
        if all(str(v).lower() in bool_values for v in values[:100]):
            return DataType.BOOLEAN
        
        # Check if datetime
        if self._is_datetime_column(values[:100]):
            return DataType.DATETIME
        
        # Default to string
        return DataType.STRING
    
    def _is_datetime_column(self, values: List[Any]) -> bool:
        """Check if column contains datetime values."""
        datetime_formats = [
            '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S',
            '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
            '%m-%d-%Y', '%d-%m-%Y', '%Y-%m-%d %H:%M:%S.%f'
        ]
        
        for value in values[:50]:  # Check first 50 values
            if pd.isna(value):
                continue
            
            str_value = str(value)
            is_datetime = False
            
            for fmt in datetime_formats:
                try:
                    pd.to_datetime(str_value, format=fmt)
                    is_datetime = True
                    break
                except (ValueError, TypeError):
                    continue
            
            if not is_datetime:
                return False
        
        return True
    
    def _generate_regex_pattern(self, values: List[str]) -> Optional[str]:
        """Generate regex pattern for string values."""
        if not values:
            return None
        
        # Simple pattern generation for common cases
        sample = values[0]
        
        # Email pattern
        if '@' in sample and '.' in sample:
            return r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # UUID pattern
        if len(sample) == 36 and sample.count('-') == 4:
            return r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        
        # Phone pattern
        if any(c.isdigit() for c in sample) and len(sample) >= 10:
            return r'^\+?[\d\s\-\(\)]{10,}$'
        
        # URL pattern
        if sample.startswith(('http://', 'https://')):
            return r'^https?://[^\s/$.?#].[^\s]*$'
        
        return None
    
    def _detect_primary_keys(self, column_stats: Dict[str, ColumnStats], total_rows: int) -> List[Dict[str, Any]]:
        """Detect potential primary key candidates."""
        candidates = []
        
        for col_name, stats in column_stats.items():
            # Calculate uniqueness score
            uniqueness_score = stats.distinct_percentage / 100
            
            # Calculate nullability score (lower is better)
            nullability_score = 1 - (stats.null_percentage / 100)
            
            # Calculate stability score (based on data type)
            stability_score = 1.0 if stats.data_type in [DataType.INTEGER, DataType.STRING] else 0.5
            
            # Overall score
            overall_score = (uniqueness_score * 0.5 + nullability_score * 0.3 + stability_score * 0.2)
            
            if overall_score > 0.7:  # Threshold for key candidacy
                candidates.append({
                    'column': col_name,
                    'uniqueness_score': uniqueness_score,
                    'nullability_score': nullability_score,
                    'stability_score': stability_score,
                    'overall_score': overall_score,
                    'is_composite': False,
                    'rationale': f"High uniqueness ({uniqueness_score:.2f}), low nulls ({stats.null_percentage:.1f}%)"
                })
        
        # Sort by overall score
        candidates.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return candidates[:5]  # Return top 5 candidates
    
    def _calculate_quality_score(self, column_stats: Dict[str, ColumnStats]) -> float:
        """Calculate overall data quality score."""
        if not column_stats:
            return 0.0
        
        scores = []
        for stats in column_stats.values():
            # Completeness score (lower null percentage is better)
            completeness = 1 - (stats.null_percentage / 100)
            
            # Consistency score (based on data type consistency)
            consistency = 1.0 if stats.semantic_type != SemanticType.GENERIC else 0.7
            
            # Validity score (based on outlier detection)
            validity = 0.8 if not stats.is_outlier_prone else 0.6
            
            # Uniqueness score (moderate uniqueness is good)
            uniqueness = min(stats.distinct_percentage / 100, 1.0)
            
            column_score = (completeness * 0.3 + consistency * 0.3 + validity * 0.2 + uniqueness * 0.2)
            scores.append(column_score)
        
        return sum(scores) / len(scores)
