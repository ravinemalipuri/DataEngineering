import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
import mssparkutils


DEFAULT_CONN = "conn_src_rw_as400_odbc_dev"
DEFAULT_SOURCE_SYSTEM = 1


def parse_args():
    parser = argparse.ArgumentParser(description="Metadata-driven spark ingest")
    parser.add_argument(
        "--connection",
        default=DEFAULT_CONN,
        help=f"Fabric connection name (default: {DEFAULT_CONN})",
    )
    parser.add_argument(
        "--source-system-id",
        type=int,
        default=DEFAULT_SOURCE_SYSTEM,
        help=f"source_system_id from metadata_db (default: {DEFAULT_SOURCE_SYSTEM})",
    )
    parser.add_argument(
        "--load-type",
        choices=["FULL", "INCREMENTAL", "HYBRID"],
        default="INCREMENTAL",
        help="load type (FULL/INCREMENTAL/HYBRID)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    spark = SparkSession.builder.getOrCreate()
    conn = mssparkutils.credentials.getConnection(args.connection)
    jdbc_url, jdbc_user, jdbc_password = conn["url"], conn["user"], conn["password"]

    metadata = (
        spark.read.format("delta")
        .load("/OneLake/Workspaces/YourWorkspace/Lakehouses/metadata/Tables/source_objects")
        .filter(col("source_system_id") == lit(args.source_system_id))
        .filter(col("is_active") == lit(1))
    )

    columns = (
        spark.read.format("delta")
        .load("/OneLake/Workspaces/YourWorkspace/Lakehouses/metadata/Tables/source_object_columns")
    )

    for row in metadata.collect():
        df = (
            spark.read.format("jdbc")
            .option("url", jdbc_url)
            .option("dbtable", row.source_object_name)
            .option("user", jdbc_user)
            .option("password", jdbc_password)
            .load()
        )

        # join columns
        rule_df = columns.filter(col("source_object_id") == lit(row.source_object_id))
        if rule_df.count():
            dq_rule_set = rule_df.select(col("dq_rule_set")).first()["dq_rule_set"]
            print(f"Applying DQ for {row.source_object_name}: {dq_rule_set}")
            # placeholder for rule execution

        target_path = row.target_path
        if row.load_type.upper() == "FULL":
            df.write.format("delta").mode("overwrite").save(target_path)
        else:
            df.write.format("delta").mode("overwrite").save(target_path)

        print(f"Loaded {row.source_object_name} -> {target_path}")


if __name__ == "__main__":
    main()

