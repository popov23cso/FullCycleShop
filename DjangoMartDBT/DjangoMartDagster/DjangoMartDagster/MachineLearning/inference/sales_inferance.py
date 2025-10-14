import duckdb
import pandas as pd
from pathlib import Path
from tensorflow import keras
from datetime import timedelta

import numpy as np

def encode_sales_data(sales_df):
    # day of week (0-6) and, circular values, tend to confuse models
    # encoding them helps model interpret them better
    sales_df['DAY_SIN'] = np.sin(2 * np.pi * sales_df['DAY_OF_THE_WEEK'] / 7)
    sales_df['DAY_COS'] = np.cos(2 * np.pi * sales_df['DAY_OF_THE_WEEK'] / 7)

    sales_df['MONTH_SIN'] = np.sin(2 * np.pi * (sales_df['RECORD_MONTH']-1) / 12)
    sales_df['MONTH_COS'] = np.cos(2 * np.pi * (sales_df['RECORD_MONTH']-1) / 12)

    X_columns = ['TOTAL_TRANSACTIONS_COUNT', 'DAY_SIN', 'DAY_COS',
                'IS_WEEKEND', 'LAST_DAY_SALES', 'LAST_7_DAYS_SALES',
                'MONTH_SIN', 'MONTH_COS', 'LAST_14_DAYS_SALES',
                'LAST_30_DAYS_SALES']
    Y_columns = ['TOTAL_TOKENS_SPENT']

    sales_df_x = sales_df[X_columns]
    sales_df_y = sales_df[Y_columns]

    return sales_df_x, sales_df_y

def infer_sales_with_model(model_name):

    current_dir = Path.cwd()
    duckdb_database_name = 'duckdb_database.db'
    duckdb_database_path = Path(current_dir.parents[3] / duckdb_database_name)

    with duckdb.connect(duckdb_database_path) as con:
        daily_sales_data_table = 'main_modeled.djangomart_purchase_summary_daily'
        daily_sales_data_query = f"""
        SELECT
            *
        FROM {daily_sales_data_table}
        ORDER BY GENERATED_DAY DESC
        LIMIT 14
        """ 

        last_two_weeks_data = con.execute(daily_sales_data_query).fetch_df()

    model_path = Path(current_dir.parents[0] / 'models' / model_name)
    model = keras.models.load_model(model_path)

    predicted_rows = pd.DataFrame()
    last_total
    for i, row in last_two_weeks_data.iterrows():
        next_day_row = row.copy()
        next_day_row['GENERATED_DAY'] = row['GENERATED_DAY'] + timedelta(days=1)
        next_day_row['LAST_7_DAYS_SALES'] = row['LAST_7_DAYS_SALES'] + row['TOTAL_TOKENS_SPENT']
        next_day_row['LAST_14_DAYS_SALES'] = row['LAST_14_DAYS_SALES'] + row['TOTAL_TOKENS_SPENT']
        next_day_row['LAST_30_DAYS_SALES'] = row['LAST_30_DAYS_SALES'] + row['TOTAL_TOKENS_SPENT']

infer_sales_with_model('daily_sales_sequential_model.keras')
