# Module 02 — Relational Databases, SQL & Query Optimization

The DBA core. This is the heaviest-weighted module for the target role (SQL Server /
MySQL / stored procedures / triggers / indexing / OLTP-OLAP / star schema). Postgres
stands in; **dialect differences are documented, not reproduced** (see `docs/scope-cap.md`).

## What's in this folder

| File | Concept (drill term) |
|---|---|
| `sql/01_views.sql` | Views over a star join |
| `sql/02_recursive_cte.sql` | Recursive CTE for hierarchies |
| `sql/03_index_demo.sql` | Index tuning (Seq Scan → Index Scan) |
| `sql/04_window_patterns.sql` | Top-N per group, MoM + running total, dedup-keep-latest |
| `sql/05_procedures_triggers.sql` | Stored procedure + AFTER UPDATE audit trigger |
| `sql/06_merge_upsert.sql` | Idempotent upsert / MERGE (no dupes on re-run) |
| `sql/07_rls_isolation.sql` | Row-level security (tenant isolation) |
| `notes/normalization_oltp_olap.md` | Normalization→3NF, OLTP vs OLAP, isolation levels |
| `load_to_postgres.py` | Load Parquet into Postgres and apply scripts in order |
| `tests/test_sql_slice.py` | Prove-it tests (`-m postgres`) |

## Infrastructure

Docker service: **postgres** (`infra/docker-compose.yml`). Requires `make seed` first.

## Run

```bash
make seed
make up
make load-sql
uv run pytest modules/02_sql_relational/tests -m postgres
```

Native Windows: `.\tasks.ps1 seed`, `.\tasks.ps1 up`, `.\tasks.ps1 load-sql`.
Optional: `make sql` for an interactive `psql` shell.

## Prove-it exercises (each has a test)

1. **VIEW over star join** — `v_sales_by_region`: one row per `dim_store.region`.
2. **Recursive CTE** — `v_category_tree` row count equals `product_hierarchy`.
3. **Index tuning** — `EXPLAIN ANALYZE` shows Index Scan after the index; plans saved to `data/sql_plans/`.
4. **Top-N per group** — `v_top_products_per_region`: ≤ 3 products/region, ranked by revenue.
5. **Window analytics** — `v_monthly_revenue`: MoM change (LAG) + cumulative running total.
6. **Dedup keep-latest** — `v_customer_emails_deduped`: newest row wins per email.
7. **Trigger** — an `AFTER UPDATE` trigger writes a JSONB before/after image to `audit_log`.
8. **Stored procedure** — `refresh_regional_kpi()` is idempotent (re-run = same rows).
9. **Idempotent upsert** — `upsert_gold_kpi()` re-run changes no row count.
10. **Row-level security** — under a non-superuser role, a tenant sees only its rows.

## Interview bar (maps to the two-question drill)

- **Index** — Q1 clustered vs non-clustered (physical row order vs separate B-tree);
  Q2 why indexes hurt writes + SARGability (`YEAR(col)=2026` and leading `%` kill the
  index). See `notes/` and the EXPLAIN artifacts.
- **Trigger** — Q1 AFTER vs INSTEAD OF; Q2 classic danger: hidden side-effects/cascades,
  hard to reason about — keep business logic in code, integrity/audit in triggers.
- **Stored procedure** — Q1 one advantage (server-side, reusable, fewer round-trips) +
  one downside (logic outside VCS/tests unless you version the DDL); Q2 how to test it.
- **Idempotent MERGE** — Q1 natural key + insert-or-update; Q2 a retried CDC event hits
  `ON CONFLICT DO UPDATE` and overwrites in place → no duplicate.
- **RBAC / RLS** — Q1 enforce in the engine not the app; Q2 leakage risk if the policy
  predicate is wrong; superusers bypass RLS (use `FORCE` + non-superuser roles).
- **Normalization / OLTP-OLAP / isolation** — see `notes/normalization_oltp_olap.md`.

## Dialect note

`ON CONFLICT` (Postgres) ≙ `ON DUPLICATE KEY UPDATE` (MySQL) ≙ `MERGE` (SQL Server /
Databricks). `GENERATED ALWAYS AS IDENTITY` ≙ `AUTO_INCREMENT` (MySQL) ≙ `IDENTITY(1,1)`
(SQL Server). RLS via `CREATE POLICY` (Postgres) ≙ `CREATE SECURITY POLICY` with an
inline TVF predicate (SQL Server). Full table in `sql-cheat-sheet.md` §15.

## Further reading

[`docs/curriculum.md` — Repo module 02](../../docs/curriculum.md#repo-module-02--sql)
