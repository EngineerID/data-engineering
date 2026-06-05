# Scope cap — note for AI assistants and future me

**This repo is deliberately capped at the depth and breadth implied by one external
document set: the Technical Interview Preparation Package.** It is a *note*, not a
freeze — the repo can still be edited, refactored, and corrected. But new work should
not push past the level below without an explicit decision to change the cap.

## The anchor document set

```
C:\Users\idamn\OneDrive\Documents\01 Admin\02 Canada\Ontario\
  Employment Ontario\VPI\Technical Interview Preparation Package\
    technical-glossary-index.md   — every term that is in scope (one line each)
    two-question-drill.md         — the depth bar (Q1 = one level past textbook, Q2 = a tradeoff/failure mode)
    sql-cheat-sheet.md            — the SQL/DBA depth bar specifically
    two-question-answers.md       — model answers (the actual ceiling)
```

These files live **outside the repo** (a personal OneDrive path, not tracked here), so a
fresh agent session won't see them unless the user provides them. They are the source of
truth for *what to build and how deep*. If a concept is not a term in the glossary, it is
out of scope. If a question in the drill probes something the repo can't yet demonstrate
or explain, that's an in-scope gap worth closing.

## The role this targets

DBA-leaning data-engineering role. Heaviest weight (lead with these):

> **SQL Server, MySQL, stored procedures, triggers, indexing, OLTP/OLAP, data
> warehouse, star schema, RBAC, Power BI.**

Secondary, still in scope: lakehouse/medallion, Delta table semantics, ELT/ETL,
Spark fundamentals, governance/compliance, dbt, cloud-storage portability.
Lighter (probed only if they appear on the CV): streaming internals, React, MLOps, CNNs.

## What "capped at interview level" means concretely

**In scope — build to the two-question depth:**
- You can *run* the happy path and *explain* one tradeoff and one failure mode.
- Example: Module 02 demonstrates an index turning a Seq Scan into an Index Scan, AND
  the README names SARGability, the write cost, and clustered-vs-non-clustered — that's
  the Q1+Q2 bar. It does **not** need a B-tree internals lab.

**Out of scope — do NOT add (no further in depth):**
- Production-grade distributed systems work: real cloud accounts, real Delta/Iceberg
  JARs on a real cluster, Spark tuning beyond shuffle/partitioning/OOM intuition,
  Kafka exactly-once transactional internals, query-planner internals.
- A real SQL Server / MySQL install. Postgres + DuckDB stand in; the **dialect
  differences are documented** (that is what the interview tests), not reproduced.
- Anything not traceable to a glossary term.

**Out of scope — do NOT add (no further in breadth):**
- New stacks, new clouds, new languages, new domains.
- Turning concept notes into full implementations where a note answers the drill.
  (Streaming, governance, and BI are intentionally docs-first: the interview asks you
  to *explain* them, not to operate them.)

## Heuristic for the next change

Before adding something, ask: **"Which glossary term does this serve, and does the
two-question drill for that term actually demand it?"**
- Demands a runnable artifact → build the minimal runnable artifact + a README that
  answers Q1 and Q2.
- Demands only an explanation → write/extend the concept note; don't build infra.
- Serves no glossary term → don't add it; note it under "Out of scope" if tempting.

## Where the cap is reflected in the repo

- Every `modules/NN_*/README.md` has a **"Prove-it"** section (acceptance criteria). The
  four role-heaviest modules — **02 SQL, 03 BI, 06 Kafka, 08 Lakehouse** — also carry an
  **"Interview bar"** section mapping exercises to the drill's Q1/Q2. (01/04/05/07/09/10
  predate this pass and don't yet have one; add it there only if you touch them.)
- [`curriculum.md`](curriculum.md) holds the reading lists and the concept-gap audit —
  all gaps are now marked covered (table formats are covered *within scope*; a real
  delta-rs/pyiceberg lab is explicitly out of scope there too).
- This file is the standing instruction; [`../CLAUDE.md`](../CLAUDE.md) links here, and
  its "Module status" block is the quick map of what exists.
