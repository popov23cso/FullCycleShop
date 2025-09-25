SELECT 
    *
FROM {{ ref('historic_djangomart_reviews') }}
WHERE DWH_IS_LATEST = 1