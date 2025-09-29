from dagster import define_asset_job, AssetSelection

djnagomart_job = define_asset_job(
                                    name='daily_djangomart_job',

                                    # drop selection if i want to run all assets with this job
                                    selection=(AssetSelection.groups('djangomart_api_objects') | AssetSelection.tag('djangomart-dbt', ''))
                                 )

