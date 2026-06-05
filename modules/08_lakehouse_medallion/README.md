# Module 08 — Lakehouse, Delta Lake & Medallion Architecture

**Status:** built (capstone for the lakehouse half of the curriculum)

## What's in this folder

- `medallion_pipeline.py` — bronze / silver / gold Parquet layers + `data/medallion/lineage.json`
- `table_format_lab.py` — runnable Delta-style semantics on DuckDB: idempotent MERGE, schema enforcement, schema evolution, time travel
- `delta_concepts.md` — full two-question-drill answers (ACID, time travel, enforcement, evolution, Parquet, Iceberg vs Delta)
- `governance_compliance.md` — PII, PIPEDA/HIPAA/GDPR/BCBS 239, de-identification, lineage
- `tests/test_medallion_pipeline.py` — pipeline and lineage checks
- `tests/test_table_format_lab.py` — proves each table-format semantic

## Infrastructure

Local DuckDB + `data/parquet/` from `make seed` (no Spark/Delta JAR required — see
[`../../docs/scope-cap.md`](../../docs/scope-cap.md) for why we simulate the semantics).

## Run

```bash
make seed
uv run python modules/08_lakehouse_medallion/medallion_pipeline.py
uv run python modules/08_lakehouse_medallion/table_format_lab.py
uv run pytest modules/08_lakehouse_medallion/tests
```

Native Windows: `.\tasks.ps1 seed`; run scripts/pytest via the venv python directly.

## Prove-it exercises (each has a test)

1. **Medallion layering** — bronze (append-only) → silver (validated) → gold (aggregated)
   under `data/medallion/`, with `lineage.json` (silver_rows ≤ bronze_rows).
2. **Idempotent MERGE** — `idempotent_merge_demo()`: re-running the upsert keeps the row count stable.
3. **Schema enforcement** — `schema_enforcement_demo()`: a bad-type write is rejected, table uncorrupted.
4. **Schema evolution** — `schema_evolution_demo()`: `ADD COLUMN` leaves old readers working, old rows NULL.
5. **Time travel** — `time_travel_demo()`: recover from a bad write by restoring a prior snapshot.
6. **Governance** — `governance_compliance.md`: PII classification → gold exposes only aggregates.

## Interview bar (maps to the two-question drill)

- **Medallion** — Q1 column-level Bronze→Silver→Gold change (raw payload + ingest metadata
  → conformed/typed/deduped → regional aggregate); Q2 what does *not* belong in Silver
  (business-specific aggregation — that's Gold).
- **Delta Lake / ACID** — Q1 transaction log gives snapshot isolation on object storage;
  Q2 Durability is hardest on object storage. See `delta_concepts.md`.
- **Time travel** — Q1 bounded by retention/VACUUM; Q2 the bad-MERGE recovery walk.
- **Schema enforcement vs evolution** — which changes are safe (add) vs force a rewrite
  (drop/rename/type) — demonstrated, not just asserted.
- **GDPR erasure on append-only** — see `governance_compliance.md` (delete via rewrite/
  `DELETE` + VACUUM, or crypto-shredding the pseudonymization key).

## Further reading

[`docs/curriculum.md` — Repo module 08](../../docs/curriculum.md#repo-module-08--lakehouse-and-medallion)
