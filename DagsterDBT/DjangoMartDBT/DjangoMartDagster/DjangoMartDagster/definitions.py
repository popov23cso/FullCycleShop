from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import (DjangoMartDBT_dbt_assets, get_purchases, batch_datetime_resource,
                     get_purchase_items)
from .project import DjangoMartDBT_project
from .schedules import schedules, daily_djangomart_schedule

defs = Definitions(
    assets=[DjangoMartDBT_dbt_assets, get_purchases, get_purchase_items],
    resources={
        'dbt': DbtCliResource(project_dir=DjangoMartDBT_project),
        'batch_datetime_resource': batch_datetime_resource
    },
    schedules=[daily_djangomart_schedule]
)