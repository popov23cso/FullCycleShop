WITH dummy_dagster_relation AS 
(
    SELECT * FROM {{ source('djangomart_products', 'dummy') }}
)

{{ read_data_lake_folder('DJANGOMART/PRODUCTS')}}