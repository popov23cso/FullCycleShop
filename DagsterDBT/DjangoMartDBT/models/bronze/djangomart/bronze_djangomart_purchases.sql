WITH dummy_dagster_relation AS 
(
    SELECT * FROM {{ source('djangomart', 'dummy_model') }}
)

{{ read_data_lake_folder('DJANGOMART/GET_PURCHASES')}}