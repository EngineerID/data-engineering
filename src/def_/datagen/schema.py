"""Star schema definitions (Kimball Ch. 3 — retail sales)."""

from __future__ import annotations

from typing import TypedDict


class ColumnSpec(TypedDict):
    name: str
    dtype: str


STAR_TABLES: dict[str, list[ColumnSpec]] = {
    "dim_date": [
        {"name": "date_key", "dtype": "int32"},
        {"name": "full_date", "dtype": "date32"},
        {"name": "year", "dtype": "int16"},
        {"name": "quarter", "dtype": "int8"},
        {"name": "month", "dtype": "int8"},
        {"name": "day_of_month", "dtype": "int8"},
    ],
    "dim_product": [
        {"name": "product_key", "dtype": "int32"},
        {"name": "product_name", "dtype": "string"},
        {"name": "category", "dtype": "string"},
        {"name": "subcategory", "dtype": "string"},
        {"name": "brand", "dtype": "string"},
        {"name": "unit_price", "dtype": "float64"},
    ],
    "dim_store": [
        {"name": "store_key", "dtype": "int32"},
        {"name": "store_name", "dtype": "string"},
        {"name": "city", "dtype": "string"},
        {"name": "state", "dtype": "string"},
        {"name": "region", "dtype": "string"},
    ],
    "dim_customer": [
        {"name": "customer_key", "dtype": "int32"},
        {"name": "customer_name", "dtype": "string"},
        {"name": "segment", "dtype": "string"},
        {"name": "country", "dtype": "string"},
    ],
    "fact_sales": [
        {"name": "sales_key", "dtype": "int64"},
        {"name": "date_key", "dtype": "int32"},
        {"name": "product_key", "dtype": "int32"},
        {"name": "store_key", "dtype": "int32"},
        {"name": "customer_key", "dtype": "int32"},
        {"name": "quantity", "dtype": "int32"},
        {"name": "sales_amount", "dtype": "float64"},
    ],
}

# Cardinalities for dimension tables (fact rows scale to hit --scale-gb)
DIM_CARDINALITIES: dict[str, int] = {
    "dim_date": 365 * 3,
    "dim_product": 500,
    "dim_store": 50,
    "dim_customer": 10_000,
}
