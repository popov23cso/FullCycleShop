import duckdb
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path 
from dagster import op
from sklearn.preprocessing import StandardScaler
import numpy as np

@op
def train_sales_sequential_prediction_model(context):
    current_dir = Path.cwd()
    duckdb_database_name = 'duckdb_database.db'
    duckdb_database_path = Path(current_dir.parents[0] / duckdb_database_name)

    con = duckdb.connect(duckdb_database_path)

    daily_sales_data_table = 'main_modeled.djangomart_purchase_summary_daily'
    daily_sales_data_query = f"""
    SELECT
        *
    FROM {daily_sales_data_table}
    WHERE RECORD_YEAR IN (2024, 2025)
    """

    daily_sales_df = con.execute(daily_sales_data_query).fetch_df()

    training_data_x, training_data_y, testing_data_x, testing_data_y = split_and_encode_sales_data(daily_sales_df)

    training_data_x_scaled, testing_data_x_scaled = scale_sales_data(training_data_x, testing_data_x)

    # build tensorflow model
    model = keras.Sequential([
        keras.Input(shape=(training_data_x_scaled.shape[1],)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1) # output will be predicted sales
    ])

    # track mean absolute error. tells on average how far off predictions are 
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(
        training_data_x_scaled, training_data_y,
        validation_data=(testing_data_x_scaled, testing_data_y),
        epochs=500,
        batch_size=32,
        callbacks=[early_stop]
    )

    test_loss, test_mae = model.evaluate(testing_data_x_scaled, testing_data_y, verbose=1)

    # mean squared error
    context.log.info(f'Test Loss (MSE): {test_loss:.2f}')

    # mean absolute error - average absolute difference betwee
    # predicted and actual values
    context.log.info(f'Test MAE: {test_mae:.2f}')

    model_name = 'daily_sales_model.keras'
    model_path = Path(current_dir / 'DjangoMartDagster' / 'DataScience' / model_name)
    model.save(model_path)

    context.log.info(f'Model Saved to: {model_path}')

def split_and_encode_sales_data(sales_df):
    # day of week (0-6) and, circular values, tend to confuse models
    # encoding them helps model interpret them better
    sales_df['DAY_SIN'] = np.sin(2 * np.pi * sales_df['DAY_OF_THE_WEEK'] / 7)
    sales_df['DAY_COS'] = np.cos(2 * np.pi * sales_df['DAY_OF_THE_WEEK'] / 7)

    sales_df['MONTH_SIN'] = np.sin(2 * np.pi * (sales_df['RECORD_MONTH']-1) / 12)
    sales_df['MONTH_COS'] = np.cos(2 * np.pi * (sales_df['RECORD_MONTH']-1) / 12)

    # split data into two batches - 80% of all data towards training, 20% towards testing
    # since data is time based no random split is applied
    split_size = int(len(sales_df) * 0.8)
    training_data = sales_df.iloc[:split_size]
    testing_data = sales_df.iloc[split_size:]

    X_columns = ['TOTAL_TRANSACTIONS_COUNT', 'DAY_SIN', 'DAY_COS',
                'IS_WEEKEND', 'LAST_DAY_SALES', 'LAST_7_DAYS_SALES',
                'MONTH_SIN', 'MONTH_COS', 'LAST_14_DAYS_SALES',
                'LAST_30_DAYS_SALES']
    Y_columns = ['TOTAL_TOKENS_SPENT']

    training_data_x = training_data[X_columns]
    training_data_y = training_data[Y_columns]

    testing_data_x = testing_data[X_columns]
    testing_data_y = testing_data[Y_columns]

    return training_data_x, training_data_y, testing_data_x, testing_data_y

def scale_sales_data(training_data_x, testing_data_x):

    # normalize feature values. mean values of 0 with standart 
    # deviation of 1. makes data more consistent, predictable and balanced
    numeric_cols = ['TOTAL_TRANSACTIONS_COUNT', 'LAST_DAY_SALES', 'LAST_7_DAYS_SALES',
                    'LAST_14_DAYS_SALES', 'LAST_30_DAYS_SALES']

    scaler = StandardScaler()

    training_data_x_scaled = training_data_x
    training_data_x_scaled[numeric_cols] = scaler.fit_transform(training_data_x[numeric_cols])

    # apply scaling derived from training data to testing data
    # ensures training and testing data is treated the same
    testing_data_x_scaled = testing_data_x
    testing_data_x_scaled[numeric_cols] = scaler.transform(testing_data_x[numeric_cols])