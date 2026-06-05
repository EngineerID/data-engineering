# Module 09 — Cloud Object Storage & Portability (AWS · GCP · Azure)

**Status:** built · **Covers:** the cloud layer. Most data-engineering roles assume
at least one cloud, but the rest of this repo is deliberately local. This module
teaches the **portable layer** — object storage and a single storage abstraction —
for all three major clouds **without spend or credentials**, using local emulators
that honor the repo's "local Docker only" rule.

## The idea

A data engineer writes against *one* storage interface and swaps clouds by
**configuration, not code**. `src/def_/common/storage.py` returns an
[`fsspec`](https://filesystem-spec.readthedocs.io/) filesystem for `aws`, `gcp`,
or `azure`; the same `object_store_roundtrip.py` job writes and reads a gold
Parquet table to whichever you pick.

| Cloud | Service | Emulator | Endpoint | fsspec backend |
|---|---|---|---|---|
| `aws` | S3 | LocalStack | `http://localhost:4566` | `s3fs` |
| `gcp` | Cloud Storage | fake-gcs-server | `http://localhost:4443` | `gcsfs` |
| `azure` | Blob / ADLS Gen2 | Azurite | `http://localhost:10000` | `adlfs` |

## What's in this folder

- `object_store_roundtrip.py` — write/read a region-revenue gold table to a cloud
- `concepts.md` — object storage vs HDFS, IAM, egress, table formats across clouds
- `tests/test_cloud_storage.py` — offline config tests + `-m cloud` roundtrip tests

## Infrastructure

Docker emulator services in [`infra/docker-compose.yml`](../../infra/docker-compose.yml):
`localstack`, `fake-gcs`, `azurite`. They are in the optional `cloud` Compose
profile, so plain `make up` does **not** start them.

## Setup

Install the optional cloud backends once:

```bash
uv sync --extra cloud      # adds fsspec, s3fs, gcsfs, adlfs
```

## Run

**WSL / macOS / Linux:**

```bash
make seed
make up-cloud                                  # start the three emulators
uv run python modules/09_cloud_portability/object_store_roundtrip.py --cloud aws
uv run python modules/09_cloud_portability/object_store_roundtrip.py --cloud gcp
uv run python modules/09_cloud_portability/object_store_roundtrip.py --cloud azure
uv run pytest modules/09_cloud_portability/tests -m cloud
make down-cloud
```

**Windows (native)** — see [`docs/setup.md`](../../docs/setup.md):

```powershell
.\tasks.ps1 seed
.\tasks.ps1 up-cloud
.\.venv\Scripts\python.exe modules\09_cloud_portability\object_store_roundtrip.py --cloud aws
.\tasks.ps1 test-cloud
.\tasks.ps1 down-cloud
```

The **offline** config tests need no Docker and run with the normal suite:

```bash
uv run pytest modules/09_cloud_portability/tests
```

## Prove-it exercises

1. **One interface, three clouds** — run the roundtrip against `aws`, `gcp`, and
   `azure`. Acceptance: each prints `rows_roundtripped=4` (one row per region)
   with no change to the job code.
2. **Config, not code** — `storage_config()` returns the right endpoint per cloud
   and rejects unknown clouds. Acceptance: offline tests pass.
3. **Portability write-up** — extend `concepts.md`: where does the abstraction
   leak (consistency, IAM, ADLS hierarchical namespace, egress cost)?

## Further reading

[`docs/curriculum.md` — Repo module 09](../../docs/curriculum.md#repo-module-09--cloud--object-storage-portability)
