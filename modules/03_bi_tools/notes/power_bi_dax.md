# Power BI & DAX — two-question-drill answers

Power BI is central to the target role. These answer the BI section of the drill at the
"explain one level past the textbook + one tradeoff" bar. Conceptual notes — pair with
the `retail` star schema (module 02 Postgres / module 05 DuckDB) as the data source.

## Storage mode: Import vs DirectQuery vs Composite

- **Import** — data copied into the in-memory VertiPaq engine. Fastest queries, full DAX,
  but data is as fresh as the last scheduled refresh and is bounded by model size/memory.
- **DirectQuery** — queries pushed live to the source (Postgres/SQL Server/warehouse) at
  report time. Always current, no size limit, but every visual is a SQL round-trip — slow,
  and some DAX/time-intelligence is restricted. Source must handle the concurrency.
- **Composite** — mix per table: dimensions Imported (small, reused), huge fact tables
  DirectQuery. Plus **aggregations** — pre-aggregated Import tables transparently answer
  high-level visuals and fall back to DirectQuery for detail.

**Tradeoff in one line:** Import trades freshness for speed; DirectQuery trades speed for
freshness; Composite buys both at the cost of model complexity.

## Measure vs calculated column (why the difference matters for performance)

- **Calculated column** — computed **row-by-row at refresh**, materialized and stored in
  the model (costs memory, expands the model). Use only when you need a value to **slice/
  filter/relate** on (e.g., a bucket category).
- **Measure** — computed **at query time** in the current filter context, stores nothing.
  Use for all aggregations (`SUM`, `[Revenue] / [Target]`, YoY). Cheaper memory, scales.

**Rule:** if it aggregates or depends on what the user filtered → measure. If you need to
put it on an axis/slicer → calculated column. Defaulting everything to calculated columns
bloats the model and is the classic junior mistake.

```dax
Total Revenue = SUM(fact_sales[sales_amount])           -- measure
Revenue MoM % =                                          -- measure, time intelligence
VAR prev = CALCULATE([Total Revenue], DATEADD(dim_date[full_date], -1, MONTH))
RETURN DIVIDE([Total Revenue] - prev, prev)
```

`DIVIDE()` over `/` because it handles divide-by-zero (returns blank, not an error) —
the DAX twin of SQL's `NULLIF(y,0)`.

## Star schema in the model

Power BI wants a **star**: one fact, dimensions one hop away, single-direction filters
(dimension → fact). Avoid bi-directional relationships unless you truly need them — they
cause ambiguous filter paths and slow queries. A snowflake works but adds hops; flatten
to a star in the Gold layer (module 02/05) before it reaches the model.

## Row-level security (RLS) in Power BI

- **Static RLS** — a role with a fixed filter, e.g. `dim_store[region] = "East"`.
- **Dynamic RLS** — one role, predicate keyed on the logged-in user:
  `dim_store[region] = LOOKUPVALUE(user_region[region], user_region[email], USERPRINCIPALNAME())`.
  One role scales to thousands of users via a mapping table. This is the BI-layer mirror
  of the Postgres row-level security in [module 02](../../02_sql_relational/sql/07_rls_isolation.sql).
- **Cost / risk:** RLS filters propagate through relationships, adding query cost; a wrong
  predicate or a bi-directional relationship can **leak across the security boundary** —
  test roles with "View as role."

## KPI vs metric

A **KPI** is a metric tied to a target and a direction (revenue *vs target*, trending).
A bare metric ("total sessions") is just a number. **Gaming:** a KPI like "tickets closed"
is gamed by closing-and-reopening; guard with a paired counter-metric (reopen rate) or a
quality gate so optimizing the KPI can't degrade the real outcome.
