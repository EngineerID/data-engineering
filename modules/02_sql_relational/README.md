# Module 02 — Relational Databases, SQL & Query Optimization

The DBA core. This is the heaviest-weighted module for the target role (SQL Server /
MySQL / stored procedures / triggers / indexing / OLTP-OLAP / star schema). Postgres
stands in; **dialect differences are documented, not reproduced** (see `docs/scope-cap.md`).

## The ladder (query-comfortable → DBA ceiling)

Three rungs, concept-first then proof. The notes carry the *why* (and the MySQL
interview idioms); the `.sql` files are the runnable, tested *how* in Postgres.
Cross-links keep them one click apart, so neither repeats the other.

- **Rung 0 — Mental models** · [`notes/sql-foundations.md`](notes/sql-foundations.md) — logical processing order, `GROUP BY` vs. window, `OVER(...)`, CTEs: *why* the patterns are shaped as they are.
- **Rung 1 — Patterns** · [`notes/sql-patterns.md`](notes/sql-patterns.md) — six analytical patterns plus the judgment calls (window vs. `GROUP BY`, which CTE earns its layer). Each maps to a runnable view.
- **Rung 2 — Proof + DBA depth** · [`sql/`](sql/) artifacts + tests — the patterns executing on seed data, **plus** the DBA-only material no LeetCode set covers: index tuning/SARGability, procedures, triggers, idempotent MERGE, RLS.

Entry floor: `SELECT`/`WHERE`/`JOIN` are assumed (the prep package's
`sql-cheat-sheet.md §1–§4` is that rung). Rung 2 is where this module goes
*past* the analytical-pattern docs into the role's heaviest-weighted topics.

## What's in this folder

Runnable SQL artifacts (each maps to a drill term):

- `sql/01_views.sql` — views over a star join.
- `sql/02_recursive_cte.sql` — recursive CTE for hierarchies.
- `sql/03_index_demo.sql` — index tuning (Seq Scan → Index Scan).
- `sql/04_window_patterns.sql` — top-N per group, MoM + running total, dedup-keep-latest.
- `sql/05_procedures_triggers.sql` — stored procedure + AFTER UPDATE audit trigger.
- `sql/06_merge_upsert.sql` — idempotent upsert / MERGE (no dupes on re-run).
- `sql/07_rls_isolation.sql` — row-level security (tenant isolation).

Concept notes:

- `notes/sql-foundations.md` — mental models: processing order, `GROUP BY` vs window, `OVER()`, CTEs.
- `notes/sql-patterns.md` — six analytical patterns + window-vs-`GROUP BY` judgment, mapped to the runnable views.
- `notes/normalization_oltp_olap.md` — normalization→3NF, OLTP vs OLAP, isolation levels.

Plumbing:

- `load_to_postgres.py` — load Parquet into Postgres and apply scripts in order.
- `tests/test_sql_slice.py` — prove-it tests (`-m postgres`).

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
  index). See the "Worked example: reading the plan" section below for real captured plans.
- **Trigger** — Q1 AFTER vs INSTEAD OF; Q2 classic danger: hidden side-effects/cascades,
  hard to reason about — keep business logic in code, integrity/audit in triggers.
- **Stored procedure** — Q1 one advantage (server-side, reusable, fewer round-trips) +
  one downside (logic outside VCS/tests unless you version the DDL); Q2 how to test it.
- **Idempotent MERGE** — Q1 natural key + insert-or-update; Q2 a retried CDC event hits
  `ON CONFLICT DO UPDATE` and overwrites in place → no duplicate.
- **RBAC / RLS** — Q1 enforce in the engine not the app; Q2 leakage risk if the policy
  predicate is wrong; superusers bypass RLS (use `FORCE` + non-superuser roles).
- **Normalization / OLTP-OLAP / isolation** — see `notes/normalization_oltp_olap.md`.

## Worked example: reading the plan (SARGability)

`test_index_speedup` runs the same query with and without an index and saves both plans
to `data/sql_plans/`. Below are **real captured plans** from this repo's seed data
(`WHERE customer_key = 42`). The lesson is *how to read a plan*, not "index = always
faster":

**Without index** — `data/sql_plans/without_index.txt`:
```
Aggregate  (cost=48.70..48.71 rows=1 ...) (actual time=0.247..0.273 ...)
  Buffers: shared hit=22
  ->  Seq Scan on fact_sales f  (cost=0.00..48.67 rows=11 ...) (actual time=0.241..0.242 ...)
        Filter: (customer_key = 42)
        Rows Removed by Filter: 2083
Execution Time: 0.323 ms
```

**With index** — `data/sql_plans/with_index.txt`:
```
Aggregate  (cost=8.30..8.31 rows=1 ...) (actual time=12.061..12.064 ...)
  Buffers: shared hit=3 read=2
  ->  Index Scan using idx_fact_customer_key on fact_sales f  (cost=0.28..8.30 rows=1 ...)
        Index Cond: (customer_key = 42)
Execution Time: 12.088 ms
```

What an interviewer wants you to notice:

- **Seq Scan + `Rows Removed by Filter: 2083`** = the engine read every row and threw
  most away. **Index Scan + `Index Cond`** = it jumped straight to matching rows.
- **The honest twist:** on this *tiny* table the Seq Scan is faster in wall-clock
  (0.32 ms vs 12 ms — the index path paid a cold-cache `read=2`). The signals that
  actually predict the win at scale are the **planner cost (48.70 → 8.30)** and
  **buffers touched (22 → 5)**. That's why the test asserts on **plan shape** (an
  `Index Scan` appears), not on raw milliseconds — wall-clock on toy data is noise.
  Indexes pay off as the table grows and the filter is selective.
- **SARGability** decides whether the index can even be used. `Index Cond:
  (customer_key = 42)` is SARGable. These are **not** (they force a Seq Scan):
  ```sql
  WHERE YEAR(order_date) = 2026     -- ❌ function on the column
  WHERE order_date >= '2026-01-01'  -- ✅ rewrite as a range
        AND order_date < '2027-01-01'
  WHERE email LIKE '%@gmail.com'    -- ❌ leading wildcard
  WHERE email LIKE 'ivan%'          -- ✅ prefix is fine
  ```

Regenerate the artifacts anytime: `make load-sql` then
`uv run pytest modules/02_sql_relational/tests -k index -m postgres`.

## Dialect note

`ON CONFLICT` (Postgres) ≙ `ON DUPLICATE KEY UPDATE` (MySQL) ≙ `MERGE` (SQL Server /
Databricks). `GENERATED ALWAYS AS IDENTITY` ≙ `AUTO_INCREMENT` (MySQL) ≙ `IDENTITY(1,1)`
(SQL Server). RLS via `CREATE POLICY` (Postgres) ≙ `CREATE SECURITY POLICY` with an
inline TVF predicate (SQL Server). Full table in `sql-cheat-sheet.md` §15.

## Further reading

[`docs/curriculum.md` — Repo module 02](../../docs/curriculum.md#repo-module-02--sql)
