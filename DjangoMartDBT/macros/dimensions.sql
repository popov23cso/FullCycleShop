-- use this macro to generate a slowly changing dimension of type 2
-- important note: this is best used for star schema dimensions 
-- (dimensions that do not join with other dimensions)
-- if you use it on a snowflake schema dimension changes in the other dimensions wont reflect in your scd2 logic
-- (no new rows will be inserted when a joined dimension adds a new row). Use if dimension is in star schema
-- or the changes in the other dimension are not of business importance
{% macro star_schema_scd2(relation_name, id_column, delta_column='DWH_BATCH_DATETIME') %}
    WITH delta_row_numbers AS 
    (
        SELECT 
            r.*,
            ROW_NUMBER() OVER (PARTITION BY {{id_column}} ORDER BY {{delta_column}}) AS row_number,
            LEAD({{delta_column}}) OVER (PARTITION BY {{id_column}} ORDER BY {{delta_column}}) AS next_delta
        FROM {{ ref(relation_name) }} r

        {% if is_incremental() %}
            -- only pull new/changed rows
            WHERE {{delta_column}} > COALESCE((SELECT max({{delta_column}}) FROM {{ this }}), {{var('BEGINNING_OF_TIME')}})
        {% endif %}
    )
    SELECT 
        r.*,
        CASE
            WHEN row_number = 1 THEN {{var('BEGINNING_OF_TIME')}}
            ELSE {{delta_column}}
        END AS DWH_EFFECTIVE_FROM,
        CASE 
            WHEN DWH_IS_LATEST = 1 THEN {{var('END_OF_TIME')}}
            ELSE next_delta
        END AS DWH_EFFECTIVE_TO
    FROM delta_row_numbers r

{% endmacro%}