SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    product_name::STRING AS PRODUCT_NAME,
    product::STRING AS PRODUCT_ID,
    price_at_purchase::DECIMAL AS PRICE_AT_PURCHASE,
    quantity::INT AS QUANTITY,
    created_date::TIMESTAMP AS CREATED_DATE,
    updated_date::TIMESTAMP AS UPDATED_DATE,
    coalesce(generated_date, '2025-01-01T10:10:10Z')::TIMESTAMP AS GENERATED_DATETIME,
    GENERATED_DATETIME::DATE AS GENERATED_DATE,
    purchase::STRING AS PURCHASE_ID
FROM {{ref('raw_djangomart_purchase_items')}}