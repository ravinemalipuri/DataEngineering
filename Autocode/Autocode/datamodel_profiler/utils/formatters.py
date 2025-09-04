"""
Schema formatters for different output formats.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import pyarrow as pa

from .types import DataType, SemanticType, ColumnStats, TableSchema, SchemaInfo


class JSONSchemaFormatter:
    """JSON Schema formatter (Draft 2020-12)."""
    
    def format_schema(self, table_schema: TableSchema) -> Dict[str, Any]:
        """Format table schema as JSON Schema."""
        properties = {}
        required = []
        
        for column in table_schema.columns:
            prop = self._format_column_property(column)
            properties[column.name] = prop
            
            if not column.nullable:
                required.append(column.name)
        
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "title": table_schema.table_name,
            "properties": properties,
            "required": required,
            "additionalProperties": False
        }
        
        return schema
    
    def _format_column_property(self, column: SchemaInfo) -> Dict[str, Any]:
        """Format a single column as JSON Schema property."""
        prop = {
            "type": self._get_json_schema_type(column.data_type),
            "description": column.description or f"Column {column.name}"
        }
        
        # Add constraints
        if column.constraints:
            if "minLength" in column.constraints:
                prop["minLength"] = column.constraints["minLength"]
            if "maxLength" in column.constraints:
                prop["maxLength"] = column.constraints["maxLength"]
            if "minimum" in column.constraints:
                prop["minimum"] = column.constraints["minimum"]
            if "maximum" in column.constraints:
                prop["maximum"] = column.constraints["maximum"]
            if "pattern" in column.constraints:
                prop["pattern"] = column.constraints["pattern"]
            if "enum" in column.constraints:
                prop["enum"] = column.constraints["enum"]
        
        # Handle nullable types
        if column.nullable:
            if prop["type"] != "null":
                prop["type"] = [prop["type"], "null"]
            else:
                prop["type"] = "null"
        
        return prop
    
    def _get_json_schema_type(self, data_type: str) -> str:
        """Convert data type to JSON Schema type."""
        type_mapping = {
            "string": "string",
            "integer": "integer",
            "float": "number",
            "boolean": "boolean",
            "datetime": "string",
            "date": "string",
            "time": "string",
            "binary": "string",
            "array": "array",
            "object": "object",
            "null": "null"
        }
        return type_mapping.get(data_type, "string")


class AvroFormatter:
    """Avro schema formatter."""
    
    def format_schema(self, table_schema: TableSchema) -> Dict[str, Any]:
        """Format table schema as Avro schema."""
        fields = []
        
        for column in table_schema.columns:
            field = self._format_column_field(column)
            fields.append(field)
        
        schema = {
            "type": "record",
            "name": table_schema.table_name,
            "namespace": "com.datamodelprofiler",
            "fields": fields
        }
        
        return schema
    
    def _format_column_field(self, column: SchemaInfo) -> Dict[str, Any]:
        """Format a single column as Avro field."""
        avro_type = self._get_avro_type(column.data_type)
        
        # Handle nullable fields
        if column.nullable and avro_type != "null":
            avro_type = ["null", avro_type]
        
        field = {
            "name": column.name,
            "type": avro_type
        }
        
        if column.description:
            field["doc"] = column.description
        
        return field
    
    def _get_avro_type(self, data_type: str) -> str:
        """Convert data type to Avro type."""
        type_mapping = {
            "string": "string",
            "integer": "long",
            "float": "double",
            "boolean": "boolean",
            "datetime": "string",
            "date": "string",
            "time": "string",
            "binary": "bytes",
            "array": "array",
            "object": "record",
            "null": "null"
        }
        return type_mapping.get(data_type, "string")


class SQLFormatter:
    """SQL DDL formatter."""
    
    def __init__(self, dialect: str = "postgres"):
        self.dialect = dialect
    
    def format_schema(self, table_schema: TableSchema) -> str:
        """Format table schema as SQL DDL."""
        lines = [f"CREATE TABLE {table_schema.table_name} ("]
        
        column_definitions = []
        for column in table_schema.columns:
            col_def = self._format_column_definition(column)
            column_definitions.append(f"    {col_def}")
        
        lines.extend(column_definitions)
        
        # Add primary key
        if table_schema.primary_key:
            pk_columns = ", ".join(table_schema.primary_key)
            lines.append(f"    PRIMARY KEY ({pk_columns})")
        
        lines.append(");")
        
        # Add foreign keys
        if table_schema.foreign_keys:
            for fk in table_schema.foreign_keys:
                fk_sql = self._format_foreign_key(table_schema.table_name, fk)
                lines.append(fk_sql)
        
        return "\n".join(lines)
    
    def _format_column_definition(self, column: SchemaInfo) -> str:
        """Format a single column as SQL definition."""
        sql_type = self._get_sql_type(column.data_type)
        
        # Add NOT NULL constraint
        nullable = "" if column.nullable else " NOT NULL"
        
        # Add constraints
        constraints = []
        if column.constraints:
            if "minLength" in column.constraints and "maxLength" in column.constraints:
                if column.constraints["minLength"] == column.constraints["maxLength"]:
                    constraints.append(f"CHECK (LENGTH({column.name}) = {column.constraints['maxLength']})")
                else:
                    constraints.append(f"CHECK (LENGTH({column.name}) BETWEEN {column.constraints['minLength']} AND {column.constraints['maxLength']})")
            elif "minimum" in column.constraints and "maximum" in column.constraints:
                constraints.append(f"CHECK ({column.name} BETWEEN {column.constraints['minimum']} AND {column.constraints['maximum']})")
        
        constraint_str = " " + " ".join(constraints) if constraints else ""
        
        return f"{column.name} {sql_type}{nullable}{constraint_str}"
    
    def _get_sql_type(self, data_type: str) -> str:
        """Convert data type to SQL type."""
        if self.dialect == "postgres":
            type_mapping = {
                "string": "TEXT",
                "integer": "BIGINT",
                "float": "DECIMAL(38,9)",
                "boolean": "BOOLEAN",
                "datetime": "TIMESTAMP",
                "date": "DATE",
                "time": "TIME",
                "binary": "BYTEA",
                "array": "TEXT[]",
                "object": "JSONB",
                "null": "TEXT"
            }
        elif self.dialect == "snowflake":
            type_mapping = {
                "string": "VARCHAR",
                "integer": "NUMBER(38,0)",
                "float": "NUMBER(38,9)",
                "boolean": "BOOLEAN",
                "datetime": "TIMESTAMP_NTZ",
                "date": "DATE",
                "time": "TIME",
                "binary": "BINARY",
                "array": "VARIANT",
                "object": "VARIANT",
                "null": "VARCHAR"
            }
        else:  # ANSI SQL
            type_mapping = {
                "string": "VARCHAR(255)",
                "integer": "BIGINT",
                "float": "DECIMAL(38,9)",
                "boolean": "BOOLEAN",
                "datetime": "TIMESTAMP",
                "date": "DATE",
                "time": "TIME",
                "binary": "BLOB",
                "array": "TEXT",
                "object": "TEXT",
                "null": "VARCHAR(255)"
            }
        
        return type_mapping.get(data_type, "VARCHAR(255)")
    
    def _format_foreign_key(self, table_name: str, fk: Dict[str, str]) -> str:
        """Format foreign key constraint."""
        return f"ALTER TABLE {table_name} ADD FOREIGN KEY ({fk['column']}) REFERENCES {fk['referenced_table']}({fk['referenced_column']});"


class ArrowFormatter:
    """Arrow schema formatter."""
    
    def format_schema(self, table_schema: TableSchema) -> str:
        """Format table schema as Arrow schema description."""
        lines = [f"Arrow Schema for {table_schema.table_name}:"]
        lines.append("=" * 50)
        
        for column in table_schema.columns:
            arrow_type = self._get_arrow_type(column.data_type)
            nullable = "nullable" if column.nullable else "non-nullable"
            
            line = f"{column.name}: {arrow_type} ({nullable})"
            if column.description:
                line += f" - {column.description}"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def _get_arrow_type(self, data_type: str) -> str:
        """Convert data type to Arrow type."""
        type_mapping = {
            "string": "string",
            "integer": "int64",
            "float": "double",
            "boolean": "bool",
            "datetime": "timestamp[ns]",
            "date": "date32",
            "time": "time64[ns]",
            "binary": "binary",
            "array": "list",
            "object": "struct",
            "null": "null"
        }
        return type_mapping.get(data_type, "string")
