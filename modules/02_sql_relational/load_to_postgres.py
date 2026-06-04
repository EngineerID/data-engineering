"""Load generated Parquet star schema into Postgres."""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

import psycopg
import pyarrow.parquet as pq

from def_.common.io import get_postgres_dsn, parquet_paths
from def_.common.logging import get_logger

logger = get_logger(__name__)
SCHEMA = "retail"


def _pg_type(arrow_type: str) -> str:
    if "date" in arrow_type:
        return "DATE"
    if "int" in arrow_type:
        return "BIGINT"
    if "float" in arrow_type or "double" in arrow_type:
        return "DOUBLE PRECISION"
    return "TEXT"


def _load_table(conn: psycopg.Connection, table: str, path: Path) -> None:
    files = list(path.glob("**/*.parquet"))
    if not files:
        msg = f"No parquet files in {path}; run make seed first"
        raise FileNotFoundError(msg)
    arrow_table = pq.read_table(files[0])
    cols = arrow_table.column_names
    col_defs = ", ".join(f"{c} {_pg_type(str(arrow_table.schema.field(c).type))}" for c in cols)
    with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS {SCHEMA}.{table} CASCADE")
        cur.execute(f"CREATE TABLE {SCHEMA}.{table} ({col_defs})")
    conn.commit()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(cols)
    for i in range(arrow_table.num_rows):
        row = [arrow_table.column(c)[i].as_py() for c in cols]
        writer.writerow(row)
    buf.seek(0)

    col_list = ", ".join(cols)
    with (
        conn.cursor() as cur,
        cur.copy(
            f"COPY {SCHEMA}.{table} ({col_list}) FROM STDIN WITH (FORMAT csv, HEADER true)"
        ) as copy,
    ):
        copy.write(buf.read())
    conn.commit()
    logger.info("Loaded %s (%d rows)", table, arrow_table.num_rows)


def _run_sql_file(conn: psycopg.Connection, sql_path: Path) -> None:
    sql = sql_path.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    logger.info("Executed %s", sql_path.name)


def main() -> None:
    paths = parquet_paths()
    dsn = get_postgres_dsn()
    sql_dir = Path(__file__).parent / "sql"

    with psycopg.connect(dsn, autocommit=False) as conn:
        with conn.cursor() as cur:
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
        conn.commit()

        for name, p in paths.items():
            _load_table(conn, name, p)

        for sql_file in sorted(sql_dir.glob("*.sql")):
            _run_sql_file(conn, sql_file)

    logger.info("Postgres load complete")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Load failed")
        sys.exit(1)
