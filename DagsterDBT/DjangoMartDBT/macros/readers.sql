{% macro read_data_lake_folder(folder_path) %}
    SELECT * FROM '{{ var("DATA_LAKE_PATH") ~ folder_path ~ "/*.parquet"}}'
{% endmacro %}
