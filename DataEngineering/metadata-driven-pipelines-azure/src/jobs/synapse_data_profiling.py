

"""
On-demand data profiling utility for Synapse / Spark.

Features:
    * Profiles Parquet data (single file or folder) with optional sampling.
    * Allows profiling a subset of files by explicit file name.
    * Writes profiling metrics to storage (CSV) for ad-hoc review.
    * Persists the profiling run to metadata_db.dbo.data_profiling_results
      using an ODBC connection to Azure SQL Database.
"""

from __future__ import annotations

import argparse
import json
import posixpath
from typing import Dict, List, Optional, Sequence

import pyodbc
from pyspark.sql import DataFrame, SparkSession, functions as F
from pyspark.sql.types import (
    DateType,
    DoubleType,
    LongType,
    NumericType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

PROFILE_TYPE = "BASIC_STATS"
PROFILE_SCHEMA = StructType(
    [
        StructField("column_name", StringType(), True),
        StructField("data_type", StringType(), True),
        StructField("row_count", LongType(), True),
        StructField("non_null_count", LongType(), True),
        StructField("null_count", LongType(), True),
        StructField("null_pct", DoubleType(), True),
        StructField("distinct_count", LongType(), True),
        StructField("distinct_pct", DoubleType(), True),
        StructField("min_value", StringType(), True),
        StructField("max_value", StringType(), True),
        StructField("sample_values", StringType(), True),
    ]
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synapse data profiling runner")
    parser.add_argument("--source-path", required=True, help="Folder or file path to Parquet data")
    parser.add_argument(
        "--file-names",
        nargs="+",
        help="Optional list of file names inside the source path to profile. "
        "If omitted the whole path (all tables/files) is profiled.",
    )
    parser.add_argument(
        "--sample-row-limit",
        type=int,
        help="Optional cap on rows for faster development/testing runs",
    )
    parser.add_argument(
        "--profile-output-path",
        help="Optional destination (folder) to write the profiling CSV report",
    )
    parser.add_argument("--run-id", required=True, help="Unique identifier for the profiling run")
    parser.add_argument(
        "--source-object-id",
        type=int,
        required=True,
        help="Metadata identifier of the source object being profiled",
    )
    parser.add_argument("--layer", default="BRONZE", help="Data layer label stored in metadata")
    parser.add_argument("--sql-server", required=True, help="Azure SQL server hostname")
    parser.add_argument("--sql-port", type=int, default=1433, help="Azure SQL server port")
    parser.add_argument("--sql-database", required=True, help="Azure SQL database name")
    parser.add_argument("--sql-username", required=True, help="SQL authentication username")
    parser.add_argument("--sql-password", required=True, help="SQL authentication password")
    parser.add_argument(
        "--sql-driver",
        default="{ODBC Driver 18 for SQL Server}",
        help="Installed ODBC driver to use for the connection",
    )
    parser.add_argument(
        "--sql-table",
        default="[metadata_db].[dbo].[data_profiling_results]",
        help="Fully-qualified target table for profiling results",
    )
    parser.add_argument(
        "--trust-server-certificate",
        action="store_true",
        help="Set to trust the SQL Server certificate (default: disabled)",
    )
    return parser.parse_args()


def resolve_input_paths(source_path: str, file_names: Optional[Sequence[str]]) -> List[str]:
    if not file_names:
        return [source_path]
    normalized = source_path.rstrip("/")
    return [posixpath.join(normalized, name.lstrip("/")) for name in file_names]


def read_source_df(spark: SparkSession, paths: Sequence[str]) -> DataFrame:
    print(f"Reading parquet from: {paths}")
    return spark.read.parquet(*paths)


def profile_dataframe(df: DataFrame) -> List[Dict]:
    total_rows = df.count()
    print(f"Total rows profiled: {total_rows}")
    print(f"Total columns profiled: {len(df.columns)}")

    profile_rows: List[Dict] = []
    for field in df.schema:
        col_name = field.name
        col_type = field.dataType
        col_type_str = str(col_type)
        print(f"Profiling column: {col_name} ({col_type_str})")

        agg_exprs = {
            "null_count": F.sum(F.when(F.col(col_name).isNull(), 1).otherwise(0)),
            "distinct_count": F.approx_count_distinct(col_name),
        }

        is_numeric = isinstance(col_type, NumericType)
        is_temporal = isinstance(col_type, (DateType, TimestampType))
        if is_numeric or is_temporal:
            agg_exprs["min"] = F.min(col_name)
            agg_exprs["max"] = F.max(col_name)

        agg_columns = [expr.alias(name) for name, expr in agg_exprs.items()]
        agg_values = df.agg(*agg_columns).collect()[0].asDict()

        null_count = int(agg_values.get("null_count", 0) or 0)
        distinct_count = int(agg_values.get("distinct_count", 0) or 0)
        min_value = agg_values.get("min")
        max_value = agg_values.get("max")

        non_null_count = total_rows - null_count
        null_pct = (null_count / total_rows * 100) if total_rows else 0
        distinct_pct = (distinct_count / total_rows * 100) if total_rows else 0

        sample_values = (
            df.select(col_name)
            .where(F.col(col_name).isNotNull())
            .distinct()
            .limit(5)
            .rdd.map(lambda r: r[0])
            .collect()
        )
        sample_values_str = [str(v) for v in sample_values]

        profile_rows.append(
            {
                "column_name": col_name,
                "data_type": col_type_str,
                "row_count": total_rows,
                "non_null_count": non_null_count,
                "null_count": null_count,
                "null_pct": round(null_pct, 2),
                "distinct_count": distinct_count,
                "distinct_pct": round(distinct_pct, 2),
                "min_value": str(min_value) if min_value is not None else None,
                "max_value": str(max_value) if max_value is not None else None,
                "sample_values": sample_values_str,
            }
        )
    return profile_rows


def build_profile_df(spark: SparkSession, profile_rows: List[Dict]) -> DataFrame:
    rows = [
        (
            entry["column_name"],
            entry["data_type"],
            entry["row_count"],
            entry["non_null_count"],
            entry["null_count"],
            entry["null_pct"],
            entry["distinct_count"],
            entry["distinct_pct"],
            entry["min_value"],
            entry["max_value"],
            ", ".join(entry["sample_values"]),
        )
        for entry in profile_rows
    ]
    if not rows:
        return spark.createDataFrame(spark.sparkContext.emptyRDD(), PROFILE_SCHEMA)
    return spark.createDataFrame(rows, PROFILE_SCHEMA)


def write_profile_csv(profile_df: DataFrame, output_path: Optional[str]) -> None:
    if not output_path:
        return
    (
        profile_df.coalesce(1)
        .write.mode("overwrite")
        .option("header", "true")
        .csv(output_path)
    )
    print(f"Profiling report written to: {output_path}")


def build_connection_string(args: argparse.Namespace) -> str:
    driver = args.sql_driver
    if not driver.startswith("{"):
        driver = "{" + driver + "}"
    server = args.sql_server
    if args.sql_port:
        server = f"{server},{args.sql_port}"
    parts = [
        f"DRIVER={driver}",
        f"SERVER={server}",
        f"DATABASE={args.sql_database}",
        f"UID={args.sql_username}",
        f"PWD={args.sql_password}",
        "Encrypt=yes",
        f"TrustServerCertificate={'yes' if args.trust_server_certificate else 'no'}",
        "Connection Timeout=30",
    ]
    return ";".join(parts)


def persist_profiling_results(
    profile_rows: List[Dict],
    connection_string: str,
    target_table: str,
    run_id: str,
    source_object_id: int,
    layer: str,
    source_path: str,
    file_names: Optional[Sequence[str]],
    sample_row_limit: Optional[int],
) -> None:
    if not profile_rows:
        print("No profiling results to persist.")
        return

    profile_params = json.dumps(
        {
            "source_path": source_path,
            "file_names": list(file_names) if file_names else [],
            "sample_row_limit": sample_row_limit,
        }
    )
    payload = []
    for entry in profile_rows:
        metric_value = json.dumps(
            {
                "data_type": entry["data_type"],
                "null_count": entry["null_count"],
                "null_pct": entry["null_pct"],
                "distinct_count": entry["distinct_count"],
                "distinct_pct": entry["distinct_pct"],
                "min_value": entry["min_value"],
                "max_value": entry["max_value"],
                "sample_values": entry["sample_values"],
            }
        )
        payload.append(
            (
                run_id,
                source_object_id,
                layer,
                entry["column_name"],
                PROFILE_TYPE,
                profile_params,
                metric_value,
                entry["row_count"],
                entry["row_count"],
            )
        )

    insert_stmt = f"""
        INSERT INTO {target_table} (
            run_id,
            source_object_id,
            layer,
            column_name,
            profile_type,
            profile_params,
            metric_value,
            sample_size,
            row_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    conn = pyodbc.connect(connection_string, autocommit=False)
    try:
        cursor = conn.cursor()
        cursor.executemany(insert_stmt, payload)
        conn.commit()
        print(f"Inserted {len(payload)} profiling rows into {target_table}.")
    finally:
        conn.close()


def main():
    args = parse_arguments()
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()

    input_paths = resolve_input_paths(args.source_path, args.file_names)
    df = read_source_df(spark, input_paths)
    if args.sample_row_limit:
        print(f"Applying sample row limit: {args.sample_row_limit}")
        df = df.limit(args.sample_row_limit)

    profile_rows = profile_dataframe(df)
    profile_df = build_profile_df(spark, profile_rows)
    try:
        display(profile_df)
    except NameError:
        pass

    write_profile_csv(profile_df, args.profile_output_path)

    connection_string = build_connection_string(args)
    persist_profiling_results(
        profile_rows,
        connection_string,
        args.sql_table,
        args.run_id,
        args.source_object_id,
        args.layer,
        args.source_path,
        args.file_names,
        args.sample_row_limit,
    )


if __name__ == "__main__":
    main()