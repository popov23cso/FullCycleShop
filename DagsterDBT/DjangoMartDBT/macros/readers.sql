{% macro read_djangomart_folder(folder_name) %}
    {% set base_folder_path = '' %}
    SELECT * FROM 'path/to/folder/*.parquet'
{% endmacro %}
