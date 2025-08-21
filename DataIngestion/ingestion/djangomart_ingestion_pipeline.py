from ingestion_functions import (get_djangomart_auth_tokens, get_djangomart_data)
from api_secrets import DJANGOMART_USERNAME, DJANGOMART_PASSWORD
from pathlib import Path
import json
import datetime


current_dir = Path.cwd()

metadata_file_name = 'django_mart_tables.json'
metadata_file_path = current_dir.parents[0] / 'metadata' / metadata_file_name

with open(metadata_file_path, 'r') as metadata_file:
    metadata = json.load(metadata_file)


for i, source in enumerate(metadata['sources']):
    source_name = source['name']
    if source_name == 'djangomart':
        batch_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')
        # TODO Add exception handling and logging
        for j, obj in enumerate(source['objects']):
            refresh_token, access_token = get_djangomart_auth_tokens(DJANGOMART_USERNAME, DJANGOMART_PASSWORD)

            endpoint_name = obj['name']
            delta_dtt = obj['last_ingestion_dtt']
            get_djangomart_data(access_token, refresh_token, endpoint_name, delta_dtt)

            metadata['sources'][i]['objects'][j] = batch_datetime



