import dagster as dg
from .ingestion_functions import ingest_djangomart_data
import datetime




@dg.resource()
def batch_datetime_resource(_):
    return datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')


@dg.asset(required_resource_keys={'batch_datetime_resource'})
def djangomart_purchases(context):
    endpoint_name = 'get_purchases'
    return ingest_djangomart_data(endpoint_name, context.resources.batch_datetime_resource)

