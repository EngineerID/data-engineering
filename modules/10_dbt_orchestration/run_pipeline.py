"""Module 10 — orchestrate the dbt transformation DAG and emit a data catalog.

This is a minimal orchestrator: in production the same ordered steps (seed →
build → test → document) are scheduled by Airflow / Dagster / a GitLab CI job.
Here we drive them in-process so the whole lab runs locally on DuckDB with no
warehouse and no Docker.

Steps:
  1. ``dbt build``   — run staging + mart models AND their data-quality tests
                       (uniqueness, not-null, referential integrity).
  2. ``dbt docs generate`` — produce ``manifest.json`` + ``catalog.json``: the
                       metadata a **data catalog** is built from (models, columns,
                       descriptions, and the lineage graph).
  3. Summarize the catalog/lineage and the gold mart.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import duckdb

from def_.common.io import data_dir
from def_.common.logging import get_logger

logger = get_logger(__name__)

PROJECT_DIR = Path(__file__).resolve().parent / "dbt_project"


def _duckdb_path() -> Path:
    path = data_dir() / "dbt" / "def.duckdb"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _dbt_args(*command: str) -> list[str]:
    """Build dbt CLI args: subcommands first, then shared options."""
    parquet_dir = str(data_dir() / "parquet")
    return [
        *command,
        "--project-dir",
        str(PROJECT_DIR),
        "--profiles-dir",
        str(PROJECT_DIR),
        "--vars",
        json.dumps({"parquet_dir": parquet_dir}),
    ]


def _invoke(*command: str) -> Any:
    from dbt.cli.main import dbtRunner

    os.environ["DBT_DUCKDB_PATH"] = str(_duckdb_path())
    result = dbtRunner().invoke(_dbt_args(*command))
    if not result.success:
        joined = " ".join(command)
        raise RuntimeError(f"dbt {joined} failed: {result.exception or 'see logs above'}")
    return result


def catalog_summary() -> dict[str, Any]:
    """Read dbt's manifest/catalog metadata into a compact summary."""
    manifest = json.loads((PROJECT_DIR / "target" / "manifest.json").read_text("utf-8"))
    nodes = manifest["nodes"]
    models = [k for k, v in nodes.items() if v["resource_type"] == "model"]
    tests = [k for k, v in nodes.items() if v["resource_type"] == "test"]
    sources = list(manifest.get("sources", {}).keys())
    # parent_map encodes lineage edges (node -> its upstream dependencies).
    lineage_edges = sum(len(parents) for parents in manifest["parent_map"].values())
    return {
        "models": len(models),
        "tests": len(tests),
        "sources": len(sources),
        "lineage_edges": lineage_edges,
    }


def run() -> dict[str, Any]:
    _invoke("build")
    _invoke("docs", "generate")

    summary = catalog_summary()

    con = duckdb.connect(str(_duckdb_path()))
    regions = con.sql("SELECT COUNT(*) FROM main.mart_regional_revenue").fetchone()[0]
    con.close()
    summary["mart_regional_revenue_rows"] = int(regions)

    out = data_dir() / "dbt" / "catalog_summary.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    summary["catalog_summary_path"] = str(out)
    return summary


def main() -> None:
    stats = run()
    logger.info("dbt pipeline complete: %s", stats)
    print(stats)


if __name__ == "__main__":
    main()
