{% macro read_data_lake_folder(folder_path) %}
    SELECT 
        *,
        filename AS DWH_FILE_PATH,
        substring
        (    
            filename
            from length(filename) - 7 - 14
            for 13
        ) AS DWH_BATCH_DATETIME
    FROM read_parquet('{{ var("DATA_LAKE_PATH") ~ folder_path ~ "/*.parquet"}}', union_by_name => TRUE)
{% endmacro %}


{% macro list_raw_metadata() %}
    DWH_BATCH_DATETIME AS DWH_BATCH_DATETIME_STR,
    strptime(DWH_BATCH_DATETIME, '%Y%m%d%H%M%S')::TIMESTAMP AS DWH_BATCH_DATETIME,
    strptime(DWH_BATCH_DATETIME, '%Y%m%d%H%M%S')::DATE AS DWH_BATCH_DATE,
{% endmacro %}