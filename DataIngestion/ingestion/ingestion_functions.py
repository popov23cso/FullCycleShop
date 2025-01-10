import pandas
import sqlite3
from pathlib import Path
import json
import datetime
import pandas as pd

def ingest_sqlite3_data(metadata_file_name):
    metadata_path = Path(__file__).resolve().parent.parent / 'metadata' / metadata_file_name
    if not metadata_path.exists():
        raise FileNotFoundError(f'Metadata file not found at {metadata_path}')
    
    metadata = None
    with open(metadata_path, 'r') as metadata_file:
        metadata = json.load(metadata_file)

    db_path = Path(__file__).resolve().parent.parent.parent / 'DjangoMart' / metadata['database_name']
    if not db_path.exists():
        raise FileNotFoundError(f'Database file not found at {db_path}')
    
    ingestion_start_dtt = datetime.datetime.now()
    
    db_connection = sqlite3.connect(db_path)

    for i, table in enumerate(metadata['tables']):
        ingest_sqlite3_table(table, db_connection, ingestion_start_dtt)
        metadata['tables'][i]['last_ingestion_dtt'] = str(ingestion_start_dtt)

    with open(metadata_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)
    db_connection.close()


def ingest_sqlite3_table(table, db_connection, ingestion_start_dtt):
    query = f"SELECT * FROM {table['name']} WHERE last_modified_date > '{table['last_ingestion_dtt']}'"
    df = pd.read_sql_query(query, db_connection)
    if len(df) > 0:
        file_name = table['name'] + '_' + ingestion_start_dtt.strftime('%Y%m%d%H%M%S') + '.parquet'
        
        file_path = Path(__file__).resolve().parent.parent.parent / 'DataLake' / 'SQLite3' / table['name'] / file_name
        df.to_parquet(file_path, engine='pyarrow', index=False)

ingest_sqlite3_data('tables.json')