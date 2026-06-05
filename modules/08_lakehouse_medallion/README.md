# Module 08 — Lakehouse, Delta Lake & Medallion Architecture

**Status:** light

## What's in this folder

- `medallion_pipeline.py` — bronze / silver / gold Parquet layers + `data/medallion/lineage.json`
- `delta_concepts.md` — ACID, time travel, schema evolution write-up starter
- `governance_compliance.md` — PII, PIPEDA/HIPAA/GDPR/BCBS 239, de-identification, lineage
- `tests/test_medallion_pipeline.py` — pipeline and lineage checks

## Infrastructure

Local DuckDB + `data/parquet/` from `make seed` (no Spark required for light pass).

## Run

```bash
make seed
uv run python modules/08_lakehouse_medallion/medallion_pipeline.py
uv run pytest modules/08_lakehouse_medallion/tests
```

## Prove-it exercises

1. **Medallion at scale** — bronze/silver/gold under `data/medallion/` with lineage metadata
2. **Delta-style table semantics** — expand `delta_concepts.md`
3. **Performance report** — optional: tie tuning notes back to module 04 Spark work
4. **Governance & compliance** — extend `governance_compliance.md`; tag a PII column and show the gold layer exposes only aggregated, non-identifying data

## Further reading

[`docs/curriculum.md` — Repo module 08](../../docs/curriculum.md#repo-module-08--lakehouse-and-medallion)
