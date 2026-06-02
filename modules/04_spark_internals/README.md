# Module 04 — Distributed Systems & Apache Spark Internals

## Interview gap this closes

> Could not explain spark-submit lifecycle (driver, executors, DAG, Catalyst, jobs/stages/tasks); PySpark described as "open a session, close a session"; could not diagnose executor OOM; no experience past ~5 GB.

## Reference reading

- *Learning Spark* — Chapters 2–3 (architecture, SparkSession)
- *Spark: The Definitive Guide* — Chapters 2–3, 10 (core concepts, SQL)
- *Designing Data-Intensive Applications* (Kleppmann) — Chapter 10 (batch processing)

## Prove-it exercises (this pass)

1. **Cluster join/aggregate** — Run `make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py`. Acceptance: job completes on standalone cluster; `data/explain/join_aggregate.txt` contains a physical plan with shuffle/exchange.
2. **Read the Spark UI** — Open http://localhost:8080 (cluster) and http://localhost:4040 (application). Acceptance: you can point to **Jobs → Stages → Tasks** and identify the shuffle stage.
3. **Catalyst plans** — Compare logical vs physical sections in the explain file. Acceptance: you can name where Catalyst optimization (predicate pushdown, join reorder) appears in the formatted plan.
4. **OOM lab** — Run `make oom-lab` (expect failure). Acceptance: you can explain skew + shuffle + low executor memory as root cause; document fix (broadcast join, repartition, `spark.executor.memory`).

## Logical vs physical plan (walkthrough)

1. **Logical plan** — Unresolved/reresolved logical nodes (what you asked for: joins, aggregates).
2. **Catalyst** — Rule-based optimizer rewrites the logical plan (filter pushdown, constant folding).
3. **Physical plan** — Concrete operators (`Exchange` = shuffle, `SortAggregate`, `BroadcastHashJoin`) scheduled as **jobs** containing **stages** separated by shuffle boundaries, each stage having **tasks** on executors.

## Run this slice

```bash
make up
make seed        # use make seed-large for shuffle-heavy runs
make spark-submit JOB=modules/04_spark_internals/join_aggregate_job.py
```
