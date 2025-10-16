SELECT 
    * 
FROM {{ source('predicted_next_week_sales', 'inferred_djangomart_purchase_summary_daily') }}