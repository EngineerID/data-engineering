# Data Engineering Foundations

A hands-on learning repository that closes the gap between **applied data governance** (medallion, lineage, quality) and the **systems-internals layer** underneath: Spark driver/executors and the DAG, SQL views/CTEs and index tuning, dimensional modeling at scale.

Assessment is **prove-it**: runnable jobs, captured plans, and passing pytest — not recall.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Compose
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/) (recommended on Windows)
- [uv](https://docs.astral.sh/uv/) (Python 3.12)

Place the curriculum and textbook extracts in `references/` (gitignored). See `references/big_data_engineering_curriculum_md.md` for the full module map.

## Quickstart (< 10 commands)

Run from **WSL** at the repo root (e.g. `/mnt/c/GitHub/data-engineering`). Without `make`, use `uv run` equivalents (see `Makefile`).

**Windows (no WSL):** `py -3.12 -m uv sync --all-groups`, then `.\\.venv\\Scripts\\python.exe -m pytest` with `$env:PYTHONPATH="src"`.

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

- Postgres: `localhost:5432` — db `def_learning`, user `def_user`
- Spark master UI: http://localhost:8080
- Spark app UI (during a job): http://localhost:4040

## Modules

| Module | Status | Topic |
|--------|--------|-------|
| [01_python_model](modules/01_python_model/) | stub | Python data model |
| [02_dsa](modules/02_dsa/) | stub | Algorithms |
| [03_sql_relational](modules/03_sql_relational/) | **built** | Views, recursive CTEs, indexing |
| [04_spark_internals](modules/04_spark_internals/) | **built** | Cluster jobs, Catalyst, OOM lab |
| [05_warehousing_bi](modules/05_warehousing_bi/) | stub | Kimball / DuckDB |
| [06_streaming_kafka](modules/06_streaming_kafka/) | stub | Kafka KRaft |
| [07_oop_design_patterns](modules/07_oop_design_patterns/) | stub | OOP / patterns |
| [08_ai_assisted_dev](modules/08_ai_assisted_dev/) | agent files | CLAUDE.md, Cursor rules |
| [09_capstone_governance](modules/09_capstone_governance/) | stub | Governance at scale |

## Scale knob

Generate larger data for shuffle/spill practice:

```bash
make seed-large   # ~1 GB
# or
uv run python -m def_.datagen.cli --scale-gb 2.0
```

## Agent context

- [`CLAUDE.md`](CLAUDE.md) — commands and conventions for AI assistants
- [`.cursor/rules/`](.cursor/rules/) — Cursor project rules

## License

Learning use. Textbook content stays in local `references/` only.
