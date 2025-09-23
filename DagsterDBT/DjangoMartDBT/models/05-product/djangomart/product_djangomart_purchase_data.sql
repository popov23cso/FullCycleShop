SELECT
    pi.*,
    p.TOTAL_PRICE,
    p.USER,
    pr.DWH_SK AS PRODUCT_SK,
    pr.TITLE AS PRODUCT_TITLE,
    pr.STOCK,
    pr.RATING,
    c.DWH_SK AS CATEGORY_SK,
    c.TITLE AS CATEGORY_TITLE
FROM {{ref('historic_djangomart_purchase_items')}} pi
JOIN {{ref('historic_djangomart_purchases')}} p
    ON p.ID = pi.PURCHASE_ID 
LEFT JOIN {{ref('scd2_djangomart_products')}} pr 
    ON pi.PRODUCT_ID = pr.ID AND pi.UPDATED_DATE BETWEEN pr.DWH_EFFECTIVE_FROM AND pr.DWH_EFFECTIVE_TO
LEFT JOIN {{ref('scd2_djangomart_categories')}} c 
    ON pr.CATEGORY_ID = c.ID AND pi.UPDATED_DATE BETWEEN c.DWH_EFFECTIVE_FROM AND c.DWH_EFFECTIVE_TO
