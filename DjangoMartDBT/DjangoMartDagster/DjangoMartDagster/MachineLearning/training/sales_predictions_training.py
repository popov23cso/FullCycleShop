from tensorflow import keras
from tensorflow.keras import layers
from dagster import op
from ..utility import (save_model_and_scaler, get_training_and_testing_data,
                       sequence_training_and_testing_data, log_testing_results)
from ..sales_constants import (TRAINING_YEARS, SEQUENTIAL_MODEL_TYPE, LSTM_MODEL_TYPE)

@op
def train_sales_sequential_prediction_model(context):
    model_input_data, scaler = get_training_and_testing_data(TRAINING_YEARS, SEQUENTIAL_MODEL_TYPE)
    
    # build tensorflow model
    model = keras.Sequential([
        keras.Input(shape=(model_input_data['training_x'].shape[1],)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1) # output will be predicted sales
    ])

    # track mean absolute error. tells on average how far off predictions are 
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(
        model_input_data['training_x'], model_input_data['training_y'],
        validation_data=(model_input_data['testing_x'], model_input_data['testing_y']),
        epochs=500,
        batch_size=32,
        callbacks=[early_stop]
    )

    log_testing_results(context, model, model_input_data)

    model_name = 'daily_sales_sequential_model.keras'
    scaler_name = 'daily_sales_sequential_scaler.pkl'
    save_model_and_scaler(model_name, model, scaler_name, scaler, context)


# LSTM - Long Short-Term Memory 
@op
def train_sales_LSTM_prediction_model(context):
    model_input_data, scaler = get_training_and_testing_data(TRAINING_YEARS, LSTM_MODEL_TYPE)

    window_size = 30
    model_input_data = sequence_training_and_testing_data(model_input_data, window_size)

    model = keras.Sequential([
        keras.Input(shape=(window_size, model_input_data['training_x'].shape[2])),
        layers.LSTM(128, activation='tanh'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1) # output will be predicted sales
    ])

    # track mean absolute error. tells on average how far off predictions are 
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(
        model_input_data['training_x'], model_input_data['training_y'],
        validation_data=(model_input_data['testing_x'], model_input_data['testing_y']),
        epochs=500,
        batch_size=32,
        callbacks=[early_stop]
    )

    log_testing_results(context, model, model_input_data)

    model_name = 'daily_sales_LSTM_model.keras'
    scaler_name = 'daily_sales_LSTM_scaler.pkl'
    
    save_model_and_scaler(model_name, model, scaler_name, scaler, context)



