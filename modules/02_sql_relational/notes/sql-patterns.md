# Reusable Patterns: Analytical SQL

> **Where this sits in the module.** This is the **pattern rung** of Module 02 —
> the judgment layer between the mental models in
> [`sql-foundations.md`](sql-foundations.md) and the runnable, tested artifacts in
> [`../sql/`](../sql/). Read foundations first. Each pattern below states the *why*
> once; where this repo already *proves* it with a runnable view, the note links
> out instead of repeating the SQL — concept here, proof there. The full
> pattern → artifact map is at the bottom. See [`README.md`](../README.md) for the
> ladder, and `notes/normalization_oltp_olap.md` for the OLTP/OLAP/isolation models
> these patterns assume.

Six transferable patterns extracted from the five examples, plus the judgment
calls (simplicity vs. cleverness, window vs. `GROUP BY`) that separate a
*working* query from a *clean, fast* one.

Each example, its core pattern(s), and a one-line verdict:

- **Human Traffic of Stadium** — gaps & islands + window-count filter + CTE chain · correct, but over-layered.
- **Trips and Users** — conditional aggregation + multi-join filter · solid, idiomatic.
- **Investments in 2016** — window-count as a filter + CTE · the cleanest of the set.
- **Department Highest Salary** — rank-and-filter (top-N per group) · textbook use of `DENSE_RANK`.
- **Second Highest Salary** — nth-value selection · works, but the slow form.

**When to reach for each pattern:**

1. **CTE staging** — when a computed value must be filtered/reused, or nesting is getting unreadable.
2. **Window-aggregate-as-filter** — when you need a per-group number (count, rank, total) but must keep every row and column.
3. **Gaps & islands** — when you need to group *consecutive* rows (runs, streaks, sessions).
4. **Rank-and-filter** — when you want the top-N (or nth) row *within each group*.
5. **Conditional aggregation** — when you're counting/summing only the rows that meet a condition (rates, pivots).
6. **Nth-value selection** — when you want a single ranked value (2nd highest, median-ish, etc.).

A note on dialect: these are MySQL. Window functions and CTEs require **MySQL
8.0+**. `IF(...)` is MySQL-specific; `CASE WHEN` is the portable equivalent (and
the form this repo's Postgres artifacts use). The patterns themselves are
dialect-independent.

---

## 1. CTE staging (name your steps, then build on them)

**Reach for it when** a query needs a computed column that you'll later filter
on, or when nested subqueries are becoming hard to read.

**Key insight.** A CTE (`WITH name AS (...)`) is a named, temporary result set
defined *before* the main query. It turns a tangled nest of subqueries into a
top-to-bottom pipeline: each stage names its output, the next stage reads it.

```sql
WITH stage_one AS (
    SELECT ... FROM source
),
stage_two AS (
    SELECT ... FROM stage_one      -- builds on the previous stage
)
SELECT ... FROM stage_two;          -- final answer reads the last stage
```

**Where you'll see this:** Stadium chains two CTEs (`partitioned_stadium` →
`group_counts`); Investments and Department Highest Salary each use one. In this
repo, every view in [`../sql/04_window_patterns.sql`](../sql/04_window_patterns.sql)
stages a CTE before filtering, and [`../sql/02_recursive_cte.sql`](../sql/02_recursive_cte.sql)
shows the *recursive* form.

**The discipline:** each CTE layer has a readability *and* a performance cost.
Add a layer when it earns its keep — when it isolates a real step. The Stadium
solution works but stacks more layers than the logic needs; that's the
difference between "correct" and "clean."

---

## 2. Window aggregate as a filter (the move to internalize)

**Reach for it when** you need a per-group statistic — a count, a total, a rank
— but you must keep every individual row and all its columns.

**Key insight.** `GROUP BY` *collapses* each group into one row, so you lose the
detail rows. A window aggregate computes the same number but *attaches it to
every row* without collapsing anything:

```sql
COUNT(*) OVER (PARTITION BY tiv_2015)   -- "how many rows share my tiv_2015?"
```

Every row keeps its identity and also learns its group's count. This is what
lets you say "keep rows whose group has more than one member" without a
self-join back to the detail.

