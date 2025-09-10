SELECT
    -- {{ list_raw_metadata() }}
    *
FROM {{ref('raw_djangomart_products')}}