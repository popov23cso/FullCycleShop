import requests
import duckdb
import datetime
from pathlib import Path 
import pandas as pd
from .api_secrets import DJANGOMART_USERNAME, DJANGOMART_PASSWORD
import json
from dagster import Failure
from filelock import FileLock
from ..common_constants import DAGSTER_PROJECT_NAME


def get_djangomart_auth_tokens(username, password):
    token_url = 'http://127.0.0.1:8000/api/token/'
    request_body = {
        'username':username,
        'password':password
    }
    try:
        response = requests.post(token_url, json=request_body)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error while requesting token server: {e}")
    
    data = response.json()
    if 'access' not in data or 'refresh' not in data:
        raise ValueError(f"Unexpected response format while retrieving auth tokens: {data}")
    
    return data['refresh'], data['access']


def refresh_access_token(refresh_token):
    token_url = 'http://127.0.0.1:8000/api/token/refresh/'
    request_body = {
        'refresh':refresh_token,
    }
    try:
        response = requests.post(token_url, json=request_body)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error while requesting access token from token server: {e}")
    
    data = response.json()
    if 'access' not in data:
        raise ValueError(f"Unexpected response format while retrieving access token: {data}")
    
    return data['access']

def get_djangomart_data(access_token, refresh_token, endpoint, updated_after):
    base_url = 'http://127.0.0.1:8000/'
    full_url = base_url + endpoint    
    params = {
        'updated_after': updated_after
    }

    all_data = []
    initial = True

    while full_url is not None:    
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            if initial:
                response = requests.get(full_url, headers=headers, params=params)
                initial = False
            else:
                response = requests.get(full_url, headers=headers)

            
            if response.status_code == 401:
                try: 
                    access_token = refresh_access_token(refresh_token)
                except ValueError as e: 
                    raise RuntimeError(f'Error while requesting a new access token: {e}')
                
                continue

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error while requesting {endpoint} data: {e}")
        
        response_data = response.json()
        if response_data['success']:
            df = pd.DataFrame(response_data['data']['results'])
            all_data.append(df)
        else:
            return None 
        
        full_url = response_data['data']['next']
        
    df = pd.concat(all_data, ignore_index=True)
    if len(df) > 0:
        current_datetime = datetime.datetime.now()
        current_datetime = current_datetime.strftime('%Y%m%d%H%M%S')
        file_name = endpoint.upper() + '_' + current_datetime + '.parquet'
        current_dir = Path.cwd()

        folder_path = Path(current_dir.parents[1] / "DataLake" / "DjangoMart" / endpoint.upper())
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / file_name

        # duckdb cannot read directly in memory python objects so an intermediate step is needed
        with duckdb.connect() as con:
            con.register("object_data", df)

            con.execute(
                f"COPY (SELECT * FROM object_data) TO '{file_path}' (FORMAT PARQUET)"
            )

        return file_name


def ingest_djangomart_data(endpoint_name, batch_datetime, log):
    current_dir = Path.cwd()
    metadata_file_name = 'django_mart_tables.json'
    metadata_file_path = current_dir / DAGSTER_PROJECT_NAME / 'Metadata' /  metadata_file_name

    with open(metadata_file_path, 'r') as metadata_file:
        metadata = json.load(metadata_file)

    delta_dtt = metadata[endpoint_name]['last_ingestion_dtt']

    log.info(f'Starting ingestion for {endpoint_name} object')

    try:
        refresh_token, access_token = get_djangomart_auth_tokens(DJANGOMART_USERNAME, DJANGOMART_PASSWORD)
    except Exception:
        raise Failure(description=f'Exception occured during retrieval of auth tokens for user {DJANGOMART_USERNAME}')

    try:
        get_djangomart_data(access_token, refresh_token, endpoint_name, delta_dtt)
        log.info(f'Succesfully ingested {endpoint_name} object')
        delta_dtt = batch_datetime
    except Exception:
        raise Failure(f'Exception occured during ingestion of {endpoint_name} object')

    with FileLock(str(metadata_file_path) + '.lock'):
        
        with open(metadata_file_path, 'r+') as metadata_file:
            metadata = json.load(metadata_file)
            metadata[endpoint_name]['last_ingestion_dtt'] = delta_dtt

            # move file pointer at file beggining
            metadata_file.seek(0)

            # paste new data in and truncate everything after the new data
            json.dump(metadata, metadata_file, indent=4)
            metadata_file.truncate()
