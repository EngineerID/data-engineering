"""Deliberately broken Spark job to reproduce executor OOM (High Performance Spark — memory)."""

from __future__ import annotations

import sys

from pyspark.sql import functions as F

from def_.common.io import parquet_paths
from def_.common.logging import get_logger
from def_.common.spark import build_spark_session

logger = get_logger(__name__)

# Skewed key forces one partition to hold most rows after shuffle
SKEW_KEY = 1


def main() -> None:
    spark = build_spark_session(
        "def-oom-exercise",
        cluster=True,
        extra_conf={
            "spark.executor.memory": "256m",
            "spark.executor.memoryOverhead": "64m",
            "spark.sql.shuffle.partitions": "200",
            "spark.sql.autoBroadcastJoinThreshold": "-1",
        },
    )
    paths = parquet_paths()
    fact = spark.read.parquet(str(paths["fact_sales"]))
    dim_product = spark.read.parquet(str(paths["dim_product"]))

    # Artificial skew column
    skewed = fact.withColumn(
        "skew_bucket",
        F.when(F.col("product_key") == SKEW_KEY, F.lit(1)).otherwise(F.col("product_key")),
    )

    # Large shuffle + wide aggregation without broadcast
    result = (
        skewed.join(dim_product, "product_key")
        .groupBy("skew_bucket", "category", "brand")
        .agg(
            F.collect_list("sales_amount").alias("all_amounts"),
            F.sum("quantity").alias("total_qty"),
        )
    )
    result.count()
    spark.stop()


if __name__ == "__main__":
    logger.warning(
        "This job is designed to OOM executors. "
        "Fix: broadcast dim_product, repartition by skew_bucket, raise executor memory."
    )
    try:
        main()
    except Exception:
        logger.exception("Expected failure for OOM lab")
        sys.exit(1)
