SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    title::STRING AS TITLE,
    description::STRING AS DESCRIPTION,
    is_main_category::BOOLEAN AS IS_MAIN_CATEGORY,
    is_active::BOOLEAN AS IS_ACTIVE,
    parent_category::STRING AS PARENT_CATEGORY,
    created_date::DATETIME AS CREATED_DATE,
    updated_date::DATETIME AS UPDATED_DATE
FROM {{ref('raw_djangomart_categories')}}