SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    product_name::STRING AS PRODUCT_NAME,
    product_id::STRING AS PRODUCT_ID,
    price_at_purchase::DECIMAL AS PRICE_AT_PURCHASE,
    quantity::INT AS QUANTITY,
    created_date::DATETIME AS CREATED_DATE,
    updated_date::DATETIME AS UPDATED_DATE,
    purchase::STRING AS PURCHASE_ID
FROM {{ref('raw_djangomart_purchase_items')}}