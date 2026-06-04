# Fact grain checklist

## Subject area

Retail sales (`fact_sales` grain: one row per line item / sale event).

## Grain definition

- **Grain:** one row per `sale_id` (line on a ticket)
- **Additive measures:** `quantity`, `sales_amount`
- **Semi-additive:** none in this slice

## Common mis-aggregation traps

- Summing `sales_amount` after joining to `dim_product` without fixing grain duplicates rows
- Averaging unit price across rows that are not at product-day grain

## Your notes

Extend this file when connecting Power BI or Tableau semantic models to `retail.fact_sales`.
