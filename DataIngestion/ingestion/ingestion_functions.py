import requests
import duckdb
import datetime
from pathlib import Path 
import pandas as pd

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

    while full_url is not None:    
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(full_url, headers=headers, params=params)
            
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
        
    current_datetime = datetime.datetime.now()
    current_datetime = current_datetime.strftime('%Y%m%d%H%M%S')
    file_name = endpoint + '_' + current_datetime + '.parquet'
    current_dir = Path.cwd()
    file_path = current_dir.parents[1] / "DataLake" / "DjangoMart" / file_name

    # duckdb cannot read directly in memory python objects so an intermediate step is needed
    df = pd.concat(all_data, ignore_index=True)
    with duckdb.connect() as con:
        con.register("object_data", df)
        con.execute(
            f"COPY (SELECT * FROM object_data) TO '{file_path}' (FORMAT PARQUET)"
        )

    return file_name
