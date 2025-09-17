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


{% macro historize_relation(relation_name, id_column) %}

    WITH relation_ranked AS 
    (
        SELECT
            r.*,
            ROW_NUMBER() OVER (PARTITION BY {{id_column}} ORDER BY DWH_BATCH_DATETIME DESC) as row_rank
        FROM {{ ref(relation_name) }} r

        {% IF is_incremental() %}
        -- only pull new/changed rows
            WHERE DWH_BATCH_DATETIME > COALESCE((SELECT max(DWH_BATCH_DATETIME) FROM {{ this }}), {{var('BEGINNING_OF_TIME')}})
        {% endif %}
    )
    SELECT 
        CONCAT({{id_column}}, '_', DWH_BATCH_DATETIME_STR) AS DWH_SK,
        r.*,
        CASE
            WHEN row_rank = 1 THEN 1
            ELSE 0 
        END AS DWH_IS_LATEST
    FROM relation_ranked r

{% endmacro %}
