-- Gold mart: revenue per region. Joins the fact to the store dimension at the
-- correct grain (one row per region) so the measure is not fanned out.
select
    s.region,
    round(sum(f.sales_amount), 2) as revenue,
    count(*) as line_count
from {{ ref('stg_fact_sales') }} as f
join {{ ref('stg_dim_store') }} as s on f.store_key = s.store_key
group by s.region
