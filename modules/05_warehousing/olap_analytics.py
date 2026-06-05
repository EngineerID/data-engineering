"""Module 05 — OLAP aggregation patterns on the star schema (DuckDB).

Makes the *dimensions vs measures* distinction concrete (the Tableau gap):
``region`` / ``category`` are dimensions you group by; ``sales_amount`` is a
measure you aggregate. All runnable over `make seed` Parquet, no Docker.

1. **ROLLUP / GROUPING SETS** — hierarchical subtotals + grand total.
2. **CUBE** — every combination of dimensions (the OLAP data cube, Gray 1997).
3. **Window functions** — running total of revenue per region (rank/cumulative).
4. **Materialized aggregate** — pre-compute a gold table once, query it cheaply.
"""

from __future__ import annotations

from typing import Any

import duckdb

from def_.common.io import parquet_paths


def _connect() -> duckdb.DuckDBPyConnection:
    paths = parquet_paths()
    con = duckdb.connect()
    con.sql(
        f"""
        CREATE VIEW fact_sales AS
            SELECT * FROM read_parquet('{paths["fact_sales"]}/**/*.parquet');
        CREATE VIEW dim_store AS
            SELECT * FROM read_parquet('{paths["dim_store"]}/**/*.parquet');
        CREATE VIEW dim_product AS
            SELECT * FROM read_parquet('{paths["dim_product"]}/**/*.parquet');
        CREATE VIEW sales_by_region_category AS
            SELECT s.region, p.category, f.sales_amount
            FROM fact_sales f
            JOIN dim_store s ON f.store_key = s.store_key
            JOIN dim_product p ON f.product_key = p.product_key;
        """
    )
    return con


def rollup_region_category() -> list[tuple[Any, ...]]:
    """Subtotals per region, per (region, category), and a grand total.

    ``GROUPING(region)`` = 1 marks the grand-total row; NULLs in dimension
    columns mark subtotal rows.
    """
    con = _connect()
    rows = con.sql(
        """
        SELECT region, category,
               ROUND(SUM(sales_amount), 2) AS revenue,
               GROUPING(region) AS g_region,
               GROUPING(category) AS g_category
        FROM sales_by_region_category
        GROUP BY ROLLUP (region, category)
        ORDER BY g_region, region NULLS LAST, g_category, category NULLS LAST
        """
    ).fetchall()
    con.close()
    return rows


def cube_region_category() -> list[tuple[Any, ...]]:
    """Every dimension combination: detail, per-region, per-category, total."""
    con = _connect()
    rows = con.sql(
        """
        SELECT region, category, ROUND(SUM(sales_amount), 2) AS revenue
        FROM sales_by_region_category
        GROUP BY CUBE (region, category)
        ORDER BY region NULLS LAST, category NULLS LAST
        """
    ).fetchall()
    con.close()
    return rows


def running_total_by_region() -> list[tuple[Any, ...]]:
    """Window function: revenue per region plus a cumulative running total."""
    con = _connect()
    rows = con.sql(
        """
        WITH per_region AS (
            SELECT region, ROUND(SUM(sales_amount), 2) AS revenue
            FROM sales_by_region_category
            GROUP BY region
        )
        SELECT region, revenue,
               SUM(revenue) OVER (ORDER BY region
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                   AS running_total,
               RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
        FROM per_region
        ORDER BY region
        """
    ).fetchall()
    con.close()
    return rows


def materialized_region_revenue() -> dict[str, int]:
    """Pre-aggregate a gold table once, then serve queries from it.

    The pattern behind a materialized view / gold layer: aggregate the large
    fact table a single time, store the small result, query it repeatedly.
    """
    con = _connect()
    con.sql(
        """
        CREATE TABLE gold_region_revenue AS
            SELECT region, ROUND(SUM(sales_amount), 2) AS revenue, COUNT(*) AS line_count
            FROM sales_by_region_category
            GROUP BY region
        """
    )
    gold_rows = con.sql("SELECT COUNT(*) FROM gold_region_revenue").fetchone()[0]
    distinct_regions = con.sql("SELECT COUNT(DISTINCT region) FROM dim_store").fetchone()[0]
    con.close()
    return {"gold_rows": int(gold_rows), "distinct_regions": int(distinct_regions)}


def main() -> None:
    print("ROLLUP (region, category):")
    for row in rollup_region_category():
        print(row)
    print("\nRunning total by region:")
    for row in running_total_by_region():
        print(row)
    print(f"\nMaterialized gold: {materialized_region_revenue()}")


if __name__ == "__main__":
    main()
