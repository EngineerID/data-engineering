# SQL Foundations
### The mental models the pattern examples rely on — nothing more

> **Where this sits in the module.** This is the **mental-model rung** of Module 02:
> the four ideas that explain *why* the analytical patterns are shaped the way they
> are. It sits **above** raw `SELECT`/`WHERE`/`JOIN` syntax (assumed — that floor is
> the prep package's `sql-cheat-sheet.md` §1–§4, an anchor doc named in
> [`docs/scope-cap.md`](../../../docs/scope-cap.md)) and **below** the runnable
> artifacts in [`../sql/`](../sql/). Read this,
> then [`sql-patterns.md`](sql-patterns.md), then watch each pattern execute in the
> `.sql` files. See the module [`README.md`](../README.md) for the full ladder.
>
> **Dialect bridge.** These examples are MySQL 8.0+. This repo *runs* on Postgres,
> and the differences are documented rather than reproduced (scope-cap policy): the
> logical processing order, `GROUP BY` vs. window split, `OVER (...)`, and CTEs are
> **identical** across MySQL / Postgres / SQL Server. Only the surface idioms differ
> (`IF()` → `CASE WHEN`, `LIMIT/OFFSET` → `FETCH`/`TOP`); each is flagged below and
> in [`../README.md`](../README.md#dialect-note).

This document covers only the SQL machinery needed to read the pattern examples
that follow, pitched at someone already comfortable writing queries. It is not a
beginner tutorial — it skips `SELECT`/`WHERE`/`JOIN` basics and instead nails
down the four ideas that quietly explain *why* the patterns are shaped the way
they are: **evaluation order, the GROUP BY vs. window split, the window syntax
itself, and CTEs.** Get these and the pattern doc reads as obvious.

Dialect note: MySQL 8.0+. Window functions and CTEs don't exist before 8.0.

---

## 1. Logical query processing order (the key to almost everything)

SQL does **not** run in the order you write it. You write `SELECT` first, but
the engine evaluates clauses in roughly this order:

```
FROM / JOIN     → assemble the rows
WHERE           → filter individual rows
GROUP BY        → collapse rows into groups
HAVING          → filter groups
WINDOW funcs    → compute per-row analytics (ROW_NUMBER, COUNT OVER, ...)
SELECT          → pick/compute output columns (aliases born here)
DISTINCT        → drop duplicate output rows
ORDER BY        → sort
LIMIT / OFFSET  → keep a slice
```

This single list explains a cluster of otherwise-baffling rules:

- **You can't filter a window function in `WHERE`.** `WHERE` runs *before*
  window functions are computed, so the rank/count column doesn't exist yet.
  That's why every ranking or window-count query computes the value in a
  CTE/subquery and filters it in an *outer* query — the filter has to happen
  after the window step.
- **You can't use a `SELECT` alias in `WHERE`.** Aliases are born in `SELECT`,
  which runs after `WHERE`. (You *can* use them in `ORDER BY`, which runs later.)
- **`HAVING` exists separately from `WHERE`** because `WHERE` filters rows
  *before* grouping and `HAVING` filters *after*.

**Where you'll see this:** every two-step "compute in a CTE, filter outside"
pattern (Stadium, Investments, Department Highest Salary) exists *because* of
this ordering. In this repo it's the shape of every view in
[`../sql/04_window_patterns.sql`](../sql/04_window_patterns.sql): the window
column is computed in an inner CTE/subquery, then filtered (`WHERE rn <= 3`,
`WHERE rn = 1`) in the outer query — because it cannot be filtered any earlier.

---

## 2. Aggregates: `GROUP BY` collapses rows

A plain aggregate with `GROUP BY` reduces each group to a **single output row**.
The detail rows are gone — you only get the grouping columns and the aggregates.

```sql
SELECT departmentId, COUNT(*), MAX(salary)
FROM Employee
GROUP BY departmentId;
-- one row per department; individual employees are no longer visible
```

`HAVING` then filters those grouped rows:

```sql
... GROUP BY departmentId HAVING COUNT(*) > 5;
```

Conditional aggregation pushes a condition *inside* the aggregate so it only
counts matching rows — this is how you compute a rate in one pass:

```sql
SUM(IF(status != 'completed', 1, 0)) / COUNT(*)   -- MySQL IF(cond, then, else)
SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) / COUNT(*)  -- portable
```

**Where you'll see this:** Trips and Users uses conditional aggregation +
`GROUP BY day` to get a per-day cancellation rate. Keep the contrast with the
next section firmly in mind — it's the most important distinction in the whole
pattern doc.

---

## 3. Window functions: same numbers, but rows stay intact

A window function computes an aggregate or rank **without collapsing rows**.
Every row keeps all its columns *and* gains the computed value. The `OVER (...)`
clause is what makes a function a window function.

```sql
COUNT(*) OVER (PARTITION BY tiv_2015)
```

Read `OVER (...)` in three parts:

- **`PARTITION BY col`** — split rows into groups (like `GROUP BY`), but *don't*
  collapse them. The function is computed within each partition. Omit it to
  treat the whole table as one partition.
- **`ORDER BY col`** — order rows *within* each partition. Required by ranking
  functions (they need to know what "first" means); optional for plain counts.
- The function itself.

**Two families appear in the examples:**

*Ranking functions* — assign a position within each partition:

```sql
ROW_NUMBER() OVER (ORDER BY id)                          -- 1,2,3,4 (always unique)
DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC)
```

How the three behave on ties:

- **`ROW_NUMBER`** — arbitrary unique numbering (1,2,3); no tie sharing.
- **`RANK`** — ties share a rank (1,1,3), then the next rank *skips*.
- **`DENSE_RANK`** — ties share a rank (1,1,2), then the next rank does *not* skip.

*Aggregate windows* — a normal aggregate with `OVER`, attached to every row:

```sql
COUNT(*) OVER (PARTITION BY lat, lon)   -- "how many rows share my location?"
SUM(people) OVER (PARTITION BY id_group)
```

A windowed aggregate can also take an explicit **frame** (`ROWS BETWEEN …`) to
compute running totals — see the `running_total` column in
[`../sql/04_window_patterns.sql`](../sql/04_window_patterns.sql), and `LAG()` in
the same file for period-over-period.

**The mental model:** `GROUP BY COUNT(*)` answers "how big is each group?" and
gives you *one row per group*. `COUNT(*) OVER (PARTITION BY ...)` answers the
same question but writes the answer onto *every original row*, so you can then
filter individual rows by their group's size.

**Where you'll see this:** Investments (`COUNT OVER` twice), Stadium
(`ROW_NUMBER` for the gaps-and-islands trick, `COUNT OVER` to size runs),
Department Highest Salary (`DENSE_RANK`). In this repo:
`v_top_products_per_region` (`ROW_NUMBER`), `v_monthly_revenue` (`LAG` + framed
`SUM OVER`), and `v_customer_emails_deduped` (`ROW_NUMBER` dedup) — all in
[`../sql/04_window_patterns.sql`](../sql/04_window_patterns.sql).

---

## 4. CTEs: name a result, then build on it

A CTE (Common Table Expression) is a named, temporary result set written with
`WITH`, *before* the main query. It's the readable alternative to nesting
subqueries inside subqueries.

```sql
WITH ranked AS (
    SELECT name, salary,
           DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) AS rnk
    FROM Employee
)
SELECT name, salary
FROM ranked          -- the main query reads the CTE by name
WHERE rnk = 1;       -- and can now filter on the window column (section 1!)
```

You can chain them — each CTE may read the ones above it:

```sql
WITH first AS (...),
     second AS (SELECT ... FROM first)   -- builds on `first`
SELECT ... FROM second;
```

CTEs are the standard way to satisfy the "compute in one scope, filter in the
next" requirement from section 1. The trade-off: each layer costs a little
readability and sometimes performance, so add layers the logic actually needs —
no more.

**Where you'll see this:** Stadium chains two CTEs; Investments and Department
Highest Salary each use one to hold a window result before filtering it. A
*recursive* CTE — the same `WITH` machinery walking a hierarchy — is demonstrated
runnably in [`../sql/02_recursive_cte.sql`](../sql/02_recursive_cte.sql).

---

## 5. A few MySQL specifics in the examples

- **`IF(condition, then_value, else_value)`** — MySQL's inline conditional. The
  portable equivalent is `CASE WHEN condition THEN ... ELSE ... END`. (This repo's
  Postgres artifacts use `CASE WHEN`.)
- **`ROUND(value, 2)`** — round to 2 decimal places (used for the rate and the
  summed investment value).
- **`LIMIT n OFFSET m`** — return `n` rows after skipping the first `m`.
  `LIMIT 1 OFFSET 1` means "skip the top row, take the next one" — i.e. the 2nd.
  (SQL Server spells this `OFFSET … FETCH`; Postgres accepts both `LIMIT/OFFSET`
  and `FETCH`.)
- **`BETWEEN a AND b`** — inclusive range filter, used on dates in Trips.

---

## Putting it together: annotated Investments in 2016

This is the cleanest example in the set, and it shows three foundations at once
— window-as-filter, the compute-then-filter shape, and a CTE:

```sql
WITH InsuranceCounts AS (                          -- CTE (section 4): a named stage
    SELECT
        tiv_2016,
        COUNT(*) OVER (PARTITION BY tiv_2015)   AS tiv_2015_count,  -- window count (section 3)
        COUNT(*) OVER (PARTITION BY lat, lon)   AS loc_count        -- rows stay intact
    FROM Insurance
)
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016         -- aggregate the survivors (section 5: ROUND)
FROM InsuranceCounts
WHERE tiv_2015_count > 1                            -- filter on the window column —
  AND loc_count = 1;                               -- only possible out here (section 1)
```

In one pass it tags every row with two group statistics, then keeps rows whose
2015 value is shared but whose location is unique — no self-join, no second
scan. Once each line above maps cleanly to a section here, the pattern doc's
explanation of *why* this beats the alternatives will read as obvious.
