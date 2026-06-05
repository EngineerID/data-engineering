"""Prove-it tests for Module 08 — Delta-style table semantics on DuckDB."""

from __future__ import annotations

import sys
from pathlib import Path

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import table_format_lab  # noqa: E402


def test_idempotent_merge() -> None:
    result = table_format_lab.idempotent_merge_demo()
    assert result["rows_after_first"] == 3
    assert result["idempotent"] is True
    assert result["rows_after_first"] == result["rows_after_second"]


def test_schema_enforcement_rejects_bad_type() -> None:
    result = table_format_lab.schema_enforcement_demo()
    assert result["bad_write_rejected"] is True
    assert result["table_uncorrupted"] is True


def test_schema_evolution_add_column() -> None:
    result = table_format_lab.schema_evolution_demo()
    assert result["old_reader_still_works"] is True
    assert result["old_rows_null_for_new_col"] is True
    assert result["new_rows_carry_value"] is True


def test_time_travel_recovers_bad_write() -> None:
    result = table_format_lab.time_travel_demo()
    assert result["bad_total"] == 0
    assert result["recovered_to_good"] is True
    assert result["recovered_total"] == result["good_total"] == 300
