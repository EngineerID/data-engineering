"""Top-level integration smoke tests."""

from __future__ import annotations

from pathlib import Path

from def_.common.io import data_dir, parquet_paths
from def_.datagen.cli import estimate_fact_rows, generate


def test_estimate_fact_rows_positive() -> None:
    assert estimate_fact_rows(0.01) >= 1000


def test_generate_tiny_dataset() -> None:
    root = generate(0.001)
    paths = parquet_paths()
    assert root == data_dir()
    for name, path in paths.items():
        assert path.exists(), f"Missing {name}"
        parquet_files = list(path.glob("**/*.parquet"))
        assert parquet_files, f"No parquet in {name}"


def test_parquet_paths_under_data() -> None:
    base = data_dir()
    assert "parquet" in str(base) or base.name == "data" or Path("data") in base.parents
