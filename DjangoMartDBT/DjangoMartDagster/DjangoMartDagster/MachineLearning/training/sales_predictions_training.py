import duckdb
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path 
from dagster import op
from ..utility import (encode_and_split_sales_data, fit_sales_scaler, scale_sales_data,
                      save_model_and_scaler)
from joblib import dump
from ...common_constants import DBT_DUCKDB_DATABASE_NAME

@op
def train_sales_sequential_prediction_model(context):
    current_dir = Path.cwd()
    duckdb_database_path = Path(current_dir.parents[0] / DBT_DUCKDB_DATABASE_NAME)

    with duckdb.connect(duckdb_database_path) as con:
        daily_sales_data_table = 'main_modeled.djangomart_purchase_summary_daily'
        daily_sales_data_query = f"""
        SELECT
            *
        FROM {daily_sales_data_table}
        WHERE RECORD_YEAR IN (2024, 2025)
        """

        daily_sales_df = con.execute(daily_sales_data_query).fetch_df()

    training_data_x, training_data_y, testing_data_x, testing_data_y = encode_and_split_sales_data(daily_sales_df)

    scaler = fit_sales_scaler(training_data_x)

    training_data_x_scaled = scale_sales_data(training_data_x, scaler)
    testing_data_x_scaled = scale_sales_data(testing_data_x, scaler)

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

    # mean absolute error - average absolute difference between
    # predicted and actual values
    context.log.info(f'Test MAE: {test_mae:.2f}')

    model_name = 'daily_sales_sequential_model.keras'
    scaler_name = 'daily_sales_sequential_scaler.pkl'
    
    save_model_and_scaler(model_name, model, scaler_name, scaler, context)