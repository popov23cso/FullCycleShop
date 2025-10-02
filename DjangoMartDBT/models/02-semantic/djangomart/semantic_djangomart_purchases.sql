SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    total_price::BIGINT AS TOTAL_PRICE,
    is_invalid::BOOLEAN AS IS_INVALID,
    created_date::TIMESTAMP AS CREATED_DATE,
    updated_date::TIMESTAMP AS UPDATED_DATE,
    coalesce(generated_date, '2025-01-01T10:10:10Z')::TIMESTAMP AS GENERATED_DATETIME,
    GENERATED_DATETIME::DATE AS GENERATED_DATE,
    user::STRING AS USER
FROM {{ref('raw_djangomart_purchases')}}