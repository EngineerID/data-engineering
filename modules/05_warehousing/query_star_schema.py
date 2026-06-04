"""Module 05 — DuckDB star-schema queries over generated Parquet."""

from __future__ import annotations

import duckdb

from def_.common.io import parquet_paths


def regional_sales_aggregate() -> duckdb.DuckDBPyRelation:
    paths = parquet_paths()
    fact = paths["fact_sales"]
    store = paths["dim_store"]
    con = duckdb.connect()
    return con.sql(
        f"""
        SELECT s.region, SUM(f.sales_amount) AS total_sales, COUNT(*) AS line_count
        FROM read_parquet('{fact}/**/*.parquet') AS f
        JOIN read_parquet('{store}/**/*.parquet') AS s ON f.store_key = s.store_key
        GROUP BY s.region
        ORDER BY s.region
        """
    )


def main() -> None:
    rel = regional_sales_aggregate()
    rows = rel.fetchall()
    print(f"regions={len(rows)}")
    for row in rows[:5]:
        print(row)


if __name__ == "__main__":
    main()
