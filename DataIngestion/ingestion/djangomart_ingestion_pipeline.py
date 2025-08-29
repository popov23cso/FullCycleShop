from ingestion_functions import (get_djangomart_auth_tokens, get_djangomart_data)
from api_secrets import DJANGOMART_USERNAME, DJANGOMART_PASSWORD
from pathlib import Path
import json
import datetime
import logging 
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('djangomart_log.log', mode='a')

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add custom handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


current_dir = Path.cwd()
metadata_file_name = 'django_mart_tables.json'
metadata_file_path = current_dir.parents[0] / 'metadata' / metadata_file_name

with open(metadata_file_path, 'r') as metadata_file:
    metadata = json.load(metadata_file)


for i, source in enumerate(metadata['sources']):
    source_name = source['name']
    if source_name == 'djangomart':
        batch_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')
        logger.info('Starting ingestion for djangomart batch %s', batch_datetime)
        for j, obj in enumerate(source['objects']):
            endpoint_name = obj['name']
            delta_dtt = obj['last_ingestion_dtt']

            logger.info('Starting ingestion for %s object', endpoint_name)

            try:
                refresh_token, access_token = get_djangomart_auth_tokens(DJANGOMART_USERNAME, DJANGOMART_PASSWORD)
            except Exception:
                logger.exception('Exception occured during retrieval of auth tokens for user %s', DJANGOMART_USERNAME)

            try:
                get_djangomart_data(access_token, refresh_token, endpoint_name, delta_dtt)
                logger.info('Succesfully ingested %s object', endpoint_name)
                object_metadata = {
                    'name': endpoint_name,
                    'last_ingestion_dtt': batch_datetime
                }
                metadata['sources'][i]['objects'][j] = object_metadata
            except Exception:
                logger.exception('Exception occured during ingestion of %s object', endpoint_name)


# save updated timestamps
with open(metadata_file_path, 'w') as metadata_file:
    json.dump(metadata, metadata_file, indent=4)


