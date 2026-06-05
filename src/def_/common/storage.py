"""Multi-cloud object-storage abstraction (AWS / GCP / Azure) via fsspec.

The teaching point of Module 09: a data engineer writes against *one* storage
interface and swaps clouds by configuration, not code. We target three **local
emulators** so the repo keeps its "local Docker only — no cloud APIs, no spend,
no credentials" rule while still exercising real S3/Blob/GCS client paths:

- ``aws`` — S3 · LocalStack · http://localhost:4566
- ``gcp`` — Cloud Storage · fake-gcs-server · http://localhost:4443
- ``azure`` — Blob / ADLS Gen2 · Azurite · http://localhost:10000

Backends (``s3fs``, ``gcsfs``, ``adlfs``) are in the optional ``cloud`` group and
imported lazily, so the base install and ``mypy`` do not require them.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:  # pragma: no cover - typing only
    from fsspec import AbstractFileSystem

Cloud = Literal["aws", "gcp", "azure"]
CLOUDS: tuple[Cloud, ...] = ("aws", "gcp", "azure")

# Azurite ships a fixed well-known development account. Safe to commit: it only
# ever authenticates against the local emulator, never a real Azure account.
AZURITE_ACCOUNT = "devstoreaccount1"
AZURITE_KEY = (
    "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
)


def _endpoint(cloud: Cloud) -> str:
    return {
        "aws": os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566"),
        "gcp": os.environ.get("GCS_ENDPOINT_URL", "http://localhost:4443"),
        "azure": os.environ.get("AZURITE_BLOB_URL", "http://127.0.0.1:10000"),
    }[cloud]


def azurite_connection_string() -> str:
    blob_endpoint = f"{_endpoint('azure')}/{AZURITE_ACCOUNT}"
    return (
        "DefaultEndpointsProtocol=http;"
        f"AccountName={AZURITE_ACCOUNT};"
        f"AccountKey={AZURITE_KEY};"
        f"BlobEndpoint={blob_endpoint};"
    )


def storage_config(cloud: Cloud) -> dict[str, Any]:
    """Return the connection settings for a cloud's emulator (pure / testable).

    No network or imports happen here, so this is unit-tested offline.
    """
    if cloud not in CLOUDS:
        raise ValueError(f"unknown cloud {cloud!r}; expected one of {CLOUDS}")
    endpoint = _endpoint(cloud)
    if cloud == "aws":
        # Note: we deliberately do NOT pass region_name. s3fs would then send a
        # CreateBucketConfiguration/LocationConstraint that LocalStack rejects for
        # the us-east-1 default ("InvalidLocationConstraint"). Omitting it keeps
        # bucket creation working against the emulator.
        return {
            "endpoint": endpoint,
            "kwargs": {
                "key": os.environ.get("AWS_ACCESS_KEY_ID", "test"),
                "secret": os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
                "client_kwargs": {"endpoint_url": endpoint},
            },
        }
    if cloud == "gcp":
        return {
            "endpoint": endpoint,
            "kwargs": {
                "project": os.environ.get("GCP_PROJECT", "def-local"),
                "token": "anon",
                "endpoint_url": endpoint,
            },
        }
    return {
        "endpoint": endpoint,
        "kwargs": {"connection_string": azurite_connection_string()},
    }


def get_filesystem(cloud: Cloud) -> AbstractFileSystem:
    """Build an fsspec filesystem pointed at the local emulator for ``cloud``.

    Lazily imports the backend so a missing optional dependency raises a clear,
    actionable error instead of failing at module import time.
    """
    cfg = storage_config(cloud)
    try:
        if cloud == "aws":
            import s3fs

            return s3fs.S3FileSystem(**cfg["kwargs"])
        if cloud == "gcp":
            # fake-gcs-server also honors this env var for client libraries.
            os.environ.setdefault("STORAGE_EMULATOR_HOST", cfg["endpoint"])
            import gcsfs

            return gcsfs.GCSFileSystem(**cfg["kwargs"])
        import adlfs

        return adlfs.AzureBlobFileSystem(**cfg["kwargs"])
    except ImportError as exc:  # pragma: no cover - exercised only without extras
        raise ImportError(
            f"cloud backend for {cloud!r} not installed. "
            "Install the optional extras: `uv sync --extra cloud`"
        ) from exc
