"""SparkSession builder — cluster-first, not notebook-local."""

from __future__ import annotations

import os

from pyspark.sql import SparkSession

from def_.common.logging import get_logger

logger = get_logger(__name__)


def build_spark_session(
    app_name: str,
    *,
    cluster: bool = True,
    extra_conf: dict[str, str] | None = None,
) -> SparkSession:
    """Build a SparkSession. Graded jobs use cluster=True (standalone master)."""
    builder = SparkSession.builder.appName(app_name)
    if cluster:
        master = os.environ.get("SPARK_MASTER_URL", "spark://localhost:7077")
        builder = builder.master(master)
        logger.info("Connecting to cluster master: %s", master)
    else:
        builder = builder.master("local[2]")
        logger.warning("Using local[*] mode — only for isolated unit tests")

    conf = {
        "spark.sql.shuffle.partitions": os.environ.get("SPARK_SHUFFLE_PARTITIONS", "8"),
        "spark.sql.adaptive.enabled": "true",
    }
    if extra_conf:
        conf.update(extra_conf)
    for key, value in conf.items():
        builder = builder.config(key, value)

    return builder.getOrCreate()
