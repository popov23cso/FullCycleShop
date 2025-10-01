from dagster import op
import duckdb
from pathlib import Path 

@op
def export_models_to_csv(context):
    current_dir = Path.cwd()
    duckdb_database_name = 'duckdb_database.db'
    duckdb_database_path = Path(current_dir.parents[0] / duckdb_database_name)

    output_path = Path(current_dir.parents[1] / 'DataVisualization' / 'ModeledData')

    with duckdb.connect(duckdb_database_path) as con:

        modeled_table_names = con.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'main_modeled';
        """).fetchall()

        for (table_name,) in modeled_table_names:
            csv_file_path = Path(output_path / f'{table_name}.csv')
            query = f"COPY main_modeled.{table_name} TO '{csv_file_path}' (HEADER, DELIMITER ',');"
            con.execute(query)
