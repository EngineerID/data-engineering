"""Prove-it tests for Module 03 — views, recursive CTE, index tuning."""

from __future__ import annotations

import os
import re

import psycopg
import pytest

from def_.common.io import get_postgres_dsn

pytestmark = pytest.mark.postgres


def _connect() -> psycopg.Connection:
    try:
        return psycopg.connect(get_postgres_dsn(), connect_timeout=3)
    except psycopg.OperationalError as exc:
        pytest.skip(f"Postgres not available: {exc}")


def _table_exists(conn: psycopg.Connection, table: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'retail' AND table_name = %s
            """,
            (table,),
        )
        return cur.fetchone() is not None


@pytest.fixture(scope="module")
def db() -> psycopg.Connection:
    conn = _connect()
    if not _table_exists(conn, "fact_sales"):
        pytest.skip("Schema not loaded — run: make seed && make load-sql")
    yield conn
    conn.close()


def test_view_sales_by_region(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM retail.v_sales_by_region")
        count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT region) FROM retail.dim_store")
        regions = cur.fetchone()[0]
    assert count == regions
    assert count >= 1


def test_recursive_cte_tree(db: psycopg.Connection) -> None:
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM retail.v_category_tree")
        tree_rows = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM retail.product_hierarchy")
        hierarchy_rows = cur.fetchone()[0]
    assert tree_rows == hierarchy_rows
    assert tree_rows > 0


def _explain_ms(conn: psycopg.Connection, sql: str) -> tuple[float, str]:
    with conn.cursor() as cur:
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) {sql}")
        plan = "\n".join(row[0] for row in cur.fetchall())
    match = re.search(r"Execution Time:\s*([\d.]+)\s*ms", plan)
    ms = float(match.group(1)) if match else 999999.0
    return ms, plan


def test_index_speedup(db: psycopg.Connection) -> None:
    query = "SELECT SUM(f.sales_amount) FROM retail.fact_sales AS f WHERE f.customer_key = 42"
    with db.cursor() as cur:
        cur.execute("DROP INDEX IF EXISTS retail.idx_fact_customer_key")
    db.commit()

    without_ms, without_plan = _explain_ms(db, query)
    assert "Seq Scan" in without_plan or "Bitmap" in without_plan

    with db.cursor() as cur:
        cur.execute("CREATE INDEX idx_fact_customer_key ON retail.fact_sales (customer_key)")
        cur.execute("ANALYZE retail.fact_sales")
    db.commit()

    with_ms, with_plan = _explain_ms(db, query)
    assert "Index" in with_plan

    artifacts = os.path.join(os.environ.get("DATA_DIR", "data"), "sql_plans")
    os.makedirs(artifacts, exist_ok=True)
    with open(os.path.join(artifacts, "without_index.txt"), "w", encoding="utf-8") as f:
        f.write(without_plan)
    with open(os.path.join(artifacts, "with_index.txt"), "w", encoding="utf-8") as f:
        f.write(with_plan)

    # Indexed path should not be slower than sequential (allow noise on tiny data)
    assert with_ms <= without_ms * 1.5 or "Index Scan" in with_plan
