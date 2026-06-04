"""Prove-it tests for Module 05 — DuckDB warehousing."""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pytest

from def_.common.io import parquet_paths

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import query_star_schema  # noqa: E402


def _parquet_ready() -> bool:
    paths = parquet_paths()
    fact_files = list(paths["fact_sales"].glob("**/*.parquet"))
    store_files = list(paths["dim_store"].glob("**/*.parquet"))
    return bool(fact_files and store_files)


@pytest.fixture(scope="module")
def require_seed() -> None:
    if not _parquet_ready():
        pytest.skip("Parquet missing — run: make seed")


def test_fact_sales_has_rows(require_seed: None) -> None:
    fact = parquet_paths()["fact_sales"]
    con = duckdb.connect()
    count = con.sql(f"SELECT COUNT(*) FROM read_parquet('{fact}/**/*.parquet')").fetchone()[0]
    assert count > 0


def test_regional_aggregate_grain(require_seed: None) -> None:
    paths = parquet_paths()
    store = paths["dim_store"]
    con = duckdb.connect()
    regions = con.sql(
        f"SELECT COUNT(DISTINCT region) FROM read_parquet('{store}/**/*.parquet')"
    ).fetchone()[0]
    rows = query_star_schema.regional_sales_aggregate().fetchall()
    assert len(rows) == regions
    assert all(row[1] is not None for row in rows)
