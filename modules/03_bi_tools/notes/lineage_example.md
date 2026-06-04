# Lineage example — regional revenue

## Report field

Dashboard tile: **Regional Revenue** (sum).

## Semantic model

- Table: `Sales`
- Measure: `Regional Revenue = SUM(Sales[sales_amount])`
- Dimension: `Store[region]` from related `dim_store`

## Warehouse source

- Postgres schema `retail`
- Fact: `retail.fact_sales.sales_amount`
- Dimension: `retail.dim_store.region` via `fact_sales.store_key`

## Lineage diagram (text)

`Regional Revenue` → `SUM(sales_amount)` → `retail.fact_sales` → join `retail.dim_store` on `store_key`
