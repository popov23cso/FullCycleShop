WITH dummy_dagster_relation AS 
(
    SELECT * FROM {{ source('djangomart_categories', 'dummy') }}
)

{{ read_data_lake_folder('DJANGOMART/GET_CATEGORIES')}}