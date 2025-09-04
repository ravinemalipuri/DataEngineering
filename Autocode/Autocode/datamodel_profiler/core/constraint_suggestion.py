"""
Constraint suggestion system with Great Expectations integration.
"""

import re
from typing import Dict, List, Optional, Any, Union, Set
from pathlib import Path
import pandas as pd
import numpy as np

from ..io.data_loader import DataLoader, DataFormat
from ..utils.types import (
    DataType, SemanticType, ColumnStats, DatasetProfile, 
    ProfilingConfig, ConstraintSuggestion
)
from ..utils.validators import SemanticTypeDetector


class ConstraintSuggester:
    """Constraint suggestion system."""
    
    def __init__(self, config: Optional[ProfilingConfig] = None):
        """
        Initialize constraint suggester.
        
        Args:
            config: Profiling configuration
        """
        self.config = config or ProfilingConfig()
        self.data_loader = DataLoader(self.config.engine)
        self.semantic_detector = SemanticTypeDetector()
    
    def suggest_constraints(
        self,
        path: Union[str, Path],
        format_type: DataFormat = DataFormat.AUTO,
        lookup_dir: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> List[ConstraintSuggestion]:
        """
        Suggest data quality constraints.
        
        Args:
            path: File or directory path
            format_type: Data format
            lookup_dir: Directory containing lookup/dimension files
            **kwargs: Additional options
            
        Returns:
            List of constraint suggestions
        """
        # Load main dataset
        data_chunks = self.data_loader.load_data(path, format_type, **kwargs)
        first_chunk = next(data_chunks)
        
        # Load lookup tables if provided
        lookup_tables = {}
        if lookup_dir:
            lookup_tables = self._load_lookup_tables(lookup_dir)
        
        # Analyze each column
        suggestions = []
        for col_name in first_chunk.columns:
            col_data = first_chunk[col_name]
            col_suggestions = self._analyze_column_constraints(
                col_name, col_data, lookup_tables
            )
            suggestions.extend(col_suggestions)
        
        # Add cross-column constraints
        cross_column_suggestions = self._suggest_cross_column_constraints(first_chunk)
        suggestions.extend(cross_column_suggestions)
        
        return suggestions
    
    def _load_lookup_tables(self, lookup_dir: Union[str, Path]) -> Dict[str, pd.DataFrame]:
        """Load lookup tables from directory."""
        lookup_dir = Path(lookup_dir)
        lookup_tables = {}
        
        for file_path in lookup_dir.glob("*"):
            if file_path.is_file():
                try:
                    # Auto-detect format and load
                    format_type = self.data_loader.detect_format(file_path)
                    data_chunks = self.data_loader.load_data(file_path, format_type)
                    df = next(data_chunks)
                    
                    # Use filename as table name
                    table_name = file_path.stem
                    lookup_tables[table_name] = df
                except Exception as e:
                    print(f"Warning: Could not load lookup table {file_path}: {e}")
        
        return lookup_tables
    
    def _analyze_column_constraints(
        self,
        col_name: str,
        col_data: pd.Series,
        lookup_tables: Dict[str, pd.DataFrame]
    ) -> List[ConstraintSuggestion]:
        """Analyze constraints for a single column."""
        suggestions = []
        
        # Type constraints
        type_suggestion = self._suggest_type_constraint(col_name, col_data)
        if type_suggestion:
            suggestions.append(type_suggestion)
        
        # Range constraints
        range_suggestions = self._suggest_range_constraints(col_name, col_data)
        suggestions.extend(range_suggestions)
        
        # Pattern constraints
        pattern_suggestion = self._suggest_pattern_constraint(col_name, col_data)
        if pattern_suggestion:
            suggestions.append(pattern_suggestion)
        
        # Allowed values constraints
        allowed_values_suggestion = self._suggest_allowed_values_constraint(col_name, col_data)
        if allowed_values_suggestion:
            suggestions.append(allowed_values_suggestion)
        
        # Foreign key constraints
        fk_suggestions = self._suggest_foreign_key_constraints(col_name, col_data, lookup_tables)
        suggestions.extend(fk_suggestions)
        
        # Completeness constraints
        completeness_suggestion = self._suggest_completeness_constraint(col_name, col_data)
        if completeness_suggestion:
            suggestions.append(completeness_suggestion)
        
        return suggestions
    
    def _suggest_type_constraint(self, col_name: str, col_data: pd.Series) -> Optional[ConstraintSuggestion]:
        """Suggest type constraint."""
        non_null_data = col_data.dropna()
        
        if len(non_null_data) == 0:
            return None
        
        # Infer data type
        if pd.api.types.is_integer_dtype(col_data):
            data_type = "integer"
            confidence = 0.9
        elif pd.api.types.is_float_dtype(col_data):
            data_type = "float"
            confidence = 0.9
        elif pd.api.types.is_bool_dtype(col_data):
            data_type = "boolean"
            confidence = 0.9
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            data_type = "datetime"
            confidence = 0.9
        elif pd.api.types.is_string_dtype(col_data):
            data_type = "string"
            confidence = 0.8
        else:
            return None
        
        return ConstraintSuggestion(
            column_name=col_name,
            constraint_type="expect_column_values_to_be_of_type",
            parameters={"column": col_name, "type_": data_type},
            confidence=confidence,
            rationale=f"Column contains {data_type} values with {confidence:.1%} confidence"
        )
    
    def _suggest_range_constraints(self, col_name: str, col_data: pd.Series) -> List[ConstraintSuggestion]:
        """Suggest range constraints for numeric columns."""
        suggestions = []
        non_null_data = col_data.dropna()
        
        if len(non_null_data) == 0:
            return suggestions
        
        # Check if numeric
        try:
            numeric_data = pd.to_numeric(non_null_data, errors='raise')
        except (ValueError, TypeError):
            return suggestions
        
        # Min/Max constraints
        min_val = float(numeric_data.min())
        max_val = float(numeric_data.max())
        
        # Add some tolerance
        range_tolerance = (max_val - min_val) * 0.1
        suggested_min = min_val - range_tolerance
        suggested_max = max_val + range_tolerance
        
        suggestions.append(ConstraintSuggestion(
            column_name=col_name,
            constraint_type="expect_column_values_to_be_between",
            parameters={
                "column": col_name,
                "min_value": suggested_min,
                "max_value": suggested_max
            },
            confidence=0.8,
            rationale=f"Values range from {min_val} to {max_val}, suggesting range constraint"
        ))
        
        # Percentile-based constraints
        p5 = float(numeric_data.quantile(0.05))
        p95 = float(numeric_data.quantile(0.95))
        
        if p5 != min_val or p95 != max_val:
            suggestions.append(ConstraintSuggestion(
                column_name=col_name,
                constraint_type="expect_column_values_to_be_between",
                parameters={
                    "column": col_name,
                    "min_value": p5,
                    "max_value": p95
                },
                confidence=0.9,
                rationale=f"95% of values fall between {p5} and {p95} (percentile-based constraint)"
            ))
        
        return suggestions
    
    def _suggest_pattern_constraint(self, col_name: str, col_data: pd.Series) -> Optional[ConstraintSuggestion]:
        """Suggest regex pattern constraint."""
        non_null_data = col_data.dropna()
        
        if len(non_null_data) == 0:
            return None
        
        # Convert to strings
        str_data = non_null_data.astype(str)
        
        # Detect semantic type
        semantic_type = self.semantic_detector.detect_semantic_type(str_data.tolist())
        
        if semantic_type == SemanticType.EMAIL:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            rationale = "Column appears to contain email addresses"
        elif semantic_type == SemanticType.UUID:
            pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            rationale = "Column appears to contain UUIDs"
        elif semantic_type == SemanticType.PHONE:
            pattern = r'^\+?[\d\s\-\(\)]{10,}$'
            rationale = "Column appears to contain phone numbers"
        elif semantic_type == SemanticType.URL:
            pattern = r'^https?://[^\s/$.?#].[^\s]*$'
            rationale = "Column appears to contain URLs"
        else:
            # Try to generate pattern from sample values
            pattern = self._generate_pattern_from_values(str_data.head(100))
            if not pattern:
                return None
            rationale = "Pattern inferred from sample values"
        
        return ConstraintSuggestion(
            column_name=col_name,
            constraint_type="expect_column_values_to_match_regex",
            parameters={
                "column": col_name,
                "regex": pattern
            },
            confidence=0.7,
            rationale=rationale
        )
    
    def _generate_pattern_from_values(self, values: pd.Series) -> Optional[str]:
        """Generate regex pattern from sample values."""
        if len(values) == 0:
            return None
        
        # Simple pattern generation
        sample = values.iloc[0]
        
        # Check for common patterns
        if all(len(str(v)) == len(sample) for v in values):
            # Fixed length
            length = len(sample)
            if all(str(v).isdigit() for v in values):
                return f"^\\d{{{length}}}$"
            elif all(str(v).isalpha() for v in values):
                return f"^[a-zA-Z]{{{length}}}$"
            elif all(str(v).isalnum() for v in values):
                return f"^[a-zA-Z0-9]{{{length}}}$"
        
        return None
    
    def _suggest_allowed_values_constraint(self, col_name: str, col_data: pd.Series) -> Optional[ConstraintSuggestion]:
        """Suggest allowed values constraint for low-cardinality columns."""
        non_null_data = col_data.dropna()
        
        if len(non_null_data) == 0:
            return None
        
        unique_values = non_null_data.unique()
        unique_count = len(unique_values)
        
        # Only suggest for low-cardinality columns
        if unique_count > self.config.max_domain_size:
            return None
        
        # Check if values are consistent
        total_count = len(non_null_data)
        if unique_count / total_count < 0.1:  # Less than 10% unique
            return None
        
        allowed_values = unique_values.tolist()
        
        return ConstraintSuggestion(
            column_name=col_name,
            constraint_type="expect_column_values_to_be_in_set",
            parameters={
                "column": col_name,
                "value_set": allowed_values
            },
            confidence=0.8,
            rationale=f"Column has only {unique_count} distinct values, suggesting enum constraint"
        )
    
    def _suggest_foreign_key_constraints(
        self,
        col_name: str,
        col_data: pd.Series,
        lookup_tables: Dict[str, pd.DataFrame]
    ) -> List[ConstraintSuggestion]:
        """Suggest foreign key constraints."""
        suggestions = []
        
        if not lookup_tables:
            return suggestions
        
        non_null_data = col_data.dropna()
        if len(non_null_data) == 0:
            return suggestions
        
        # Check against each lookup table
        for table_name, lookup_df in lookup_tables.items():
            for lookup_col in lookup_df.columns:
                # Check for potential foreign key relationship
                lookup_values = set(lookup_df[lookup_col].dropna().unique())
                data_values = set(non_null_data.unique())
                
                # Calculate overlap
                overlap = len(data_values.intersection(lookup_values))
                overlap_ratio = overlap / len(data_values) if len(data_values) > 0 else 0
                
                # Suggest foreign key if high overlap
                if overlap_ratio > 0.8:
                    suggestions.append(ConstraintSuggestion(
                        column_name=col_name,
                        constraint_type="expect_column_values_to_be_in_set",
                        parameters={
                            "column": col_name,
                            "value_set": list(lookup_values)
                        },
                        confidence=overlap_ratio,
                        rationale=f"High overlap ({overlap_ratio:.1%}) with {table_name}.{lookup_col}, suggesting foreign key relationship"
                    ))
        
        return suggestions
    
    def _suggest_completeness_constraint(self, col_name: str, col_data: pd.Series) -> Optional[ConstraintSuggestion]:
        """Suggest completeness constraint."""
        null_count = col_data.isnull().sum()
        total_count = len(col_data)
        null_percentage = (null_count / total_count) * 100
        
        # Only suggest if null percentage is low
        if null_percentage > 10:
            return None
        
        return ConstraintSuggestion(
            column_name=col_name,
            constraint_type="expect_column_values_to_not_be_null",
            parameters={"column": col_name},
            confidence=1 - (null_percentage / 100),
            rationale=f"Column has only {null_percentage:.1f}% null values, suggesting NOT NULL constraint"
        )
    
    def _suggest_cross_column_constraints(self, df: pd.DataFrame) -> List[ConstraintSuggestion]:
        """Suggest cross-column constraints."""
        suggestions = []
        
        # Check for date range constraints
        date_columns = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
        
        if len(date_columns) >= 2:
            # Check for start/end date pairs
            for i, start_col in enumerate(date_columns):
                for end_col in date_columns[i+1:]:
                    if self._is_date_range_pair(start_col, end_col, df):
                        suggestions.append(ConstraintSuggestion(
                            column_name=f"{start_col}__{end_col}",
                            constraint_type="expect_column_pair_values_A_to_be_greater_than_B",
                            parameters={
                                "column_A": end_col,
                                "column_B": start_col
                            },
                            confidence=0.8,
                            rationale=f"{end_col} should be greater than {start_col} (date range constraint)"
                        ))
        
        return suggestions
    
    def _is_date_range_pair(self, start_col: str, end_col: str, df: pd.DataFrame) -> bool:
        """Check if two columns form a date range pair."""
        # Simple heuristic: check if end dates are generally after start dates
        valid_pairs = df[[start_col, end_col]].dropna()
        
        if len(valid_pairs) == 0:
            return False
        
        # Check if end > start for most pairs
        valid_count = (valid_pairs[end_col] > valid_pairs[start_col]).sum()
        total_count = len(valid_pairs)
        
        return valid_count / total_count > 0.8
    
    def export_constraints(
        self,
        suggestions: List[ConstraintSuggestion],
        output_path: Union[str, Path]
    ) -> Path:
        """
        Export constraints to JSON file.
        
        Args:
            suggestions: List of constraint suggestions
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        output_path = Path(output_path)
        
        # Convert to Great Expectations format (if available) or generic format
        ge_constraints = []
        for suggestion in suggestions:
            ge_constraint = {
                "expectation_type": suggestion.constraint_type,
                "kwargs": suggestion.parameters,
                "meta": {
                    "confidence": suggestion.confidence,
                    "rationale": suggestion.rationale
                }
            }
            ge_constraints.append(ge_constraint)
        
        export_data = {
            "expectations": ge_constraints,
            "summary": {
                "total_constraints": len(suggestions),
                "constraint_types": list(set(s.constraint_type for s in suggestions)),
                "columns_with_constraints": list(set(s.column_name for s in suggestions))
            }
        }
        
        import json
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return output_path
    
    def generate_markdown_report(
        self,
        suggestions: List[ConstraintSuggestion],
        output_path: Union[str, Path]
    ) -> Path:
        """
        Generate markdown report of constraints.
        
        Args:
            suggestions: List of constraint suggestions
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        output_path = Path(output_path)
        
        # Group by column
        by_column = {}
        for suggestion in suggestions:
            if suggestion.column_name not in by_column:
                by_column[suggestion.column_name] = []
            by_column[suggestion.column_name].append(suggestion)
        
        # Generate markdown
        lines = [
            "# Data Quality Constraints Report",
            "",
            f"Generated {len(suggestions)} constraint suggestions across {len(by_column)} columns.",
            "",
            "## Summary",
            "",
            f"- **Total Constraints**: {len(suggestions)}",
            f"- **Columns with Constraints**: {len(by_column)}",
            f"- **Constraint Types**: {', '.join(set(s.constraint_type for s in suggestions))}",
            "",
            "## Column Constraints",
            ""
        ]
        
        for col_name, col_suggestions in by_column.items():
            lines.extend([
                f"### {col_name}",
                ""
            ])
            
            for suggestion in col_suggestions:
                lines.extend([
                    f"**{suggestion.constraint_type}** (Confidence: {suggestion.confidence:.1%})",
                    "",
                    f"*{suggestion.rationale}*",
                    "",
                    "```json",
                    json.dumps(suggestion.parameters, indent=2),
                    "```",
                    ""
                ])
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
        
        return output_path
