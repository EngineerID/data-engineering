"""Module 09 — write/read a gold table to emulated S3 / GCS / Azure Blob.

One code path, three clouds: the cloud is chosen by ``--cloud`` and everything
below goes through the fsspec abstraction in ``def_.common.storage``. Targets
local emulators (LocalStack / fake-gcs-server / Azurite) — no real cloud, no spend.

    uv run python modules/09_cloud_portability/object_store_roundtrip.py --cloud aws
    uv run python modules/09_cloud_portability/object_store_roundtrip.py --cloud gcp
    uv run python modules/09_cloud_portability/object_store_roundtrip.py --cloud azure
"""

from __future__ import annotations

import argparse
import io

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

from def_.common.io import parquet_paths
from def_.common.logging import get_logger
from def_.common.storage import Cloud, get_filesystem

logger = get_logger(__name__)

BUCKET = "def-gold"
OBJECT_KEY = "region_revenue.parquet"


def build_gold_table() -> pa.Table:
    """Aggregate region revenue from the seeded star schema (DuckDB → Arrow)."""
    paths = parquet_paths()
    con = duckdb.connect()
    table = con.sql(
        f"""
        SELECT s.region, ROUND(SUM(f.sales_amount), 2) AS revenue
        FROM read_parquet('{paths["fact_sales"]}/**/*.parquet') f
        JOIN read_parquet('{paths["dim_store"]}/**/*.parquet') s
          ON f.store_key = s.store_key
        GROUP BY s.region
        ORDER BY s.region
        """
    ).to_arrow_table()
    con.close()
    return table


_EXISTS_MARKERS = ("exist", "conflict", "alreadyown", "409")


def _ensure_bucket(fs: object, bucket: str) -> None:
    # mkdir creates a bucket (s3fs/gcsfs) or container (adlfs); note makedirs does
    # NOT create an Azure container. Backends signal "already there" differently
    # (FileExistsError, 409 Conflict, BucketAlreadyOwnedByYou), so we treat any
    # existence error as success and re-raise anything else.
    try:
        fs.mkdir(bucket)  # type: ignore[attr-defined]
    except FileExistsError:
        logger.info("bucket %s already exists", bucket)
    except Exception as exc:  # noqa: BLE001 - normalize cross-backend "exists"
        if not any(marker in str(exc).lower() for marker in _EXISTS_MARKERS):
            raise
        logger.info("bucket %s already exists", bucket)
    if hasattr(fs, "invalidate_cache"):
        fs.invalidate_cache()  # type: ignore[attr-defined]


def roundtrip(cloud: Cloud, bucket: str = BUCKET) -> int:
    """Write the gold table to object storage and read it back; return row count."""
    table = build_gold_table()
    fs = get_filesystem(cloud)
    _ensure_bucket(fs, bucket)

    remote_path = f"{bucket}/{OBJECT_KEY}"
    buf = io.BytesIO()
    pq.write_table(table, buf)  # type: ignore[no-untyped-call]
    with fs.open(remote_path, "wb") as handle:  # type: ignore[attr-defined]
        handle.write(buf.getvalue())
    logger.info("wrote %s://%s (%d rows)", cloud, remote_path, table.num_rows)

    with fs.open(remote_path, "rb") as handle:  # type: ignore[attr-defined]
        round_tripped = pq.read_table(handle)  # type: ignore[no-untyped-call]
    logger.info("read back %d rows from %s", round_tripped.num_rows, cloud)
    return int(round_tripped.num_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Object-store roundtrip across clouds")
    parser.add_argument("--cloud", choices=["aws", "gcp", "azure"], required=True)
    parser.add_argument("--bucket", default=BUCKET)
    args = parser.parse_args()
    rows = roundtrip(args.cloud, args.bucket)
    print(f"cloud={args.cloud} rows_roundtripped={rows}")


if __name__ == "__main__":
    main()
