from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import (DjangoMartDBT_dbt_assets, get_purchases, batch_datetime_resource,
                     get_purchase_items, get_products, get_users, get_categories,
                     get_reviews, predicted_next_week_sales)
from .project import DjangoMartDBT_project
from .schedules import daily_djangomart_schedule
from .jobs import export_models_for_reporting, djangomart_ingestion_job, train_sales_sequential_predictive_model_job

defs = Definitions(
    assets=[DjangoMartDBT_dbt_assets, get_purchases, get_purchase_items,
            get_products, get_users, get_categories, get_reviews,
            predicted_next_week_sales],
    resources={
        'dbt': DbtCliResource(project_dir=DjangoMartDBT_project),
        'batch_datetime_resource': batch_datetime_resource
    },
    schedules=[daily_djangomart_schedule],
    jobs=[export_models_for_reporting, djangomart_ingestion_job,
          train_sales_sequential_predictive_model_job]
)