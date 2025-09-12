SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    total_price::BIGINT AS TOTAL_PRICE,
    is_invalid::BOOLEAN AS IS_INVALID,
    created_date::DATETIME AS CREATED_DATE,
    updated_date::DATETIME AS UPDATED_DATE,
    user::STRING AS USER
FROM {{ref('raw_djangomart_purchases')}}