select
    store_key,
    store_name,
    city,
    state,
    region
from {{ source('raw', 'dim_store') }}
