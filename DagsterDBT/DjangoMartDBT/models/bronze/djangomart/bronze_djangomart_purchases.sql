with dummy_dagster_relation as 
(
    select * from {{ source('djangomart', 'dummy_model') }}
)

select 2 as data