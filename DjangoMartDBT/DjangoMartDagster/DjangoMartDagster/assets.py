from dagster import AssetExecutionContext, resource, asset
from dagster_dbt import DbtCliResource, dbt_assets

from .project import DjangoMartDBT_project
from .ingestion_functions import ingest_djangomart_data

import datetime

DJANGOMART_ASSET_METADATA = {
    'api': 'djangomart',
    'owner': 'djangomart data platform_team',
    'delta_metadata_file_name': 'django_mart_tables.json'
}

@dbt_assets(manifest=DjangoMartDBT_project.manifest_path)
def DjangoMartDBT_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

@resource()
def batch_datetime_resource(_):
    return datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')

@asset(
        required_resource_keys={'batch_datetime_resource'},
        group_name='djangomart_api_objects',
        description='Fetches djangomart purchase data and saves it to a parquet file in the data lake',
        metadata=DJANGOMART_ASSET_METADATA
        )
def get_purchases(context):
    endpoint_name = 'get_purchases'
    return ingest_djangomart_data(endpoint_name, context.resources.batch_datetime_resource, context.log)

@asset(
        required_resource_keys={'batch_datetime_resource'},
        group_name='djangomart_api_objects',
        description='Fetches djangomart purchase items data and saves it to a parquet file in the data lake',
        metadata=DJANGOMART_ASSET_METADATA
        )
def get_purchase_items(context):
    endpoint_name = 'get_purchase_items'
    return ingest_djangomart_data(endpoint_name, context.resources.batch_datetime_resource, context.log)

@asset(
        required_resource_keys={'batch_datetime_resource'},
        group_name='djangomart_api_objects',
        description='Fetches djangomart product data and saves it to a parquet file in the data lake',
        metadata=DJANGOMART_ASSET_METADATA
        )
def get_products(context):
    endpoint_name = 'get_products'
    return ingest_djangomart_data(endpoint_name, context.resources.batch_datetime_resource, context.log)

@asset(
        required_resource_keys={'batch_datetime_resource'},
        group_name='djangomart_api_objects',
        description='Fetches djangomart user data and saves it to a parquet file in the data lake',
        metadata=DJANGOMART_ASSET_METADATA
        )
def get_users(context):
    endpoint_name = 'get_users'
    return ingest_djangomart_data(endpoint_name, context.resources.batch_datetime_resource, context.log)

@asset(
        required_resource_keys={'batch_datetime_resource'},
        group_name='djangomart_api_objects',
        description='Fetches djangomart category data and saves it to a parquet file in the data lake',
        metadata=DJANGOMART_ASSET_METADATA
        )
def get_categories(context):
    endpoint_name = 'get_categories'
    return ingest_djangomart_data(endpoint_name, context.resources.batch_datetime_resource, context.log)

@asset(
        required_resource_keys={'batch_datetime_resource'},
        group_name='djangomart_api_objects',
        description='Fetches djangomart review data and saves it to a parquet file in the data lake',
        metadata=DJANGOMART_ASSET_METADATA
        )
def get_reviews(context):
    endpoint_name = 'get_reviews'
    return ingest_djangomart_data(endpoint_name, context.resources.batch_datetime_resource, context.log)


    