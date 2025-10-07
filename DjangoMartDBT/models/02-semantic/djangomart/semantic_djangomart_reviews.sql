SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    rating::INT AS RATING,
    comment::STRING AS COMMENT,
    user::STRING AS USER_ID,
    purchase_item::STRING AS PURCHASE_ITEM_ID,
    product::STRING AS PRODUCT_ID,
    created_date::TIMESTAMP AS CREATED_DATE,
    updated_date::TIMESTAMP AS UPDATED_DATE,
    coalesce(generated_date, '2025-01-01T10:10:10Z')::TIMESTAMP AS GENERATED_DATETIME,
    GENERATED_DATETIME::DATE AS GENERATED_DATE
FROM {{ref('raw_djangomart_reviews')}}