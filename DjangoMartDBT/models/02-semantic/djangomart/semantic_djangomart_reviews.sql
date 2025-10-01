SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    rating::INT AS RATING,
    comment::STRING AS COMMENT,
    user::STRING AS USER_ID,
    purchase_item::STRING AS PURCHASE_ITEM_ID,
    product::STRING AS PRODUCT_ID,
    created_date::DATETIME AS CREATED_DATE,
    updated_date::DATETIME AS UPDATED_DATE,
    generated_date::DATETIME AS GENERATED_DATE
FROM {{ref('raw_djangomart_reviews')}}