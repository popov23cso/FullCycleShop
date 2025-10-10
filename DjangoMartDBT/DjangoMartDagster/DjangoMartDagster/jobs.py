from dagster import define_asset_job, AssetSelection, job
from .ops import export_models_to_csv
from .DataScience.sales_predictions import sequential_sales_prediction

djnagomart_daily_job = define_asset_job(
                                    name='daily_djangomart_job',

                                    # drop selection if i want to run all assets with this job
                                    selection=(AssetSelection.groups('djangomart_api_objects') | AssetSelection.tag('djangomart-dbt', ''))

                                 )
djangomart_ingestion_job = define_asset_job(
                                    name='djangomart_ingestion_job',
                                    selection=(AssetSelection.groups('djangomart_api_objects'))
                                 )


# duckdb does not have a PowerBI connector so data is exported to csv files which power the reports
@job
def export_models_for_reporting():
    export_models_to_csv()

@job
def build_sales_sequential_predictive_model():
    sequential_sales_prediction()