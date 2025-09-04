"""
Command-line interface for datamodel_profiler.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import click

from .core.profiler import DataProfiler
from .core.schema_inference import SchemaInferencer
from .core.key_detection import KeyDetector
from .core.constraint_suggestion import ConstraintSuggester
from .io.data_loader import DataFormat
from .utils.types import ProfilingConfig


@click.group()
@click.version_option(version="1.0.0")
def main():
    """DataModel Profiler - A production-ready Python package for data profiling and schema inference."""
    pass


@main.command()
@click.option('--path', '-p', required=True, help='File or folder path to profile')
@click.option('--format', 'format_type', type=click.Choice(['auto', 'csv', 'parquet', 'json', 'yaml', 'xlsx', 'orc']), 
              default='auto', help='Data format (auto-detect if auto)')
@click.option('--engine', type=click.Choice(['pandas', 'polars']), default='pandas', help='Data processing engine')
@click.option('--delimiter', default=',', help='CSV delimiter')
@click.option('--encoding', default='utf-8', help='File encoding')
@click.option('--sheet-name', help='Excel sheet name')
@click.option('--json-lines', is_flag=True, help='JSON Lines format')
@click.option('--chunksize', type=int, default=10000, help='Chunk size for processing')
@click.option('--sample-rows', type=int, help='Number of rows to sample (None for all)')
@click.option('--html-report', help='Path for HTML report (requires ydata-profiling)')
@click.option('--md-report', help='Path for Markdown report')
@click.option('--output-dir', '-o', default='.', help='Output directory')
def profile(path, format_type, engine, delimiter, encoding, sheet_name, json_lines, 
           chunksize, sample_rows, html_report, md_report, output_dir):
    """Profile a dataset and generate statistics."""
    try:
        # Create configuration
        config = ProfilingConfig(
            engine=engine,
            sample_rows=sample_rows,
            chunksize=chunksize,
            enable_html_report=bool(html_report),
            enable_md_report=bool(md_report)
        )
        
        # Initialize profiler
        profiler = DataProfiler(config)
        
        # Convert format string to enum
        format_enum = DataFormat(format_type)
        
        # Prepare options
        options = {
            'delimiter': delimiter,
            'encoding': encoding,
            'json_lines': json_lines
        }
        if sheet_name:
            options['sheet_name'] = sheet_name
        
        click.echo(f"Profiling {path}...")
        
        # Run profiling
        profile_result = profiler.profile(path, format_enum, **options)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save profile results
        profile_file = output_path / "profile.json"
        with open(profile_file, 'w') as f:
            json.dump({
                "row_count": profile_result.row_count,
                "column_count": profile_result.column_count,
                "file_size_bytes": profile_result.file_size_bytes,
                "quality_score": profile_result.quality_score,
                "profiling_time_seconds": profile_result.profiling_time_seconds,
                "columns": {
                    name: {
                        "data_type": col.data_type.value,
                        "semantic_type": col.semantic_type.value,
                        "null_count": col.null_count,
                        "null_percentage": col.null_percentage,
                        "distinct_count": col.distinct_count,
                        "distinct_percentage": col.distinct_percentage,
                        "min_value": col.min_value,
                        "max_value": col.max_value,
                        "mean_value": col.mean_value,
                        "median_value": col.median_value,
                        "std_dev": col.std_dev,
                        "percentiles": col.percentiles,
                        "is_outlier_prone": col.is_outlier_prone,
                        "sample_values": col.sample_values,
                        "regex_pattern": col.regex_pattern
                    }
                    for name, col in profile_result.columns.items()
                },
                "primary_key_candidates": profile_result.primary_key_candidates
            }, f, indent=2, default=str)
        
        click.echo(f"Profile saved to {profile_file}")
        
        # Generate column stats CSV
        stats_file = output_path / "column_stats.csv"
        import pandas as pd
        stats_data = []
        for name, col in profile_result.columns.items():
            stats_data.append({
                'column_name': name,
                'data_type': col.data_type.value,
                'semantic_type': col.semantic_type.value,
                'null_count': col.null_count,
                'null_percentage': col.null_percentage,
                'distinct_count': col.distinct_count,
                'distinct_percentage': col.distinct_percentage,
                'min_value': col.min_value,
                'max_value': col.max_value,
                'mean_value': col.mean_value,
                'std_dev': col.std_dev,
                'is_outlier_prone': col.is_outlier_prone
            })
        
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_csv(stats_file, index=False)
        click.echo(f"Column statistics saved to {stats_file}")
        
        # Generate HTML report if requested
        if html_report:
            try:
                _generate_html_report(profile_result, html_report)
                click.echo(f"HTML report saved to {html_report}")
            except ImportError:
                click.echo("Warning: HTML report requires ydata-profiling. Install with: pip install ydata-profiling")
        
        # Generate Markdown report if requested
        if md_report:
            _generate_markdown_report(profile_result, md_report)
            click.echo(f"Markdown report saved to {md_report}")
        
        click.echo("Profiling completed successfully!")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--path', '-p', required=True, help='File or folder path to analyze')
@click.option('--format', 'format_type', type=click.Choice(['auto', 'csv', 'parquet', 'json', 'yaml', 'xlsx', 'orc']), 
              default='auto', help='Data format (auto-detect if auto)')
@click.option('--engine', type=click.Choice(['pandas', 'polars']), default='pandas', help='Data processing engine')
@click.option('--sql-dialect', type=click.Choice(['postgres', 'snowflake']), default='postgres', help='SQL dialect for DDL')
@click.option('--table-name', default='table', help='Table name for schema')
@click.option('--nullable-threshold', type=float, default=0.01, help='Threshold for NOT NULL constraint')
@click.option('--decimal-precision-scale-strategy', default='auto', help='Decimal precision strategy')
@click.option('--timestamp-tz', is_flag=True, help='Include timezone in timestamp types')
@click.option('--output-dir', '-o', default='.', help='Output directory')
def infer_schema(path, format_type, engine, sql_dialect, table_name, nullable_threshold, 
                decimal_precision_scale_strategy, timestamp_tz, output_dir):
    """Infer schema from dataset and generate multiple format outputs."""
    try:
        # Create configuration
        config = ProfilingConfig(engine=engine)
        
        # Initialize schema inferencer
        inferencer = SchemaInferencer(config)
        
        # Convert format string to enum
        format_enum = DataFormat(format_type)
        
        click.echo(f"Inferring schema for {path}...")
        
        # Infer schema
        schema = inferencer.infer_schema(path, table_name, format_enum, sql_dialect)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export schema in multiple formats
        output_files = inferencer.export_schema(schema, output_path, sql_dialect)
        
        click.echo("Schema inference completed successfully!")
        click.echo("Generated files:")
        for format_name, file_path in output_files.items():
            click.echo(f"  {format_name}: {file_path}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--path', '-p', required=True, help='File or folder path to analyze')
@click.option('--lookup-dir', help='Directory containing lookup/dimension files')
@click.option('--max-domain-size', type=int, default=100, help='Maximum domain size for allowed_values')
@click.option('--regex-level', type=click.Choice(['basic', 'strict']), default='basic', help='Regex pattern level')
@click.option('--output-dir', '-o', default='.', help='Output directory')
def suggest_constraints(path, lookup_dir, max_domain_size, regex_level, output_dir):
    """Suggest data quality constraints."""
    try:
        # Create configuration
        config = ProfilingConfig(
            max_domain_size=max_domain_size,
            regex_level=regex_level
        )
        
        # Initialize constraint suggester
        suggester = ConstraintSuggester(config)
        
        # Convert format string to enum
        format_enum = DataFormat.auto
        
        click.echo(f"Analyzing constraints for {path}...")
        
        # Suggest constraints
        suggestions = suggester.suggest_constraints(path, format_enum, lookup_dir)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export constraints
        constraints_file = output_path / "constraints.json"
        suggester.export_constraints(suggestions, constraints_file)
        click.echo(f"Constraints saved to {constraints_file}")
        
        # Generate markdown report
        md_file = output_path / "constraints.md"
        suggester.generate_markdown_report(suggestions, md_file)
        click.echo(f"Constraints report saved to {md_file}")
        
        click.echo(f"Generated {len(suggestions)} constraint suggestions")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--path', '-p', required=True, help='File or folder path to analyze')
@click.option('--format', 'format_type', type=click.Choice(['auto', 'csv', 'parquet', 'json', 'yaml', 'xlsx', 'orc']), 
              default='auto', help='Data format (auto-detect if auto)')
@click.option('--max-composite-size', type=int, default=3, help='Maximum composite key size')
@click.option('--output-dir', '-o', default='.', help='Output directory')
def detect_keys(path, format_type, max_composite_size, output_dir):
    """Detect primary key candidates."""
    try:
        # Create configuration
        config = ProfilingConfig()
        
        # Initialize key detector
        detector = KeyDetector(config)
        
        # Convert format string to enum
        format_enum = DataFormat(format_type)
        
        click.echo(f"Detecting keys for {path}...")
        
        # Detect keys
        candidates = detector.detect_keys(path, format_enum, max_composite_size)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export key candidates
        keys_file = output_path / "key_candidates.json"
        detector.export_key_candidates(candidates, keys_file)
        click.echo(f"Key candidates saved to {keys_file}")
        
        click.echo(f"Found {len(candidates)} key candidates")
        if candidates:
            top_candidate = candidates[0]
            click.echo(f"Top candidate: {', '.join(top_candidate.columns)} (score: {top_candidate.overall_score:.3f})")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def _generate_html_report(profile_result, output_path):
    """Generate HTML report using ydata-profiling."""
    try:
        import ydata_profiling
        from ydata_profiling import ProfileReport
        
        # This is a placeholder - in practice, you'd need to load the data
        # and create a proper ProfileReport
        click.echo("HTML report generation requires data loading - not implemented in this example")
        
    except ImportError:
        raise ImportError("ydata-profiling is required for HTML reports")


def _generate_markdown_report(profile_result, output_path):
    """Generate Markdown report."""
    lines = [
        "# Data Profiling Report",
        "",
        f"**Dataset**: {profile_result.row_count:,} rows × {profile_result.column_count} columns",
        f"**File Size**: {profile_result.file_size_bytes / (1024*1024):.2f} MB",
        f"**Quality Score**: {profile_result.quality_score:.2f}",
        f"**Profiling Time**: {profile_result.profiling_time_seconds:.2f} seconds",
        "",
        "## Column Statistics",
        ""
    ]
    
    for name, col in profile_result.columns.items():
        lines.extend([
            f"### {name}",
            f"- **Type**: {col.data_type.value} ({col.semantic_type.value})",
            f"- **Nulls**: {col.null_count:,} ({col.null_percentage:.1f}%)",
            f"- **Distinct**: {col.distinct_count:,} ({col.distinct_percentage:.1f}%)",
        ])
        
        if col.min_value is not None:
            lines.append(f"- **Range**: {col.min_value} to {col.max_value}")
        
        if col.mean_value is not None:
            lines.append(f"- **Mean**: {col.mean_value:.2f} (std: {col.std_dev:.2f})")
        
        if col.is_outlier_prone:
            lines.append("- **⚠️ Outlier prone**")
        
        if col.sample_values:
            lines.append(f"- **Sample values**: {', '.join(map(str, col.sample_values[:5]))}")
        
        lines.append("")
    
    # Primary key candidates
    if profile_result.primary_key_candidates:
        lines.extend([
            "## Primary Key Candidates",
            ""
        ])
        
        for i, candidate in enumerate(profile_result.primary_key_candidates[:5], 1):
            lines.extend([
                f"### {i}. {', '.join(candidate['column'])}",
                f"- **Score**: {candidate['overall_score']:.3f}",
                f"- **Rationale**: {candidate['rationale']}",
                ""
            ])
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    main()
