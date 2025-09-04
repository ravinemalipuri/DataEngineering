"""
Schema inference engine for multiple output formats.
"""

from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import json

from ..io.data_loader import DataLoader, DataFormat
from ..utils.types import (
    DataType, SemanticType, ColumnStats, DatasetProfile, 
    TableSchema, SchemaInfo, ProfilingConfig
)
from ..utils.formatters import JSONSchemaFormatter, AvroFormatter, SQLFormatter, ArrowFormatter


class SchemaInferencer:
    """Schema inference engine."""
    
    def __init__(self, config: Optional[ProfilingConfig] = None):
        """
        Initialize schema inferencer.
        
        Args:
            config: Profiling configuration
        """
        self.config = config or ProfilingConfig()
        self.data_loader = DataLoader(self.config.engine)
        
        # Initialize formatters
        self.json_formatter = JSONSchemaFormatter()
        self.avro_formatter = AvroFormatter()
        self.sql_formatter = SQLFormatter()
        self.arrow_formatter = ArrowFormatter()
    
    def infer_schema(
        self,
        path: Union[str, Path],
        table_name: str = "table",
        format_type: DataFormat = DataFormat.AUTO,
        sql_dialect: str = "postgres",
        **kwargs
    ) -> TableSchema:
        """
        Infer schema from dataset.
        
        Args:
            path: File or directory path
            table_name: Name for the table
            format_type: Data format
            sql_dialect: SQL dialect for DDL generation
            **kwargs: Additional options
            
        Returns:
            Inferred table schema
        """
        # Load data and get basic info
        data_chunks = self.data_loader.load_data(path, format_type, **kwargs)
        first_chunk = next(data_chunks)
        
        # Infer column schemas
        columns = []
        for col_name in first_chunk.columns:
            col_data = first_chunk[col_name]
            schema_info = self._infer_column_schema(col_name, col_data)
            columns.append(schema_info)
        
        # Detect primary key
        primary_key = self._detect_primary_key(columns)
        
        return TableSchema(
            table_name=table_name,
            columns=columns,
            primary_key=primary_key
        )
    
    def _infer_column_schema(self, col_name: str, col_data) -> SchemaInfo:
        """Infer schema for a single column."""
        import pandas as pd
        
        # Determine data type
        data_type = self._infer_data_type(col_data)
        
        # Determine nullability
        nullable = col_data.isnull().any()
        
        # Generate description
        description = self._generate_column_description(col_name, col_data, data_type)
        
        # Generate constraints
        constraints = self._generate_constraints(col_data, data_type)
        
        # Get sample values
        examples = col_data.dropna().head(5).tolist()
        
        return SchemaInfo(
            name=col_name,
            data_type=data_type,
            nullable=nullable,
            description=description,
            constraints=constraints,
            examples=examples
        )
    
    def _infer_data_type(self, col_data) -> str:
        """Infer data type from column data."""
        import pandas as pd
        
        # Check for null-only column
        if col_data.isnull().all():
            return "null"
        
        # Get non-null data
        non_null_data = col_data.dropna()
        
        if len(non_null_data) == 0:
            return "null"
        
        # Check pandas dtype
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
            # Try to infer from sample values
            sample_values = non_null_data.head(100)
            
            # Check if it's a datetime
            if self._is_datetime_column(sample_values):
                return "datetime"
            
            # Check if it's numeric
            if self._is_numeric_column(sample_values):
                if all(isinstance(v, int) or (isinstance(v, float) and v.is_integer()) 
                       for v in sample_values):
                    return "integer"
                else:
                    return "float"
            
            # Default to string
            return "string"
    
    def _is_datetime_column(self, values) -> bool:
        """Check if column contains datetime values."""
        import pandas as pd
        
        datetime_formats = [
            '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S',
            '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
            '%m-%d-%Y', '%d-%m-%Y', '%Y-%m-%d %H:%M:%S.%f'
        ]
        
        for value in values[:50]:
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
    
    def _is_numeric_column(self, values) -> bool:
        """Check if column contains numeric values."""
        for value in values[:50]:
            try:
                float(value)
            except (ValueError, TypeError):
                return False
        return True
    
    def _generate_column_description(self, col_name: str, col_data, data_type: str) -> str:
        """Generate description for column."""
        import pandas as pd
        
        non_null_count = col_data.notnull().sum()
        total_count = len(col_data)
        null_percentage = ((total_count - non_null_count) / total_count) * 100
        
        description = f"{data_type.title()} column"
        
        if null_percentage > 0:
            description += f" with {null_percentage:.1f}% null values"
        
        # Add semantic hints
        if data_type == "string":
            sample_values = col_data.dropna().head(10)
            if any('@' in str(v) for v in sample_values):
                description += " (appears to contain email addresses)"
            elif any(len(str(v)) == 36 and str(v).count('-') == 4 for v in sample_values):
                description += " (appears to contain UUIDs)"
        
        return description
    
    def _generate_constraints(self, col_data, data_type: str) -> Optional[Dict[str, Any]]:
        """Generate constraints for column."""
        import pandas as pd
        
        constraints = {}
        non_null_data = col_data.dropna()
        
        if len(non_null_data) == 0:
            return None
        
        if data_type == "string":
            # String length constraints
            lengths = non_null_data.astype(str).str.len()
            min_length = int(lengths.min())
            max_length = int(lengths.max())
            
            if min_length == max_length:
                constraints["minLength"] = min_length
                constraints["maxLength"] = max_length
            else:
                constraints["minLength"] = min_length
                constraints["maxLength"] = max_length
            
            # Check for enum-like values
            unique_values = non_null_data.unique()
            if len(unique_values) <= 20:  # Low cardinality
                constraints["enum"] = unique_values.tolist()
        
        elif data_type in ["integer", "float"]:
            # Numeric range constraints
            numeric_data = pd.to_numeric(non_null_data, errors='coerce').dropna()
            if len(numeric_data) > 0:
                constraints["minimum"] = float(numeric_data.min())
                constraints["maximum"] = float(numeric_data.max())
        
        return constraints if constraints else None
    
    def _detect_primary_key(self, columns: List[SchemaInfo]) -> Optional[List[str]]:
        """Detect potential primary key from columns."""
        # Look for columns that are non-nullable and likely unique
        candidates = []
        
        for col in columns:
            if not col.nullable and col.data_type in ["integer", "string"]:
                # Check if it might be unique (simple heuristic)
                if col.constraints and "enum" in col.constraints:
                    # Skip enum columns as they're likely not unique
                    continue
                
                candidates.append(col.name)
        
        # Return first candidate or None
        return [candidates[0]] if candidates else None
    
    def export_schema(
        self,
        table_schema: TableSchema,
        output_dir: Union[str, Path],
        sql_dialect: str = "postgres"
    ) -> Dict[str, Path]:
        """
        Export schema in multiple formats.
        
        Args:
            table_schema: Table schema to export
            output_dir: Output directory
            sql_dialect: SQL dialect for DDL
            
        Returns:
            Dictionary mapping format names to output file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_files = {}
        
        # JSON Schema
        json_schema = self.json_formatter.format_schema(table_schema)
        json_path = output_dir / "schema.json"
        with open(json_path, 'w') as f:
            json.dump(json_schema, f, indent=2)
        output_files["json"] = json_path
        
        # Avro Schema
        avro_schema = self.avro_formatter.format_schema(table_schema)
        avro_path = output_dir / "schema.avsc"
        with open(avro_path, 'w') as f:
            json.dump(avro_schema, f, indent=2)
        output_files["avro"] = avro_path
        
        # SQL DDL
        sql_formatter = SQLFormatter(sql_dialect)
        sql_ddl = sql_formatter.format_schema(table_schema)
        sql_path = output_dir / "schema.sql"
        with open(sql_path, 'w') as f:
            f.write(sql_ddl)
        output_files["sql"] = sql_path
        
        # Arrow Schema
        arrow_schema = self.arrow_formatter.format_schema(table_schema)
        arrow_path = output_dir / "schema_arrow.txt"
        with open(arrow_path, 'w') as f:
            f.write(arrow_schema)
        output_files["arrow"] = arrow_path
        
        # Pydantic Model
        pydantic_code = self._generate_pydantic_model(table_schema)
        pydantic_path = output_dir / "schema_pydantic.py"
        with open(pydantic_path, 'w') as f:
            f.write(pydantic_code)
        output_files["pydantic"] = pydantic_path
        
        # Dataclass Model
        dataclass_code = self._generate_dataclass_model(table_schema)
        dataclass_path = output_dir / "schema_dataclass.py"
        with open(dataclass_path, 'w') as f:
            f.write(dataclass_code)
        output_files["dataclass"] = dataclass_path
        
        return output_files
    
    def _generate_pydantic_model(self, table_schema: TableSchema) -> str:
        """Generate Pydantic model code."""
        lines = [
            "from pydantic import BaseModel, Field",
            "from typing import Optional",
            "from datetime import datetime",
            "",
            f"class {table_schema.table_name.title()}(BaseModel):",
        ]
        
        for column in table_schema.columns:
            python_type = self._get_python_type(column.data_type)
            
            if column.nullable:
                python_type = f"Optional[{python_type}]"
                default = "None"
            else:
                default = "..."
            
            field_def = f"    {column.name}: {python_type} = Field(default={default}"
            
            if column.description:
                field_def += f', description="{column.description}"'
            
            field_def += ")"
            lines.append(field_def)
        
        return "\n".join(lines)
    
    def _generate_dataclass_model(self, table_schema: TableSchema) -> str:
        """Generate dataclass model code."""
        lines = [
            "from dataclasses import dataclass",
            "from typing import Optional",
            "from datetime import datetime",
            "",
            f"@dataclass",
            f"class {table_schema.table_name.title()}:",
        ]
        
        for column in table_schema.columns:
            python_type = self._get_python_type(column.data_type)
            
            if column.nullable:
                python_type = f"Optional[{python_type}]"
                default = "None"
            else:
                default = "..."
            
            field_def = f"    {column.name}: {python_type}"
            if default != "...":
                field_def += f" = {default}"
            
            lines.append(field_def)
        
        return "\n".join(lines)
    
    def _get_python_type(self, data_type: str) -> str:
        """Convert data type to Python type."""
        type_mapping = {
            "string": "str",
            "integer": "int",
            "float": "float",
            "boolean": "bool",
            "datetime": "datetime",
            "date": "datetime",
            "time": "datetime",
            "binary": "bytes",
            "array": "list",
            "object": "dict",
            "null": "None"
        }
        return type_mapping.get(data_type, "str")
