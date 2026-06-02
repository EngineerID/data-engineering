# Data Engineering Foundations

Hands-on repo closing the gap between governance/medallion fluency and **systems internals** (Spark cluster model, SQL foundations, tuning). Graded artifacts are **runnable jobs + passing tests**, not notebooks.

## Commands (run from WSL at repo root)

| Command | Purpose |
|---------|---------|
| `make setup` | `uv sync` + pre-commit hooks |
| `make up` / `make down` | Docker: Spark (1 master, 2 workers), Postgres 16, Kafka KRaft |
| `make seed` | Generate star-schema Parquet (~0.01 GB) |
| `make seed-large` | ~1 GB for shuffle/OOM labs |
| `make load-sql` | Load Parquet into Postgres + apply SQL |
| `make spark-submit JOB=path/to/job.py` | Submit to **standalone cluster** (not `local[*]`) |
| `make oom-lab` | Module 04 OOM exercise (expect failure) |
| `make sql` | psql shell |
| `make lint` / `make typecheck` / `make test` | Quality gates |
| `make check` | lint + typecheck + test |

## Stack

- Python 3.12, **uv**, package `def_` under `src/def_/`
- **ruff**, **mypy** (strict on `src/def_/`), **pytest**
- Local Docker only — no cloud APIs
- **duckdb** for future warehousing module; **PySpark** on Bitnami Spark 3.5 cluster

## Layout

- `src/def_/common/` — Spark session builder, Postgres DSN, paths (cluster-first)
- `src/def_/datagen/` — Kimball-style retail star schema, `--scale-gb`
- `modules/NN_*/` — learning units; exercises + tests in-module
- `references/` — **gitignored** local textbook corpus; never commit
- `data/` — **gitignored** generated Parquet and explain artifacts

## Principles

1. **Real cluster over notebooks** — Spark jobs via `spark-submit` against `spark://localhost:7077`; inspect UI :8080 (cluster) and :4040 (app).
2. **Prove it** — Every exercise has pytest acceptance criteria; stubs use `skip`.
3. **Typed `src/`** — Fully annotated; `make typecheck` must pass before done.
4. **Copyright** — Paraphrase concepts in READMEs; cite as *Book — Chapter N*; never paste long verbatim text from `references/`.

## Spark session

Use `def_.common.spark.build_spark_session(name, cluster=True)` for graded jobs. Do not default to `local[*]` except isolated unit tests.

## Environment

Copy `.env.example` → `.env`. Defaults match `docker-compose.yml` (`def_user` / `def_learning`).

## Module status (first pass)

- **Built:** 03 SQL, 04 Spark, datagen, infra, agent files
- **Stub:** 01, 02, 05, 06, 07, 09

## UIs

- Spark master: http://localhost:8080
- Spark application: http://localhost:4040 (while a job runs)
