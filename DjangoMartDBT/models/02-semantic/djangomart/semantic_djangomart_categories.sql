SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    title::STRING AS TITLE,
    description::STRING AS DESCRIPTION,
    is_main_category::BOOLEAN AS IS_MAIN_CATEGORY,
    is_active::BOOLEAN AS IS_ACTIVE,
    parent_category::STRING AS PARENT_CATEGORY,
    created_date::TIMESTAMP AS CREATED_DATE,
    updated_date::TIMESTAMP AS UPDATED_DATE,
    coalesce(generated_date, '2025-01-01T10:10:10Z')::TIMESTAMP AS GENERATED_DATETIME,
    GENERATED_DATETIME::DATE AS GENERATED_DATE
FROM {{ref('raw_djangomart_categories')}}