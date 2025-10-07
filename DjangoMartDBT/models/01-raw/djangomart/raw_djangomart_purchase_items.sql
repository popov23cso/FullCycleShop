WITH dummy_dagster_relation AS 
(
    SELECT * FROM {{ source('djangomart_purchase_items', 'dummy') }}
)

{{ read_data_lake_folder('DJANGOMART/GET_PURCHASE_ITEMS')}}