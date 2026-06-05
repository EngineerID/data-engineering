# Data Engineering Foundations

Hands-on repo closing the gap between **analytics delivery** (SQL, BI, warehousing) and **systems internals** (Spark cluster model, SQL tuning, streaming, lakehouse patterns). Graded artifacts are **runnable jobs + passing tests**, not notebooks.

## Commands (WSL/macOS/Linux from repo root; native Windows: `.\tasks.ps1 <target>`)

| Command | Purpose |
|---------|---------|
| `make setup` | `uv sync` + pre-commit hooks |
| `make up` / `make down` | Docker: Spark (1 master, 2 workers), Postgres 16, Kafka KRaft |
| `make up-cloud` / `make down-cloud` | Module 09 cloud emulators (LocalStack/fake-gcs/Azurite) |
| `make seed` | Generate star-schema Parquet (~0.01 GB) |
| `make seed-large` | ~1 GB for shuffle/OOM labs |
| `make load-sql` | Load Parquet into Postgres + apply SQL |
| `make spark-submit JOB=path/to/job.py` | Submit to **standalone cluster** (not `local[*]`) |
| `make oom-lab` | Module 04 OOM exercise (expect failure) |
| `make sql` | psql shell |
| `make lint` / `make typecheck` / `make test` | Quality gates |
| `make test-cloud` | Module 09 roundtrip (`uv sync --extra cloud` + `make up-cloud`) |
| `make check` | lint + typecheck + test |

## Stack

- Python 3.12, **uv**, package `def_` under `src/def_/`
- **ruff**, **mypy** (strict on `src/def_/`), **pytest**
- Local Docker only — no real cloud APIs (Module 09 uses **local emulators**: LocalStack/fake-gcs/Azurite)
- **duckdb** for Module 05 warehousing exercises; **PySpark** on Bitnami Spark 3.5 cluster
- Cloud backends (`fsspec`, `s3fs`, `gcsfs`, `adlfs`) are an optional extra: `uv sync --extra cloud`

## Layout

- `src/def_/common/` — Spark session builder, Postgres DSN, paths (cluster-first)
- `src/def_/datagen/` — Kimball-style retail star schema, `--scale-gb`
- `modules/NN_*/` — learning units 01–09; exercises + tests in-module
- `src/def_/common/storage.py` — multi-cloud fsspec abstraction (Module 09)
- `docs/curriculum.md` — committed curriculum and reading lists
- `references/` — **gitignored** optional local textbook extracts only; never commit
- `data/` — **gitignored** generated Parquet and explain artifacts

## Principles

1. **Real cluster over notebooks** — Spark jobs via `spark-submit` against `spark://localhost:7077`; inspect UI :8080 (cluster) and :4040 (app).
2. **Prove it** — Every exercise has pytest acceptance criteria; integration tests skip when Docker is down.
3. **Typed `src/`** — Fully annotated; `make typecheck` must pass before done.
4. **Copyright** — Paraphrase concepts in READMEs; cite as *Book — Chapter N*; never paste long verbatim text from `references/`.

## Spark session

Use `def_.common.spark.build_spark_session(name, cluster=True)` for graded jobs. Do not default to `local[*]` except isolated unit tests.

## Environment

Copy `.env.example` → `.env`. Defaults match `infra/docker-compose.yml` (`def_user` / `def_learning`).

## Module status

- **Built:** 02 SQL, 04 Spark, 05 warehousing (SCD2/OLAP), 09 cloud portability, datagen, infra, agent files (07)
- **Light:** 01 Python, 03 BI notes, 06 Kafka roundtrip, 08 medallion pipeline

## UIs

- Spark master: http://localhost:8080
- Spark application: http://localhost:4040 (while a job runs)
