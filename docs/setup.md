# Environment setup

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Compose
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/) (recommended on Windows)
- [uv](https://docs.astral.sh/uv/) (Python 3.12)

## Where to run commands

Run from the **repository root** in WSL (e.g. `/mnt/c/GitHub/data-engineering`). Paths like `modules/` and `src/` assume the root as the working directory.

**Windows without WSL:**

```powershell
py -3.12 -m uv sync --all-groups
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m pytest
```

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
- `make test` — pytest (skips Spark integration by default)
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
