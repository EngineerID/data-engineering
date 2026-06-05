select
    sales_key,
    date_key,
    product_key,
    store_key,
    customer_key,
    quantity,
    sales_amount
from {{ source('raw', 'fact_sales') }}
