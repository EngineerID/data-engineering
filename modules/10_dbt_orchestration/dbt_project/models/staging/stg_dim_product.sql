select
    product_key,
    product_name,
    category,
    subcategory,
    brand,
    unit_price
from {{ source('raw', 'dim_product') }}
