"""
Main data loader for handling multiple file formats.
"""

import os
import pathlib
from typing import Iterator, Union, Optional, Dict, Any
from enum import Enum
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Optional ORC support
try:
    import pyarrow.orc as orc
    ORC_AVAILABLE = True
except ImportError:
    orc = None
    ORC_AVAILABLE = False

from .formats import (
    CSVReader, ParquetReader, JSONReader, YAMLReader, 
    ExcelReader, ORCReader
)


class DataFormat(Enum):
    """Supported data formats."""
    AUTO = "auto"
    CSV = "csv"
    PARQUET = "parquet"
    JSON = "json"
    YAML = "yaml"
    EXCEL = "xlsx"
    ORC = "orc"


class DataLoader:
    """Main data loader that handles multiple formats."""
    
    def __init__(self, engine: str = "pandas"):
        """
        Initialize data loader.
        
        Args:
            engine: Data processing engine ("pandas" or "polars")
        """
        self.engine = engine
        self.readers = {
            DataFormat.CSV: CSVReader(engine),
            DataFormat.PARQUET: ParquetReader(engine),
            DataFormat.JSON: JSONReader(engine),
            DataFormat.YAML: YAMLReader(engine),
            DataFormat.EXCEL: ExcelReader(engine),
            DataFormat.ORC: ORCReader(engine),
        }
    
    def detect_format(self, path: Union[str, pathlib.Path]) -> DataFormat:
        """
        Auto-detect file format from extension.
        
        Args:
            path: File or directory path
            
        Returns:
            Detected data format
        """
        path = pathlib.Path(path)
        
        if path.is_dir():
            # For directories, check first file
            files = list(path.glob("*"))
            if not files:
                raise ValueError(f"No files found in directory: {path}")
            path = files[0]
        
        suffix = path.suffix.lower()
        
        format_map = {
            '.csv': DataFormat.CSV,
            '.parquet': DataFormat.PARQUET,
            '.json': DataFormat.JSON,
            '.jsonl': DataFormat.JSON,
            '.ndjson': DataFormat.JSON,
            '.yaml': DataFormat.YAML,
            '.yml': DataFormat.YAML,
            '.xlsx': DataFormat.EXCEL,
            '.xls': DataFormat.EXCEL,
            '.orc': DataFormat.ORC,
        }
        
        return format_map.get(suffix, DataFormat.CSV)
    
    def load_data(
        self,
        path: Union[str, pathlib.Path],
        format_type: DataFormat = DataFormat.AUTO,
        **kwargs
    ) -> Iterator[pd.DataFrame]:
        """
        Load data from file or directory.
        
        Args:
            path: File or directory path
            format_type: Data format (auto-detect if AUTO)
            **kwargs: Format-specific options
            
        Yields:
            DataFrame chunks
        """
        path = pathlib.Path(path)
        
        if format_type == DataFormat.AUTO:
            format_type = self.detect_format(path)
        
        if path.is_file():
            yield from self._load_single_file(path, format_type, **kwargs)
        elif path.is_dir():
            yield from self._load_directory(path, format_type, **kwargs)
        else:
            raise ValueError(f"Path does not exist: {path}")
    
    def _load_single_file(
        self,
        path: pathlib.Path,
        format_type: DataFormat,
        **kwargs
    ) -> Iterator[pd.DataFrame]:
        """Load data from a single file."""
        if format_type not in self.readers:
            raise ValueError(f"Unsupported format: {format_type}")
        
        reader = self.readers[format_type]
        yield from reader.read_file(path, **kwargs)
    
    def _load_directory(
        self,
        path: pathlib.Path,
        format_type: DataFormat,
        **kwargs
    ) -> Iterator[pd.DataFrame]:
        """Load data from all files in directory."""
        if format_type == DataFormat.AUTO:
            # Group files by format
            files_by_format = {}
            for file_path in path.iterdir():
                if file_path.is_file():
                    detected_format = self.detect_format(file_path)
                    if detected_format not in files_by_format:
                        files_by_format[detected_format] = []
                    files_by_format[detected_format].append(file_path)
            
            # Process each format group
            for fmt, files in files_by_format.items():
                for file_path in sorted(files):
                    yield from self._load_single_file(file_path, fmt, **kwargs)
        else:
            # Load all files of specified format
            pattern = f"*.{format_type.value}"
            for file_path in sorted(path.glob(pattern)):
                yield from self._load_single_file(file_path, format_type, **kwargs)
    
    def get_file_info(self, path: Union[str, pathlib.Path]) -> Dict[str, Any]:
        """
        Get basic file information.
        
        Args:
            path: File path
            
        Returns:
            Dictionary with file information
        """
        path = pathlib.Path(path)
        
        if not path.exists():
            raise ValueError(f"File does not exist: {path}")
        
        stat = path.stat()
        
        return {
            "path": str(path),
            "name": path.name,
            "size_bytes": stat.st_size,
            "size_mb": stat.st_size / (1024 * 1024),
            "format": self.detect_format(path).value,
            "modified_time": stat.st_mtime,
        }
    
    def estimate_row_count(
        self,
        path: Union[str, pathlib.Path],
        format_type: DataFormat = DataFormat.AUTO,
        sample_size: int = 1000
    ) -> int:
        """
        Estimate total row count without loading full dataset.
        
        Args:
            path: File path
            format_type: Data format
            sample_size: Number of rows to sample for estimation
            
        Returns:
            Estimated row count
        """
        path = pathlib.Path(path)
        
        if format_type == DataFormat.AUTO:
            format_type = self.detect_format(path)
        
        if format_type == DataFormat.PARQUET:
            # Parquet files have metadata
            try:
                parquet_file = pq.ParquetFile(path)
                return parquet_file.metadata.num_rows
            except Exception:
                pass
        
        # For other formats, sample and extrapolate
        try:
            sample_df = next(self.load_data(path, format_type, nrows=sample_size))
            if len(sample_df) == 0:
                return 0
            
            # Estimate based on file size
            file_size = path.stat().st_size
            sample_size_bytes = len(sample_df.to_csv().encode())
            estimated_rows = int((file_size / sample_size_bytes) * len(sample_df))
            
            return max(estimated_rows, len(sample_df))
        except Exception:
            return 0
