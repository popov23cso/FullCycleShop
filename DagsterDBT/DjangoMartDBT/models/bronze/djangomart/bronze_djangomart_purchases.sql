with dummy_dagster_relation as 
(
    select * from {{ source('djangomart', 'dummy_model') }}
)

{{ read_data_lake_folder('DJANGOMART/GET_PURCHASES')}}