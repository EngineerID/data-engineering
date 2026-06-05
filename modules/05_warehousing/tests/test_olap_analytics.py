"""Prove-it tests for Module 05 — OLAP aggregation patterns."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from def_.common.io import parquet_paths

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import olap_analytics as olap  # noqa: E402


def _parquet_ready() -> bool:
    paths = parquet_paths()
    return bool(
        list(paths["fact_sales"].glob("**/*.parquet"))
        and list(paths["dim_store"].glob("**/*.parquet"))
    )


@pytest.fixture(scope="module", autouse=True)
def require_seed() -> None:
    if not _parquet_ready():
        pytest.skip("Parquet missing — run: make seed")


def test_rollup_has_grand_total_row() -> None:
    rows = olap.rollup_region_category()
    # Exactly one grand-total row: GROUPING(region)=1 and GROUPING(category)=1.
    grand = [r for r in rows if r[3] == 1 and r[4] == 1]
    assert len(grand) == 1


def test_rollup_grand_total_equals_sum_of_details() -> None:
    rows = olap.rollup_region_category()
    grand_total = next(r[2] for r in rows if r[3] == 1 and r[4] == 1)
    detail_sum = sum(r[2] for r in rows if r[3] == 0 and r[4] == 0)
    assert grand_total == pytest.approx(detail_sum, rel=1e-6)


def test_running_total_is_monotonic_and_ends_at_total() -> None:
    rows = olap.running_total_by_region()
    running = [r[2] for r in rows]
    assert running == sorted(running)  # cumulative => non-decreasing
    assert running[-1] == pytest.approx(sum(r[1] for r in rows), rel=1e-6)


def test_materialized_gold_one_row_per_region() -> None:
    stats = olap.materialized_region_revenue()
    assert stats["gold_rows"] == stats["distinct_regions"]
