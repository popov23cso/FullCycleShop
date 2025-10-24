import duckdb
import pandas as pd
from pathlib import Path
from tensorflow import keras
from datetime import timedelta

import numpy as np
from ..utility import encode_sales_data, scale_sales_data, retreive_model_and_scaler
from ...common_constants import DBT_DUCKDB_DATABASE_NAME

def infer_sales_with_model(model_name, scaler_name):
    current_dir = Path.cwd()
    duckdb_database_path = Path(current_dir.parents[0] / DBT_DUCKDB_DATABASE_NAME)

    con = duckdb.connect(duckdb_database_path)
    daily_sales_data_table = 'main_modeled.djangomart_purchase_summary_daily'
    daily_sales_data_query = f"""
    SELECT
        *
    FROM {daily_sales_data_table}
    ORDER BY GENERATED_DAY DESC
    LIMIT 30
    """ 

    last_month_sales_data = con.execute(daily_sales_data_query).fetch_df()

    model, scaler = retreive_model_and_scaler(model_name, scaler_name)

    predicted_rows = pd.DataFrame()
    day_index_30 = 29
    day_index_14 = 13
    day_index_7 = 6
    last_total_tokens_spent = last_month_sales_data.iloc[0]['TOTAL_TOKENS_SPENT']
    last_date = last_month_sales_data.iloc[0]['GENERATED_DAY']

    for i in last_month_sales_data.tail(7).index:
        row = last_month_sales_data.loc[[i]] 
        next_day_row = last_month_sales_data.loc[[i]] 

        next_date = last_date + timedelta(days=1)
        day_of_week = next_date.isoweekday()  
        record_month = next_date.month   

        # set the fields for the next day that total tokens spent will be estimated for
        next_day_row['DAY_OF_THE_WEEK'] = day_of_week
        next_day_row['IS_WEEKEND'] = 1 if day_of_week in (6, 7) else 0
        next_day_row['RECORD_MONTH'] = record_month
        next_day_row['LAST_7_DAYS_SALES'] = row['LAST_7_DAYS_SALES'] + last_total_tokens_spent - last_month_sales_data.iloc[day_index_7]['TOTAL_TOKENS_SPENT']
        next_day_row['LAST_14_DAYS_SALES'] = row['LAST_14_DAYS_SALES'] + last_total_tokens_spent - last_month_sales_data.iloc[day_index_14]['TOTAL_TOKENS_SPENT']
        next_day_row['LAST_30_DAYS_SALES'] = row['LAST_30_DAYS_SALES'] + last_total_tokens_spent - last_month_sales_data.iloc[day_index_30]['TOTAL_TOKENS_SPENT']
        next_day_row['TOTAL_TRANSACTIONS_COUNT'] = last_month_sales_data.iloc[day_index_7]['TOTAL_TRANSACTIONS_COUNT']
        
        encoded_data, _ = encode_sales_data(next_day_row)

        encoded_data = scale_sales_data(encoded_data, scaler)

        predicted_total_tokens_spent = model.predict(encoded_data)
        predicted_total_tokens_spent = predicted_total_tokens_spent.item()

        day_index_30 -= 1
        day_index_14 -= 1
        day_index_7 -= 1
        last_total_tokens_spent = predicted_total_tokens_spent
        last_date = next_date

        predicted_row = pd.DataFrame({
            'GENERATED_DAY': [next_date],
            'TOTAL_TOKENS_SPENT': [predicted_total_tokens_spent]
        })

        predicted_rows = pd.concat([predicted_rows, predicted_row], ignore_index=True)

    
    inferred_schema_name = 'main_inferred'
    inferred_table_name = 'inferred_djangomart_purchase_summary_daily'
    
    con.execute(f'CREATE SCHEMA IF NOT EXISTS {inferred_schema_name}')

    con.execute(f'DROP TABLE IF EXISTS {inferred_schema_name}.{inferred_table_name}')
    con.execute(f'CREATE TABLE {inferred_schema_name}.{inferred_table_name} AS SELECT * FROM predicted_rows')
    con.close()
