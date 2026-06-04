# Module 04 — Distributed Systems & Apache Spark Internals

## What's in this folder

- `join_aggregate_job.py` — cluster join/aggregate + explain artifact
- `oom_exercise.py` — intentional OOM lab
- `tests/test_spark_slice.py` — Spark integration tests (`-m spark`)

## Infrastructure

Docker: **spark-master**, **spark-worker-1**, **spark-worker-2** (`infra/docker-compose.yml`). Reads Parquet from `data/` (via `make seed`).

## Run

```bash
make up
make seed        # use make seed-large for shuffle-heavy runs
make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py
make oom-lab     # expect failure
uv run pytest modules/04_spark_internals/tests -m spark
```

- Cluster UI: http://localhost:8080
- Application UI: http://localhost:4040 (while a job runs)

## Prove-it exercises (this pass)

1. **Cluster join/aggregate** — Run `make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py`. Acceptance: job completes on standalone cluster; `data/explain/join_aggregate.txt` contains a physical plan with shuffle/exchange.
2. **Read the Spark UI** — Acceptance: you can point to **Jobs → Stages → Tasks** and identify the shuffle stage.
3. **Catalyst plans** — Acceptance: you can name where Catalyst optimization appears in the formatted explain file.
4. **OOM lab** — Run `make oom-lab` (expect failure). Acceptance: explain skew + shuffle + low executor memory; document fix (broadcast join, repartition, `spark.executor.memory`).

## Logical vs physical plan (walkthrough)

1. **Logical plan** — Unresolved/reresolved logical nodes (joins, aggregates).
2. **Catalyst** — Rule-based optimizer rewrites the logical plan (filter pushdown, constant folding).
3. **Physical plan** — Concrete operators (`Exchange`, `SortAggregate`, `BroadcastHashJoin`) scheduled as jobs → stages → tasks on executors.

## Further reading

[`docs/curriculum.md` — Repo module 04](../docs/curriculum.md#repo-module-04--spark-internals)
