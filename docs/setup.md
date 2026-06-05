# Environment setup

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Compose
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/) (recommended on Windows)
- [uv](https://docs.astral.sh/uv/) (Python 3.12)

## Where to run commands

Run from the **repository root** in WSL (e.g. `/mnt/c/GitHub/data-engineering`). Paths like `modules/` and `src/` assume the root as the working directory.

## Native Windows (no WSL)

WSL is **not required**. Use the bundled PowerShell task runner [`tasks.ps1`](../tasks.ps1),
which mirrors the Makefile targets against the local `.venv` and Docker Desktop:

```powershell
Copy-Item .env.example .env
.\tasks.ps1 setup        # uv sync if uv is present, else pip install -e .[dev] into .venv
.\tasks.ps1 up           # Docker services (needs Docker Desktop running)
.\tasks.ps1 seed
.\tasks.ps1 test
.\tasks.ps1 check
```

Available tasks: `setup up down up-cloud down-cloud seed seed-large load-sql lint
typecheck test test-cloud check spark-submit <job> oom-lab`.

If you prefer raw commands, the venv interpreter works directly:

```powershell
$env:PYTHONPATH = "src;."
.\.venv\Scripts\python.exe -m pytest -m "not spark and not kafka and not cloud"
```

> **Note:** `make`, `psql`, and `spark-submit` are not on the Windows PATH — they
> run inside WSL or the Docker containers. The PowerShell tasks above invoke the
> containerized `spark-submit` for you.

## First-time setup

```bash
cp .env.example .env
make setup    # uv sync + pre-commit
make up       # Docker services (see infra/)
make seed     # star-schema Parquet under data/
```

## Docker (`infra/`)

Compose file: [`infra/docker-compose.yml`](../infra/docker-compose.yml). The Makefile wraps:

```bash
make up       # start Postgres, Spark (1 master + 2 workers), Kafka
make down     # stop all services
```

- **Postgres** `5432` — module 02 SQL
- **Spark master UI** `8080` — module 04 Spark
- **Spark app UI** `4040` — module 04 (while a job runs)
- **Spark master RPC** `7077` — module 04 Spark
- **Kafka** `9092` — module 06 streaming (light)

Cloud emulators (module 09) start under a separate profile and are **not** part of `make up`:

```bash
make up-cloud      # LocalStack (S3 :4566), fake-gcs (:4443), Azurite (:10000)
make down-cloud
```

Details: [`infra/README.md`](../infra/README.md).

## Shared data (`make seed`)

[`src/def_/datagen/`](../src/def_/datagen/) generates Kimball-style retail Parquet. Module 02 loads it into Postgres; module 04 reads it from Spark.

```bash
make seed         # ~0.01 GB
make seed-large   # ~1 GB (shuffle / spill practice)
```

## Light module tests (01, 03, 05, 06, 08)

```bash
uv run pytest modules/01_python_model/tests modules/03_bi_tools/tests
make seed
uv run pytest modules/05_warehousing/tests modules/08_lakehouse_medallion/tests
make up
uv run pytest modules/06_streaming_kafka/tests -m kafka
```

## Common commands

- `make load-sql` — load Parquet into Postgres + SQL scripts (module 02)
- `make sql` — `psql` shell
- `make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py` — standalone Spark cluster
- `make oom-lab` — module 04 OOM exercise (expect failure)
- `make test` — pytest (skips Spark/Kafka/cloud integration by default)
- `make test-cloud` — module 09 cloud roundtrip (needs `make up-cloud` + `uv sync --extra cloud`)
- `make check` — lint + typecheck + test

## Quickstart (full path)

```bash
cp .env.example .env
make setup
make up
make seed
make load-sql
make test
make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py
make check
```

Next: pick a module from [`modules.md`](modules.md) or [`modules/README.md`](../modules/README.md).
