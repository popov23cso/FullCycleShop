from dagster import define_asset_job

djnagomart_job = define_asset_job(
                                    name='daily_djangomart_job',
                                    selection=['djangomart_purchases'] # drop selection if i want to run all assets with this job
                                 )

