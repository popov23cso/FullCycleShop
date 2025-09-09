from dagster import define_asset_job, AssetKey

djnagomart_job = define_asset_job(
                                    name='daily_djangomart_job',

                                    # drop selection if i want to run all assets with this job
                                    selection=['get_purchases', 'raw/raw_djangomart_purchases'] 
                                 )

