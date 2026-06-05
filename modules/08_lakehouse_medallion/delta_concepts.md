# Delta-style table concepts (portable) — and how to demonstrate them

Paraphrased; cite *Reis & Housley — Fundamentals of Data Engineering* and the Delta
Lake docs. The runnable proof for each concept is in
[`table_format_lab.py`](table_format_lab.py) (DuckDB simulating the *semantics* — no
Delta JAR, per [`../../docs/scope-cap.md`](../../docs/scope-cap.md)).

## ACID on object storage

Object storage (S3/GCS/ADLS) has no transactions — a multi-file write can be seen
half-done. Delta adds a **transaction log** (`_delta_log/`, ordered JSON commits) on top
of Parquet. A writer stages new Parquet files, then **atomically appends one commit** to
the log; readers only see files referenced by committed log entries, so they always get
a consistent snapshot. Isolation is **snapshot isolation** via optimistic concurrency:
two writers each read a version, and the second to commit must reconcile or fail and
retry. **Durability** is the hardest letter on cloud storage — it leans on the object
store's own durability and on the log being the single source of truth.

## Time travel

The log retains previous versions, so you can read `VERSION AS OF n` / `TIMESTAMP AS OF`
for audit, debugging, or rollback. **Recovery drill:** a bad `MERGE` an hour ago →
`RESTORE TABLE t TO VERSION AS OF <pre-merge>` (or read the old version and overwrite
forward). The window is **bounded by retention** — `VACUUM` deletes files older than the
retention threshold (default 7 days), after which those versions are gone. The lab's
`time_travel_demo()` keeps an explicit `gold_v0` snapshot and restores from it.

## Schema enforcement

A write is rejected when it doesn't match the table schema. Walk the cases: a **type
mismatch** rejects; an **extra column** rejects (unless `mergeSchema`); a **missing
column** is allowed only if the column is nullable. Strict enforcement keeps bad data
out; it becomes a liability when a benign new field should flow through — relax it
explicitly via evolution, never by disabling the check. Lab: `schema_enforcement_demo()`.

## Schema evolution

Controlled, safe changes without breaking readers. **Add column** = metadata-only, old
rows read back NULL, downstream readers expecting the old shape still work (this is how
you add a column safely). **Drop / rename / type-change** are not free — they force a
rewrite or a new column + backfill. Lab: `schema_evolution_demo()`.

## Idempotent MERGE (the pipeline-correctness primitive)

Insert-or-update on a natural key so re-running a batch — or a retried CDC event —
produces no duplicate. This is the same idea as the relational `ON CONFLICT` / `MERGE`
in [module 02](../02_sql_relational/sql/06_merge_upsert.sql). Lab:
`idempotent_merge_demo()` runs the same upsert twice and asserts the row count is stable.

## Parquet & why columnar

Columnar layout unlocks two analytics wins: **column pruning** (read only the columns the
query needs) and **predicate pushdown + run-length/dictionary encoding** (skip row groups
via min/max stats, compress repeated values). Parquet is the *wrong* format for
row-at-a-time OLTP writes or tiny point lookups — that's a row store's job.

## Iceberg vs Delta (one architectural difference)

Both add ACID + snapshots over Parquet. Delta uses an ordered JSON/Parquet **transaction
log**; Iceberg uses a tree of **metadata + manifest files** pointing at data files. You'd
pick **Iceberg in a multi-engine shop** (Spark + Trino + Flink + Snowflake all reading
one table) because its spec is engine-neutral; Delta is strongest inside the
Databricks/Spark ecosystem.

## Relation to this repo

The medallion pipeline ([`medallion_pipeline.py`](medallion_pipeline.py)) practices the
**layering** (Bronze append-only → Silver cleaned/validated → Gold aggregated) on local
Parquet; this file + `table_format_lab.py` cover the **table-format semantics** a
lakehouse adds on top. Together they answer the Lakehouse, Delta Lake, and Medallion
sections of the two-question drill.
