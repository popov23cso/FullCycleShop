import duckdb
import tensorflow as tf
from tensorflow import keras
from pathlib import Path 
from dagster import op
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



current_dir = Path.cwd()
duckdb_database_name = 'duckdb_database.db'
duckdb_database_path = Path(current_dir.parents[2] / duckdb_database_name)

con = duckdb.connect(duckdb_database_path)

daily_sales_data_table = 'main_modeled.djangomart_purchase_summary_daily'
daily_sales_data_query = f"""
SELECT
    *
FROM {daily_sales_data_table}
"""

daily_sales_df = con.execute(daily_sales_data_query).fetch_df()

# split data into two batches - 80% of all data towards training, 20% towards testing
split_size = int(len(daily_sales_df) * 0.8)
training_data = daily_sales_df.iloc[:split_size]
testing_data = daily_sales_df.iloc[split_size:]

X_columns = ['TOTAL_TRANSACTIONS_COUNT', 'DAY_OF_THE_WEEK', 'RECORD_MONTH',
            'RECORD_YEAR', 'IS_WEEKEND', 'LAST_DAY_SALES',
            'LAST_7_DAYS_SALES']
Y_columns = ['TOTAL_TOKENS_SPENT']

training_data_x = training_data[X_columns]
training_data_y = training_data[Y_columns]

testing_data_x = testing_data[X_columns]
testing_data_y = testing_data[Y_columns]

scaler = StandardScaler()

training_data_x_scaled = scaler.fit_transform(training_data_x)
testing_data_x_scaled = scaler.fit_transform(testing_data_x)

# build tensorflow model

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=[training_data_x.shape[1]]),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1) # output will be predicted sales
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

model.fit(
    training_data_x_scaled, training_data_y,
    validation_data=(testing_data_x_scaled, testing_data_y),
    epochs=50,
    batch_size=16
)

test_loss, test_mae = model.evaluate(testing_data_x_scaled, testing_data_y, verbose=1)
print(f"Test Loss (MSE): {test_loss:.2f}")
print(f"Test MAE: {test_mae:.2f}")


