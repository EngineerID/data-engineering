"""Module 08 — Delta-style table semantics on DuckDB (no Delta JAR).

The two-question drill asks you to *explain and demonstrate* what a transactional
table format buys you on top of plain Parquet: idempotent MERGE, schema enforcement,
schema evolution, and time travel. Per `docs/scope-cap.md` we simulate the *semantics*
on DuckDB rather than standing up a real Delta/Iceberg cluster — the interview tests
the concepts, not the cluster. Each function returns a small result a test can assert.
"""

from __future__ import annotations

from typing import TypedDict

import duckdb


class MergeResult(TypedDict):
    rows_after_first: int
    rows_after_second: int
    idempotent: bool


def idempotent_merge_demo() -> MergeResult:
    """Run the same upsert twice; an idempotent MERGE leaves the row count unchanged.

    Drill (Idempotent MERGE): the natural key (id) + insert-or-update means a retried
    CDC event hits the UPDATE branch and overwrites in place — no duplicate row.
    """
    con = duckdb.connect()
    con.execute("CREATE TABLE target (id INTEGER PRIMARY KEY, value INTEGER, updated_at TIMESTAMP)")
    con.execute(
        "CREATE TABLE staging AS SELECT * FROM (VALUES (1, 10), (2, 20), (3, 30)) AS t(id, value)"
    )

    upsert = (
        "INSERT OR REPLACE INTO target (id, value, updated_at) SELECT id, value, now() FROM staging"
    )
    con.execute(upsert)
    first = con.sql("SELECT COUNT(*) FROM target").fetchone()[0]
    # Second run simulates a retried/replayed batch — must not duplicate.
    con.execute(upsert)
    second = con.sql("SELECT COUNT(*) FROM target").fetchone()[0]
    con.close()
    return {
        "rows_after_first": int(first),
        "rows_after_second": int(second),
        "idempotent": first == second,
    }


def schema_enforcement_demo() -> dict[str, bool]:
    """A typed table rejects a write whose type can't be coerced — bad data stays out.

    Drill (Schema enforcement): a type mismatch triggers rejection. Strict enforcement
    is a liability only when a benign new column should be allowed — relax it explicitly
    via evolution (see below), never by turning off the check.
    """
    con = duckdb.connect()
    con.execute("CREATE TABLE silver (id INTEGER, amount DOUBLE)")
    con.execute("INSERT INTO silver VALUES (1, 9.99)")

    rejected = False
    try:
        # 'not-a-number' cannot be coerced to DOUBLE → enforcement rejects the write.
        con.execute("INSERT INTO silver VALUES (2, 'not-a-number')")
    except duckdb.Error:
        rejected = True

    good_rows = con.sql("SELECT COUNT(*) FROM silver").fetchone()[0]
    con.close()
    return {"bad_write_rejected": rejected, "table_uncorrupted": good_rows == 1}


def schema_evolution_demo() -> dict[str, bool]:
    """Adding a nullable column is a metadata-only change; old rows read back as NULL.

    Drill (Schema evolution): add is safe/automatic; drop/rename/type-change force a
    rewrite. A downstream reader expecting the old shape still works because the new
    column is nullable and defaults to NULL for pre-existing rows.
    """
    con = duckdb.connect()
    con.execute("CREATE TABLE silver (id INTEGER, amount DOUBLE)")
    con.execute("INSERT INTO silver VALUES (1, 9.99)")

    # Safe evolution: ADD COLUMN (no rewrite of existing data).
    con.execute("ALTER TABLE silver ADD COLUMN currency VARCHAR")
    old_reader_ok = con.sql("SELECT id, amount FROM silver").fetchone() == (1, 9.99)
    new_col_null = con.sql("SELECT currency FROM silver WHERE id = 1").fetchone()[0] is None

    con.execute("INSERT INTO silver VALUES (2, 5.00, 'CAD')")
    new_row_ok = con.sql("SELECT currency FROM silver WHERE id = 2").fetchone()[0] == "CAD"
    con.close()
    return {
        "old_reader_still_works": old_reader_ok,
        "old_rows_null_for_new_col": new_col_null,
        "new_rows_carry_value": new_row_ok,
    }


def time_travel_demo() -> dict[str, int | bool]:
    """Keep version snapshots so a bad write can be recovered by reading an older one.

    Drill (Time travel): you ran a bad MERGE an hour ago — read VERSION AS OF the
    pre-MERGE version and overwrite forward. Here versions are explicit snapshot tables;
    in Delta they're the transaction log + retained files (bounded by the retention /
    VACUUM window, which is why time travel isn't infinite).
    """
    con = duckdb.connect()
    con.execute("CREATE TABLE gold (region VARCHAR, revenue INTEGER)")
    con.execute("INSERT INTO gold VALUES ('east', 100), ('west', 200)")
    # v0 = good snapshot (the transaction log's previous version).
    con.execute("CREATE TABLE gold_v0 AS SELECT * FROM gold")
    good_total = con.sql("SELECT SUM(revenue) FROM gold").fetchone()[0]

    # A bad MERGE zeroes out revenue.
    con.execute("UPDATE gold SET revenue = 0")
    bad_total = con.sql("SELECT SUM(revenue) FROM gold").fetchone()[0]

    # Recover: restore from v0 (the "RESTORE TABLE ... TO VERSION AS OF 0" equivalent).
    con.execute("DELETE FROM gold")
    con.execute("INSERT INTO gold SELECT * FROM gold_v0")
    recovered_total = con.sql("SELECT SUM(revenue) FROM gold").fetchone()[0]
    con.close()
    return {
        "good_total": int(good_total),
        "bad_total": int(bad_total),
        "recovered_total": int(recovered_total),
        "recovered_to_good": good_total == recovered_total,
    }


def main() -> None:
    print("idempotent MERGE :", idempotent_merge_demo())
    print("schema enforce   :", schema_enforcement_demo())
    print("schema evolution :", schema_evolution_demo())
    print("time travel      :", time_travel_demo())


if __name__ == "__main__":
    main()
