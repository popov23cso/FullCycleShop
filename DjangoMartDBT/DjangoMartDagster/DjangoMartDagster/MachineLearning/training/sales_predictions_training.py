from tensorflow import keras
from tensorflow.keras import layers
from dagster import op
from ..utility import (encode_and_split_sales_data, fit_sales_scaler, scale_sales_data,
                      save_model_and_scaler, get_training_daily_sales_data_years,
                      create_time_sequences)

TRAINING_YEARS = [2024, 2025]

@op
def train_sales_sequential_prediction_model(context):
    daily_sales_df = get_training_daily_sales_data_years(TRAINING_YEARS)

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


# LSTM - Long Short-Term Memory 
@op
def train_sales_LSTM_prediction_model(context):
    daily_sales_df = get_training_daily_sales_data_years(TRAINING_YEARS)

    training_data_x, training_data_y, testing_data_x, testing_data_y = encode_and_split_sales_data(daily_sales_df)

    scaler = fit_sales_scaler(training_data_x)

    training_data_x_scaled = scale_sales_data(training_data_x, scaler)
    testing_data_x_scaled = scale_sales_data(testing_data_x, scaler)

    window_size = 14

    training_data_x_sequenced, training_data_y_sequenced = create_time_sequences(training_data_x_scaled, training_data_y, window_size) 
    testing_data_x_sequenced, testing_data_y_sequenced = create_time_sequences(testing_data_x_scaled, testing_data_y, window_size) 

    # build tensorflow model
    model = keras.Sequential([
        layers.LSTM(64, activation='tanh', input_shape=(window_size, training_data_x_sequenced.shape[2])),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1) # output will be predicted sales
    ])

    # track mean absolute error. tells on average how far off predictions are 
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(
        training_data_x_sequenced, training_data_y_sequenced,
        validation_data=(testing_data_x_sequenced, testing_data_y_sequenced),
        epochs=500,
        batch_size=32,
        callbacks=[early_stop]
    )

    test_loss, test_mae = model.evaluate(testing_data_x_sequenced, testing_data_y_sequenced, verbose=1)

    # mean squared error
    context.log.info(f'Test Loss (MSE): {test_loss:.2f}')

    # mean absolute error - average absolute difference between
    # predicted and actual values
    context.log.info(f'Test MAE: {test_mae:.2f}')

    model_name = 'daily_sales_LSTM_model.keras'
    scaler_name = 'daily_sales_LSTM_scaler.pkl'
    
    save_model_and_scaler(model_name, model, scaler_name, scaler, context)



