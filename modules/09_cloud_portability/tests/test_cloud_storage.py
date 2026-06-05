"""Prove-it tests for Module 09 — cloud object-storage portability.

The config-builder tests run offline (no Docker, no backends). The roundtrip
tests are marked ``cloud`` and skip unless the corresponding emulator is up
(`make up-cloud`) and the optional backend is installed.
"""

from __future__ import annotations

import socket
import sys
from pathlib import Path
from urllib.parse import urlparse

import pytest

from def_.common import storage

_MODULE_DIR = Path(__file__).resolve().parents[1]
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))


# --------------------------------------------------------------------------- #
# Offline: the config builder is pure and always testable.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("cloud", storage.CLOUDS)
def test_storage_config_has_endpoint(cloud: storage.Cloud) -> None:
    cfg = storage.storage_config(cloud)
    assert cfg["endpoint"].startswith("http")
    assert isinstance(cfg["kwargs"], dict)


def test_storage_config_rejects_unknown_cloud() -> None:
    with pytest.raises(ValueError, match="unknown cloud"):
        storage.storage_config("oracle")  # type: ignore[arg-type]


def test_azurite_connection_string_uses_dev_account() -> None:
    conn = storage.azurite_connection_string()
    assert "AccountName=devstoreaccount1" in conn
    assert "BlobEndpoint=" in conn


# --------------------------------------------------------------------------- #
# Integration: requires the emulator + backend. Skips cleanly otherwise.
# --------------------------------------------------------------------------- #
def _reachable(endpoint: str) -> bool:
    parsed = urlparse(endpoint)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False


@pytest.mark.cloud
@pytest.mark.parametrize("cloud", storage.CLOUDS)
def test_object_store_roundtrip(cloud: storage.Cloud) -> None:
    cfg = storage.storage_config(cloud)
    if not _reachable(cfg["endpoint"]):
        pytest.skip(f"{cloud} emulator not reachable at {cfg['endpoint']} — run: make up-cloud")
    pytest.importorskip(
        {"aws": "s3fs", "gcp": "gcsfs", "azure": "adlfs"}[cloud],
        reason="cloud backend not installed — run: uv sync --extra cloud",
    )
    import object_store_roundtrip as job  # noqa: E402

    rows = job.roundtrip(cloud, bucket=f"def-test-{cloud}")
    assert rows == 4  # one row per region
