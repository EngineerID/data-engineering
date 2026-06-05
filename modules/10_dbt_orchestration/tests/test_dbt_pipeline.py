"""Prove-it tests for Module 10 — dbt transformations, tests, and catalog.

Marked ``dbt``: requires the optional dbt extra (`uv sync --extra dbt`) and seeded
Parquet. Runs locally on DuckDB — no Docker. Skips cleanly when either is absent.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from def_.common.io import parquet_paths

pytest.importorskip("dbt", reason="dbt not installed — run: uv sync --extra dbt")

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import run_pipeline  # noqa: E402

pytestmark = pytest.mark.dbt


def _parquet_ready() -> bool:
    return bool(list(parquet_paths()["fact_sales"].glob("**/*.parquet")))


@pytest.fixture(scope="module")
def stats() -> dict[str, object]:
    if not _parquet_ready():
        pytest.skip("Parquet missing — run: make seed")
    return run_pipeline.run()


def test_models_and_tests_built(stats: dict[str, object]) -> None:
    # build runs every model and every data-quality test; run() raises if any fail.
    assert stats["models"] == 4
    assert stats["tests"] >= 10  # not_null / unique / relationships across the model


def test_catalog_metadata_emitted(stats: dict[str, object]) -> None:
    # dbt docs generate -> manifest.json + catalog.json, the data-catalog metadata.
    assert stats["sources"] == 5
    assert stats["lineage_edges"] > 0
    assert (run_pipeline.PROJECT_DIR / "target" / "catalog.json").exists()
    assert (run_pipeline.PROJECT_DIR / "target" / "manifest.json").exists()


def test_gold_mart_one_row_per_region(stats: dict[str, object]) -> None:
    assert stats["mart_regional_revenue_rows"] == 4
