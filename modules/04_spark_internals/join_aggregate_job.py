"""Star join + aggregate on the standalone Spark cluster (Learning Spark — cluster model)."""

from __future__ import annotations

import sys

from pyspark.sql import functions as F

from def_.common.io import data_dir, parquet_paths
from def_.common.logging import get_logger
from def_.common.spark import build_spark_session

logger = get_logger(__name__)


def main() -> None:
    spark = build_spark_session("def-join-aggregate", cluster=True)
    paths = parquet_paths()

    fact = spark.read.parquet(str(paths["fact_sales"]))
    dim_date = spark.read.parquet(str(paths["dim_date"]))
    dim_product = spark.read.parquet(str(paths["dim_product"]))
    dim_store = spark.read.parquet(str(paths["dim_store"]))
    dim_customer = spark.read.parquet(str(paths["dim_customer"]))

    joined = (
        fact.join(dim_date, "date_key")
        .join(dim_product, "product_key")
        .join(dim_store, "store_key")
        .join(dim_customer, "customer_key")
    )

    result = joined.groupBy("region", "category", "year").agg(
        F.sum("sales_amount").alias("total_sales"),
        F.sum("quantity").alias("total_quantity"),
        F.count("*").alias("line_count"),
    )

    explain_dir = data_dir() / "explain"
    explain_dir.mkdir(parents=True, exist_ok=True)
    explain_path = explain_dir / "join_aggregate.txt"

    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        result.explain(mode="formatted")
    explain_path.write_text(buf.getvalue(), encoding="utf-8")

    out = data_dir() / "spark_output" / "join_aggregate"
    result.write.mode("overwrite").parquet(str(out))
    row_count = result.count()
    logger.info("Wrote %d aggregated rows to %s", row_count, out)
    logger.info("Explain plan saved to %s", explain_path)
    logger.info("Open Spark UI: master :8080, application :4040 — find shuffle stages")

    spark.stop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Job failed")
        sys.exit(1)
