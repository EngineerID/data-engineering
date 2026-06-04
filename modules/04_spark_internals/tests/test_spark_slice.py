"""Prove-it tests for Module 04 — Spark cluster integration."""

from __future__ import annotations

import os
import socket
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
EXPLAIN_FILE = Path(os.environ.get("DATA_DIR", "data")) / "explain" / "join_aggregate.txt"


def _spark_master_reachable() -> bool:
    host = os.environ.get("SPARK_MASTER_HOST", "localhost")
    port = int(os.environ.get("SPARK_MASTER_PORT", "7077"))
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False


@pytest.mark.spark
def test_explain_artifact_after_submit() -> None:
    if not _spark_master_reachable():
        pytest.skip("Spark master not reachable — run: make up")

    job = REPO_ROOT / "modules" / "04_spark_internals" / "join_aggregate_job.py"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["SPARK_MASTER_URL"] = os.environ.get("SPARK_MASTER_URL", "spark://localhost:7077")

    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            "infra/docker-compose.yml",
            "exec",
            "-T",
            "-e",
            "PYTHONPATH=/workspace/src",
            "spark-master",
            "spark-submit",
            "--master",
            "spark://spark-master:7077",
            "--deploy-mode",
            "client",
            "--conf",
            "spark.driver.host=spark-master",
            "--conf",
            "spark.driver.bindAddress=0.0.0.0",
            f"/workspace/{job.relative_to(REPO_ROOT).as_posix()}",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail(f"spark-submit failed:\n{result.stderr}\n{result.stdout}")

    assert EXPLAIN_FILE.exists(), "Run join_aggregate_job to produce explain file"
    content = EXPLAIN_FILE.read_text(encoding="utf-8")
    assert len(content) > 50
    assert any(kw in content.lower() for kw in ("shuffle", "exchange", "aggregate", "join"))


def test_explain_file_exists_or_skip() -> None:
    """Fast check when explain artifact already present from manual run."""
    if EXPLAIN_FILE.exists():
        assert (
            "Physical Plan" in EXPLAIN_FILE.read_text(encoding="utf-8")
            or len(EXPLAIN_FILE.read_text(encoding="utf-8")) > 100
        )
    elif not _spark_master_reachable():
        pytest.skip("No explain file and Spark not up")
