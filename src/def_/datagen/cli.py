"""CLI: generate star-schema Parquet at a target scale in GB."""

from __future__ import annotations

import argparse
import random
from datetime import date, timedelta
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from def_.common.io import data_dir, parquet_paths
from def_.common.logging import get_logger
from def_.datagen.schema import DIM_CARDINALITIES, STAR_TABLES

logger = get_logger(__name__)
RNG = random.Random(42)

# Rough bytes per fact row in Parquet (empirical; used to scale toward --scale-gb)
BYTES_PER_FACT_ROW = 48


def _write_table(name: str, table: pa.Table, out_path: Path) -> int:
    out_path.mkdir(parents=True, exist_ok=True)
    pq.write_table(  # type: ignore[no-untyped-call]
        table, out_path / "part-00000.parquet", compression="snappy"
    )
    size = sum(f.stat().st_size for f in out_path.glob("**/*") if f.is_file())
    logger.info("Wrote %s: %d rows, %.2f MB", name, table.num_rows, size / 1e6)
    return size


def _gen_dim_date(n: int) -> pa.Table:
    start = date(2022, 1, 1)
    keys: list[int] = []
    dates: list[date] = []
    years: list[int] = []
    quarters: list[int] = []
    months: list[int] = []
    days: list[int] = []
    for i in range(n):
        d = start + timedelta(days=i)
        keys.append(i + 1)
        dates.append(d)
        years.append(d.year)
        quarters.append((d.month - 1) // 3 + 1)
        months.append(d.month)
        days.append(d.day)
    return pa.table(
        {
            "date_key": pa.array(keys, type=pa.int32()),
            "full_date": pa.array(dates, type=pa.date32()),
            "year": pa.array(years, type=pa.int16()),
            "quarter": pa.array(quarters, type=pa.int8()),
            "month": pa.array(months, type=pa.int8()),
            "day_of_month": pa.array(days, type=pa.int8()),
        }
    )


def _gen_dim_product(n: int) -> pa.Table:
    categories = ["Electronics", "Apparel", "Grocery", "Home", "Sports"]
    return pa.table(
        {
            "product_key": pa.array(range(1, n + 1), type=pa.int32()),
            "product_name": pa.array([f"Product-{i}" for i in range(1, n + 1)]),
            "category": pa.array([categories[i % len(categories)] for i in range(n)]),
            "subcategory": pa.array([f"Sub-{i % 20}" for i in range(n)]),
            "brand": pa.array([f"Brand-{i % 50}" for i in range(n)]),
            "unit_price": pa.array(
                [round(RNG.uniform(5.0, 500.0), 2) for _ in range(n)], type=pa.float64()
            ),
        }
    )


def _gen_dim_store(n: int) -> pa.Table:
    regions = ["North", "South", "East", "West"]
    return pa.table(
        {
            "store_key": pa.array(range(1, n + 1), type=pa.int32()),
            "store_name": pa.array([f"Store-{i}" for i in range(1, n + 1)]),
            "city": pa.array([f"City-{i % 30}" for i in range(n)]),
            "state": pa.array([f"ST-{i % 10}" for i in range(n)]),
            "region": pa.array([regions[i % len(regions)] for i in range(n)]),
        }
    )


def _gen_dim_customer(n: int) -> pa.Table:
    segments = ["Consumer", "Corporate", "Home Office"]
    return pa.table(
        {
            "customer_key": pa.array(range(1, n + 1), type=pa.int32()),
            "customer_name": pa.array([f"Customer-{i}" for i in range(1, n + 1)]),
            "segment": pa.array([segments[i % len(segments)] for i in range(n)]),
            "country": pa.array(["US" if i % 5 else "CA" for i in range(n)]),
        }
    )


def _gen_fact_sales(
    n_rows: int,
    n_date: int,
    n_product: int,
    n_store: int,
    n_customer: int,
) -> pa.Table:
    sales_keys = list(range(1, n_rows + 1))
    date_keys = [RNG.randint(1, n_date) for _ in range(n_rows)]
    product_keys = [RNG.randint(1, n_product) for _ in range(n_rows)]
    store_keys = [RNG.randint(1, n_store) for _ in range(n_rows)]
    customer_keys = [RNG.randint(1, n_customer) for _ in range(n_rows)]
    quantities = [RNG.randint(1, 10) for _ in range(n_rows)]
    amounts = [round(q * RNG.uniform(5.0, 200.0), 2) for q in quantities]
    return pa.table(
        {
            "sales_key": pa.array(sales_keys, type=pa.int64()),
            "date_key": pa.array(date_keys, type=pa.int32()),
            "product_key": pa.array(product_keys, type=pa.int32()),
            "store_key": pa.array(store_keys, type=pa.int32()),
            "customer_key": pa.array(customer_keys, type=pa.int32()),
            "quantity": pa.array(quantities, type=pa.int32()),
            "sales_amount": pa.array(amounts, type=pa.float64()),
        }
    )


def estimate_fact_rows(scale_gb: float) -> int:
    target_bytes = max(scale_gb, 0.001) * 1e9
    # Subtract small dim footprint (~few MB)
    dim_overhead = 5 * 1e6
    fact_bytes = max(target_bytes - dim_overhead, 1e5)
    return max(int(fact_bytes / BYTES_PER_FACT_ROW), 1_000)


def generate(scale_gb: float) -> Path:
    """Generate all star-schema tables; return data root."""
    paths = parquet_paths()
    n_date = DIM_CARDINALITIES["dim_date"]
    n_product = DIM_CARDINALITIES["dim_product"]
    n_store = DIM_CARDINALITIES["dim_store"]
    n_customer = DIM_CARDINALITIES["dim_customer"]
    n_fact = estimate_fact_rows(scale_gb)

    logger.info(
        "Target scale ~%.3f GB -> ~%d fact rows (dims fixed)",
        scale_gb,
        n_fact,
    )

    total = 0
    total += _write_table("dim_date", _gen_dim_date(n_date), paths["dim_date"])
    total += _write_table("dim_product", _gen_dim_product(n_product), paths["dim_product"])
    total += _write_table("dim_store", _gen_dim_store(n_store), paths["dim_store"])
    total += _write_table("dim_customer", _gen_dim_customer(n_customer), paths["dim_customer"])
    total += _write_table(
        "fact_sales",
        _gen_fact_sales(n_fact, n_date, n_product, n_store, n_customer),
        paths["fact_sales"],
    )

    root = data_dir()
    logger.info("Total generated size: %.2f MB (%.4f GB)", total / 1e6, total / 1e9)
    _ = STAR_TABLES  # schema reference for tooling
    return root


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate retail star-schema Parquet")
    parser.add_argument(
        "--scale-gb",
        type=float,
        default=0.01,
        help="Approximate total dataset size in GB (fact table dominates)",
    )
    args = parser.parse_args()
    generate(args.scale_gb)


if __name__ == "__main__":
    main()
