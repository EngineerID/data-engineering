"""Module 05 — dimensional modeling on the retail star schema (DuckDB).

Three prove-it concepts, all runnable over `make seed` Parquet with no Docker:

1. **Grain & the fan-out trap** — joining a fact to a dimension at the wrong
   grain double-counts a measure. We prove the correct grain.
2. **SCD Type 2** — a slowly changing dimension keeps history: changed rows are
   expired and a new current version is inserted (`valid_from`/`valid_to`/`is_current`).
3. **Star vs snowflake** — normalizing a dimension trades fewer redundant strings
   for an extra join. We show both return the same revenue.
"""

from __future__ import annotations

from typing import Any

import duckdb

from def_.common.io import parquet_paths

# A subset of customers "change segment" between two snapshots; deterministic so
# tests can assert exact history. Every 7th customer is rotated to the next segment.
SEGMENTS = ["Consumer", "Corporate", "Home Office"]
V0_DATE = "2024-01-01"
V1_DATE = "2024-06-01"


def _connect() -> duckdb.DuckDBPyConnection:
    """In-memory DuckDB with star-schema Parquet registered as views."""
    paths = parquet_paths()
    con = duckdb.connect()
    for name, path in paths.items():
        con.sql(f"CREATE VIEW {name} AS SELECT * FROM read_parquet('{path}/**/*.parquet')")
    return con


# --------------------------------------------------------------------------- #
# 1. Grain & the fan-out trap
# --------------------------------------------------------------------------- #
def fanout_trap() -> dict[str, float]:
    """Show how a wrong-grain join inflates a SUM.

    ``dim_store`` has one row per store, so the join is safe. We *simulate* a
    fan-out by joining to a deliberately duplicated dimension and compare the
    summed measure against the true total.
    """
    con = _connect()
    true_total = con.sql("SELECT SUM(sales_amount) FROM fact_sales").fetchone()[0]

    # A dimension with 2 rows per store (e.g. a careless join to a bridge table)
    # duplicates every fact row, doubling the measure.
    inflated = con.sql(
        """
        WITH dup_store AS (
            SELECT store_key, region FROM dim_store
            UNION ALL
            SELECT store_key, region FROM dim_store
        )
        SELECT SUM(f.sales_amount)
        FROM fact_sales f
        JOIN dup_store d ON f.store_key = d.store_key
        """
    ).fetchone()[0]
    con.close()
    return {"true_total": float(true_total), "inflated_total": float(inflated)}


# --------------------------------------------------------------------------- #
# 2. Slowly Changing Dimension — Type 2
# --------------------------------------------------------------------------- #
def build_scd2() -> duckdb.DuckDBPyConnection:
    """Materialize a Type-2 history table ``scd2_customer`` from two snapshots.

    Returns the live connection so callers/tests can query it.
    """
    con = _connect()
    con.sql(
        f"""
        CREATE TABLE customer_v0 AS
            SELECT customer_key, segment FROM dim_customer;

        CREATE TABLE customer_v1 AS
            SELECT
                customer_key,
                CASE
                    WHEN customer_key % 7 = 0
                    THEN list_value('Consumer','Corporate','Home Office')[
                             (list_position(
                                 list_value('Consumer','Corporate','Home Office'), segment
                             ) % 3) + 1
                         ]
                    ELSE segment
                END AS segment
            FROM customer_v0;

        CREATE TABLE scd2_customer AS
            -- Expired versions: rows whose segment changed between v0 and v1.
            SELECT v0.customer_key, v0.segment,
                   DATE '{V0_DATE}' AS valid_from,
                   DATE '{V1_DATE}' AS valid_to,
                   FALSE AS is_current
            FROM customer_v0 v0
            JOIN customer_v1 v1 USING (customer_key)
            WHERE v0.segment <> v1.segment
            UNION ALL
            -- Current versions: latest value for every customer.
            SELECT customer_key, segment,
                   CASE WHEN customer_key % 7 = 0 THEN DATE '{V1_DATE}'
                        ELSE DATE '{V0_DATE}' END AS valid_from,
                   NULL AS valid_to,
                   TRUE AS is_current
            FROM customer_v1;
        """
    )
    return con


def scd2_stats() -> dict[str, int]:
    """Summary counts a test can assert against."""
    con = build_scd2()
    total_customers = con.sql("SELECT COUNT(*) FROM dim_customer").fetchone()[0]
    current_rows = con.sql("SELECT COUNT(*) FROM scd2_customer WHERE is_current").fetchone()[0]
    versioned = con.sql(
        "SELECT COUNT(*) FROM scd2_customer GROUP BY customer_key HAVING COUNT(*) = 2"
    ).fetchall()
    con.close()
    return {
        "customers": int(total_customers),
        "current_rows": int(current_rows),
        "customers_with_history": len(versioned),
    }


# --------------------------------------------------------------------------- #
# 3. Star vs snowflake
# --------------------------------------------------------------------------- #
def star_category_revenue() -> list[tuple[Any, ...]]:
    """Revenue by product category from the denormalized (star) dimension."""
    con = _connect()
    rows = con.sql(
        """
        SELECT p.category, ROUND(SUM(f.sales_amount), 2) AS revenue
        FROM fact_sales f
        JOIN dim_product p ON f.product_key = p.product_key
        GROUP BY p.category
        ORDER BY p.category
        """
    ).fetchall()
    con.close()
    return rows


def snowflake_category_revenue() -> list[tuple[Any, ...]]:
    """Same revenue, but category lives in a normalized sub-dimension.

    ``dim_product`` is split into ``product`` (key -> category_id) and a
    ``category`` lookup, so the query needs an extra join.
    """
    con = _connect()
    con.sql(
        """
        CREATE TABLE category AS
            SELECT ROW_NUMBER() OVER (ORDER BY category) AS category_id, category
            FROM (SELECT DISTINCT category FROM dim_product);

        CREATE TABLE product_norm AS
            SELECT p.product_key, c.category_id
            FROM dim_product p JOIN category c ON p.category = c.category;
        """
    )
    rows = con.sql(
        """
        SELECT c.category, ROUND(SUM(f.sales_amount), 2) AS revenue
        FROM fact_sales f
        JOIN product_norm p ON f.product_key = p.product_key
        JOIN category c ON p.category_id = c.category_id
        GROUP BY c.category
        ORDER BY c.category
        """
    ).fetchall()
    con.close()
    return rows


def main() -> None:
    trap = fanout_trap()
    print(
        f"fan-out trap: true={trap['true_total']:.2f} "
        f"inflated={trap['inflated_total']:.2f} "
        f"(ratio {trap['inflated_total'] / trap['true_total']:.1f}x)"
    )
    stats = scd2_stats()
    print(f"SCD2: {stats}")
    star = star_category_revenue()
    snow = snowflake_category_revenue()
    print(f"star == snowflake revenue: {star == snow}")
    for row in star:
        print(row)


if __name__ == "__main__":
    main()
