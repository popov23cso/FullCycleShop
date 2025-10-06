WITH product_base AS 
(
    SELECT
        *,
        COALESCE(
        LEAD(DWH_BATCH_DATETIME) OVER (PARTITION BY ID ORDER BY DWH_BATCH_DATETIME),
        {{var('END_OF_TIME')}}) AS next_delta
    FROM {{ref('historic_djangomart_products')}}
), 
category_dates AS 
(
    SELECT
        ID,
        DWH_SK,
        DWH_BATCH_DATETIME
    FROM {{ref('historic_djangomart_categories')}}

    {% if is_incremental() %}
        WHERE DWH_BATCH_DATETIME > (SELECT MAX(DWH_DELTA_DATE) FROM {{ this }})
    {% endif %}
),
integrated_category_dates AS
(
    SELECT 
        p.* EXCLUDE (DWH_DELTA_DATE, next_delta, DWH_SK),
        HASH(p.DWH_SK, c.DWH_SK) AS DWH_SK,
        c.DWH_BATCH_DATETIME AS DWH_DELTA_DATE
    FROM product_base p
    JOIN category_dates c ON c.ID = p.CATEGORY_ID
    AND c.DWH_BATCH_DATETIME >= p.DWH_BATCH_DATETIME
    AND c.DWH_BATCH_DATETIME < p.next_delta
),
product_history AS (
    SELECT 
        *
    FROM {{ ref('historic_djangomart_products') }}
)

SELECT 
    {{ dbt_utils.star(from=ref('historic_djangomart_products')) }},
    'product' AS CHANGE_SOURCE
FROM product_history
UNION ALL 
SELECT
    {{ dbt_utils.star(from=ref('historic_djangomart_products')) }},
    'category' AS CHANGE_SOURCE
FROM integrated_category_dates
