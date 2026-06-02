"""I/O paths and Postgres connectivity."""

from __future__ import annotations

import os
from pathlib import Path


def data_dir() -> Path:
    root = Path(os.environ.get("DATA_DIR", "data"))
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()


def parquet_paths() -> dict[str, Path]:
    base = data_dir() / "parquet"
    return {
        "fact_sales": base / "fact_sales",
        "dim_date": base / "dim_date",
        "dim_product": base / "dim_product",
        "dim_store": base / "dim_store",
        "dim_customer": base / "dim_customer",
    }


def get_postgres_dsn() -> str:
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "def_learning")
    user = os.environ.get("POSTGRES_USER", "def_user")
    password = os.environ.get("POSTGRES_PASSWORD", "def_pass")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"
