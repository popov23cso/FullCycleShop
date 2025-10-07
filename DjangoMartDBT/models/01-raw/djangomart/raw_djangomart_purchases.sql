WITH dummy_dagster_relation AS 
(
    SELECT * FROM {{ source('djangomart_purchases', 'dummy') }}
)

{{ read_data_lake_folder('DJANGOMART/GET_PURCHASES')}}