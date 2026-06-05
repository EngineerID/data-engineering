"""Prove-it tests for Module 02 — views, recursive CTE, index tuning."""

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


def test_top_n_per_region(db: psycopg.Connection) -> None:
    """Window pattern: at most 3 products per region, ranked 1..3 by revenue."""
    with db.cursor() as cur:
        cur.execute(
            "SELECT region, COUNT(*), MAX(rn) FROM retail.v_top_products_per_region GROUP BY region"
        )
        rows = cur.fetchall()
    assert rows, "expected at least one region"
    for _region, n, max_rn in rows:
        assert n <= 3
        assert max_rn <= 3


def test_monthly_running_total_is_cumulative(db: psycopg.Connection) -> None:
    """LAG + windowed SUM: running_total never decreases (revenue is positive)."""
    with db.cursor() as cur:
        cur.execute("SELECT running_total FROM retail.v_monthly_revenue ORDER BY year, month")
        totals = [float(r[0]) for r in cur.fetchall()]
    assert len(totals) >= 1
    assert all(b >= a for a, b in zip(totals, totals[1:], strict=False))


def test_dedup_keeps_latest(db: psycopg.Connection) -> None:
    """ROW_NUMBER dedup keeps the most recent row per email."""
    with db.cursor() as cur:
        cur.execute(
            "SELECT full_name FROM retail.v_customer_emails_deduped WHERE email = 'a@example.com'"
        )
        name = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM retail.v_customer_emails_deduped")
        n = cur.fetchone()[0]
    assert name == "Ann New"
    assert n == 2  # two distinct emails after dedup


def test_trigger_wrote_audit_log(db: psycopg.Connection) -> None:
    """The AFTER UPDATE trigger populated audit_log when the script bumped targets."""
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM retail.audit_log WHERE table_name = 'kpi_targets'")
        assert cur.fetchone()[0] > 0


def test_stored_procedure_is_idempotent(db: psycopg.Connection) -> None:
    """Re-running the refresh procedure rebuilds the same row set (no duplicates)."""
    with db.cursor() as cur:
        cur.execute("CALL retail.refresh_regional_kpi()")
        cur.execute("SELECT COUNT(*) FROM retail.gold_regional_kpi")
        first = cur.fetchone()[0]
        cur.execute("CALL retail.refresh_regional_kpi()")
        cur.execute("SELECT COUNT(*) FROM retail.gold_regional_kpi")
        second = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT region) FROM retail.dim_store")
        regions = cur.fetchone()[0]
    db.commit()
    assert first == second == regions


def test_upsert_is_idempotent(db: psycopg.Connection) -> None:
    """ON CONFLICT upsert: a second run changes no row count (idempotent MERGE)."""
    with db.cursor() as cur:
        cur.execute("CALL retail.upsert_gold_kpi()")
        cur.execute("SELECT COUNT(*) FROM retail.gold_kpi")
        first = cur.fetchone()[0]
        cur.execute("CALL retail.upsert_gold_kpi()")
        cur.execute("SELECT COUNT(*) FROM retail.gold_kpi")
        second = cur.fetchone()[0]
    db.commit()
    assert first == second
    assert first > 0


def test_row_level_security_isolates_tenant(db: psycopg.Connection) -> None:
    """Under a non-superuser role, RLS shows only the session's tenant rows."""
    with db.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM pg_policies "
            "WHERE schemaname='retail' AND tablename='tenant_metrics' "
            "AND policyname='tenant_isolation'"
        )
        assert cur.fetchone() is not None, "RLS policy not registered"

        cur.execute("SET ROLE retail_app")
        cur.execute("SET app.tenant_id = 'hk'")
        cur.execute("SELECT DISTINCT tenant_id FROM retail.tenant_metrics")
        visible = sorted(r[0] for r in cur.fetchall())
        cur.execute("RESET ROLE")
    db.rollback()
    assert visible == ["hk"], f"RLS leak: saw {visible}"
