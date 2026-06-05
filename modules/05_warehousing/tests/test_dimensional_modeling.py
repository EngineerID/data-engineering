"""Prove-it tests for Module 05 — dimensional modeling."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from def_.common.io import parquet_paths

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import dimensional_modeling as dm  # noqa: E402


def _parquet_ready() -> bool:
    paths = parquet_paths()
    return bool(
        list(paths["fact_sales"].glob("**/*.parquet"))
        and list(paths["dim_customer"].glob("**/*.parquet"))
    )


@pytest.fixture(scope="module", autouse=True)
def require_seed() -> None:
    if not _parquet_ready():
        pytest.skip("Parquet missing — run: make seed")


def test_fanout_trap_doubles_measure() -> None:
    trap = dm.fanout_trap()
    # A 2x duplicated dimension exactly doubles the summed measure.
    assert trap["inflated_total"] == pytest.approx(trap["true_total"] * 2, rel=1e-9)


def test_scd2_keeps_one_current_row_per_customer() -> None:
    stats = dm.scd2_stats()
    assert stats["current_rows"] == stats["customers"]


def test_scd2_versions_changed_customers() -> None:
    stats = dm.scd2_stats()
    # Every 7th customer rotates segment, so it gets a second (historical) row.
    assert stats["customers_with_history"] == stats["customers"] // 7


def test_star_and_snowflake_agree() -> None:
    assert dm.star_category_revenue() == dm.snowflake_category_revenue()
