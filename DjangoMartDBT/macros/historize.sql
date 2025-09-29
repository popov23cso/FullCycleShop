{% macro dedupe_relation(relation_name, dedupe_columns, delta_column) %}

    SELECT 
        *
    FROM {{ ref(relation_name) }}
    QUALIFY ROW_NUMBER() OVER 
    (
        PARTITION BY {{dedupe_columns}}
        ORDER BY {{dedupe_columns}} DESC
    ) = 1;

{% endmacro%}


{% macro historize_relation(relation_name, id_column, delta_column='DWH_BATCH_DATETIME') %}

    WITH relation_ranked AS 
    (
        SELECT
            r.*,
            ROW_NUMBER() OVER (PARTITION BY {{id_column}} ORDER BY {{delta_column}} DESC) as row_rank
        FROM {{ ref(relation_name) }} r

        {% if is_incremental() %}
            -- only pull new/changed rows
            WHERE {{delta_column}} > COALESCE((SELECT max({{delta_column}}) FROM {{ this }}), {{var('BEGINNING_OF_TIME')}})
        {% endif %}
    )
    SELECT 
        -- generate a surrogate key
        CONCAT({{id_column}}, '_', DWH_BATCH_DATETIME_STR) AS DWH_SK,
        r.*,
        CASE
            WHEN row_rank = 1 THEN 1
            ELSE 0 
        END AS DWH_IS_LATEST
    FROM relation_ranked r

{% endmacro %}
