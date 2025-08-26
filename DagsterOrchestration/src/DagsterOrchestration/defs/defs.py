import dagster as dg
from .assets import djangomart_purchases, batch_datetime_resource

defs = dg.Definitions(
    assets=[djangomart_purchases],
    resources={
        'batch_datetime_resource': batch_datetime_resource,
    },
)