"""Module 08 — local bronze/silver/gold medallion on generated Parquet."""

from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

import duckdb

from def_.common.io import data_dir, parquet_paths


def medallion_root() -> Path:
    root = data_dir() / "medallion"
    root.mkdir(parents=True, exist_ok=True)
    return root


def run_pipeline() -> dict[str, int | str]:
    paths = parquet_paths()
    root = medallion_root()
    bronze = root / "bronze" / "fact_sales"
    silver = root / "silver" / "fact_sales.parquet"
    gold = root / "gold" / "regional_revenue.parquet"
    lineage_file = root / "lineage.json"

    if bronze.exists():
        shutil.rmtree(bronze)
    if silver.exists():
        silver.unlink()
    if gold.exists():
        gold.unlink()
    bronze.mkdir(parents=True)
    for parquet_file in paths["fact_sales"].glob("**/*.parquet"):
        dest = bronze / parquet_file.name
        shutil.copy2(parquet_file, dest)

    silver.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    fact_glob = str(bronze / "*.parquet")
    con.sql(
        f"""
        COPY (
            SELECT * FROM read_parquet('{fact_glob}')
            WHERE quantity > 0
        ) TO '{silver}' (FORMAT PARQUET)
        """
    )

    store_glob = str(paths["dim_store"] / "**/*.parquet")
    gold.parent.mkdir(parents=True, exist_ok=True)
    con.sql(
        f"""
        COPY (
            SELECT s.region, SUM(f.sales_amount) AS revenue
            FROM read_parquet('{silver}') AS f
            JOIN read_parquet('{store_glob}') AS s ON f.store_key = s.store_key
            GROUP BY s.region
        ) TO '{gold}' (FORMAT PARQUET)
        """
    )

    bronze_count = con.sql(f"SELECT COUNT(*) FROM read_parquet('{fact_glob}')").fetchone()[0]
    silver_count = con.sql(f"SELECT COUNT(*) FROM read_parquet('{silver}')").fetchone()[0]
    gold_count = con.sql(f"SELECT COUNT(*) FROM read_parquet('{gold}')").fetchone()[0]

    lineage = {
        "timestamp": datetime.now(UTC).isoformat(),
        "bronze_rows": bronze_count,
        "silver_rows": silver_count,
        "gold_rows": gold_count,
        "layers": ["bronze", "silver", "gold"],
    }
    lineage_file.write_text(json.dumps(lineage, indent=2), encoding="utf-8")
    return {
        "bronze_rows": bronze_count,
        "silver_rows": silver_count,
        "gold_rows": gold_count,
        "lineage_path": str(lineage_file),
    }


def main() -> None:
    stats = run_pipeline()
    print(stats)


if __name__ == "__main__":
    main()