**The catch — and the universal shape.** You *cannot* filter on a window
function in the same `WHERE` (evaluation order: `WHERE` runs before window
functions exist — see [`sql-foundations.md` §1](sql-foundations.md#1-logical-query-processing-order-the-key-to-almost-everything)).
So the pattern is always two-step: **compute the window column in a CTE/subquery,
then filter on it in the outer query.**

```sql
WITH counted AS (
    SELECT *,
           COUNT(*) OVER (PARTITION BY tiv_2015) AS tiv_2015_count,
           COUNT(*) OVER (PARTITION BY lat, lon) AS loc_count
    FROM Insurance
)
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM counted
WHERE tiv_2015_count > 1 AND loc_count = 1;   -- filter happens out here
```

**Where you'll see this:** Investments (two `COUNT OVER` filters — duplicated
value *and* unique location in one pass, no self-join), Stadium (`COUNT OVER`
to size each group), Department Highest Salary (`DENSE_RANK OVER`). The
runnable repo proof is `v_top_products_per_region` (compute `ROW_NUMBER`, filter
`rn <= 3`) in [`../sql/04_window_patterns.sql`](../sql/04_window_patterns.sql).

**vs. `GROUP BY` / `HAVING`:** if you only need the aggregated rows themselves
(one row per group), `GROUP BY ... HAVING` is simpler and often faster. Use the
window form when you need the detail rows *alongside* the group statistic.

---

## 3. Gaps and islands (group consecutive rows)

**Reach for it when** you need to find runs of consecutive rows — streaks,
sessions, "3+ days in a row," uninterrupted ID sequences.

**Key insight.** For consecutive IDs, both the ID and the row number climb by 1
in lockstep, so their *difference stays constant* within a run. A gap in the
IDs breaks the constant. That difference becomes a group label:

```sql
id - ROW_NUMBER() OVER (ORDER BY id) AS id_group
```

Walking the arithmetic, `(id, row_number) → id - row_number`:

- `(5, 1) → 4`
- `(6, 2) → 4` — same group (consecutive)
- `(7, 3) → 4` — same group
- `(9, 4) → 5` — new group (8 was missing)

Once each run shares a label, group by it and filter by run length (here, with
the window-count from pattern 2: `group_size >= 3`).

**Where you'll see this:** Stadium — the `id - ROW_NUMBER()` line is the entire
trick; everything around it is plumbing to count and filter the runs.

**Generalizes to:** longest win/loss streaks, consecutive login days, contiguous
free time slots. The same `value - ROW_NUMBER()` idea works on dates if you
convert to a day number first. *(Explanation-only in this repo — see the map
below; it shares the `ROW_NUMBER` machinery already runnable in
[`../sql/04_window_patterns.sql`](../sql/04_window_patterns.sql).)*

---

## 4. Rank-and-filter (top-N or nth per group)

**Reach for it when** you want the highest (or nth) row *within each group* —
top earner per department, latest order per customer, etc.

**Key insight.** A ranking window numbers rows inside each partition; the outer
query then keeps the rank you want.

```sql
WITH ranked AS (
    SELECT name, salary,
           DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) AS rnk
    FROM Employee
)
SELECT name, salary FROM ranked WHERE rnk = 1;
```

**The one distinction worth memorizing** (ties on the same value):

- **`ROW_NUMBER`** — breaks the tie arbitrarily (1,2,3,4); no shared ranks.
- **`RANK`** — ties share a rank (1,1,3), then the next rank skips (here 3).
- **`DENSE_RANK`** — ties share a rank (1,1,2), then the next rank does not skip.

Pick by intent: "every employee tied for top pay" → `DENSE_RANK`/`RANK`; "exactly
one row per group" → `ROW_NUMBER`.

**Where you'll see this:** Department Highest Salary uses `DENSE_RANK() = 1` so
that co-leaders on equal salary are all returned. The repo's
`v_top_products_per_region` is the *top-N* form with `ROW_NUMBER` (one row per
rank); the dedup-keep-latest view `v_customer_emails_deduped` is the *nth = 1*
form — both in [`../sql/04_window_patterns.sql`](../sql/04_window_patterns.sql).

**Generalizes to:** this is also the clean fix for Second Highest Salary (see
pattern 6) — `DENSE_RANK ... = 2`.

---

## 5. Conditional aggregation (count/sum only what matches)

**Reach for it when** you need a rate, a count of matching rows, or a pivot —
"what fraction of trips were cancelled per day?"

**Key insight.** Put a condition *inside* an aggregate so it only counts the
rows you care about, computing the whole thing in one pass — no extra subquery,
no second join.

```sql
SUM(IF(status != 'completed', 1, 0)) / COUNT(*)        -- MySQL
SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) / COUNT(*)   -- portable
```

`SUM(1/0 per row)` counts the matches; dividing by `COUNT(*)` turns it into a
rate. (An even shorter idiom: `AVG(status != 'completed')`, since the average of
1s and 0s *is* the rate.)

**Where you'll see this:** Trips and Users computes a per-day cancellation rate
this way, wrapped in `ROUND(..., 2)` and grouped by day — with the banned-user
and date filters handled in `WHERE` before aggregation.

**Generalizes to:** building pivot-style columns (`SUM(CASE WHEN region='EU' ...)`
as one column, `... 'US' ...` as another), pass/fail counts, any "share of rows
meeting X."

---

## 6. Selecting the nth value (and why the example was slow)

**Reach for it when** you want a single ranked scalar — 2nd highest salary,
3rd most recent, etc.

The example used:

```sql
SELECT DISTINCT salary FROM Employee ORDER BY salary DESC LIMIT 1 OFFSET 1;
```

It's correct, but it's the form the assessment flagged as slow: `DISTINCT` over
the whole column, a full sort, then skip-one. Two cleaner alternatives:

```sql
-- (a) correlated MAX subquery: "the largest salary below the maximum"
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);

-- (b) rank-and-filter (pattern 4), scales to "nth" by changing the number
SELECT DISTINCT salary
FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
      FROM Employee) t
WHERE rnk = 2;
```

**Key insight.** "Nth value" has several correct shapes; they are not equally
clean. For *2nd specifically*, the `MAX`-below-`MAX` form (a) is the simplest and
usually the fastest. For a general *nth*, the ranking form (b) is the one that
scales — change `= 2` to `= n` and you're done. Reach for `LIMIT/OFFSET` last
when ranking would read more clearly.

**Where you'll see this:** Second Highest Salary — and it's the clearest single
illustration of this doc's main theme below.

---

## Cross-cutting takeaways

These tie directly to the patterns above — and to the habits worth building.

- **The recurring shape is "compute, then filter."** Window functions and
  conditional aggregates produce a value per row; you then filter on that value
  in an outer scope (CTE or subquery). Internalizing *why* the filter must live
  outside (evaluation order) removes most of the guesswork.

- **`GROUP BY` collapses; window functions don't.** Choosing between them is the
  single highest-leverage decision in these problems. Need one row per group →
  `GROUP BY`. Need every row *plus* a group statistic → window. Investments is
  clean precisely because it picked the window form and skipped a self-join.

- **Match the pattern to the question's shape, not to your comfort zone.** The
  performance swings (Investments clean, Second Highest slow) trace back to
  reaching for a familiar tool over the simplest effective one. A two-line
  `MAX`-subquery beats a `DISTINCT`-sort-offset for "second highest"; a single
  `GROUP BY` can beat a CTE-plus-window when you don't need the detail rows.

- **Every CTE layer should earn its place.** They aid readability, but stacking
  layers the logic doesn't require (Stadium) trades performance for nothing.
  Fewer, well-named stages beat many thin ones.

- **Prefer the form that generalizes.** `DENSE_RANK ... = n` reads the same for
  2nd, 3rd, or nth; `LIMIT/OFFSET` quietly changes meaning with `DISTINCT` and
  ties. When two forms are equally correct, keep the one a teammate can extend
  without rethinking it.

---

## Pattern → runnable artifact map (concept here, proof there)

To keep this note free of duplicated SQL, each pattern points at the repo
artifact that *executes and tests* it. "Explanation-only" patterns are kept at
the two-question depth here by design (scope cap) — the idea and its trade-off,
not a graded harness.

Each pattern, where it runs in this repo, and the test that guards it:

1. **CTE staging** → [`sql/04_window_patterns.sql`](../sql/04_window_patterns.sql) (every view) and [`sql/02_recursive_cte.sql`](../sql/02_recursive_cte.sql) (recursive); guarded across `test_sql_slice.py`.
2. **Window-aggregate-as-filter** → `v_top_products_per_region` (compute `rn`, filter outside); guarded by `test_top_n_per_region`.
3. **Gaps & islands** → *explanation-only*; reuses the `ROW_NUMBER` machinery proven in `v_top_products_per_region` / `v_customer_emails_deduped`.
4. **Rank-and-filter** → `v_top_products_per_region` (top-N) and `v_customer_emails_deduped` (nth=1 dedup); guarded by `test_top_n_per_region` and `test_dedup_keeps_latest`.
5. **Conditional aggregation** → *explanation-only*; the `CASE WHEN` rate idiom — closest runnable cousin is the framed/`LAG` analytics in `v_monthly_revenue`.
6. **Nth-value selection** → *explanation-only*; pattern 4's `DENSE_RANK ... = n` is the runnable generalization.

Also one rung down the stack: the array-side mirror of pattern 4's
"partition the equal things, keep one representative" is the sort+dedup move in
[Module 01's array/string patterns](../../01_python_model/notes/array-string-patterns.md#4-sort--fix-one--skip-duplicates)
— same reasoning, different syntax.
