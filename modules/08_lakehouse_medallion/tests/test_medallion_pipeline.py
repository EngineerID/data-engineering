"""Prove-it tests for Module 08 — medallion pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from def_.common.io import data_dir, parquet_paths

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import medallion_pipeline  # noqa: E402

DELTA_CONCEPTS = _MODULE_DIR / "delta_concepts.md"


def _parquet_ready() -> bool:
    return bool(list(parquet_paths()["fact_sales"].glob("**/*.parquet")))


@pytest.fixture(scope="module")
def pipeline_stats() -> dict[str, int | str]:
    if not _parquet_ready():
        pytest.skip("Parquet missing — run: make seed")
    return medallion_pipeline.run_pipeline()


def test_medallion_layers_exist(pipeline_stats: dict[str, int | str]) -> None:
    root = data_dir() / "medallion"
    assert (root / "bronze" / "fact_sales").exists()
    assert (root / "silver" / "fact_sales.parquet").exists()
    assert (root / "gold" / "regional_revenue.parquet").exists()
    assert pipeline_stats["bronze_rows"] > 0
    assert pipeline_stats["silver_rows"] > 0
    assert pipeline_stats["gold_rows"] > 0


def test_lineage_json(pipeline_stats: dict[str, int | str]) -> None:
    lineage_path = Path(str(pipeline_stats["lineage_path"]))
    data = json.loads(lineage_path.read_text(encoding="utf-8"))
    assert data["layers"] == ["bronze", "silver", "gold"]
    assert "timestamp" in data
    assert data["silver_rows"] <= data["bronze_rows"]


def test_delta_concepts_structure() -> None:
    text = DELTA_CONCEPTS.read_text(encoding="utf-8")
    for heading in ("## ACID on object storage", "## Time travel", "## Schema evolution"):
        assert heading in text
    assert len(text.strip()) > 200
