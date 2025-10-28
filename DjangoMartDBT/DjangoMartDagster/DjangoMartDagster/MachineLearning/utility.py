from sklearn.preprocessing import StandardScaler
import numpy as np
from joblib import dump, load
from pathlib import Path 
from tensorflow import keras
import duckdb
from ..common_constants import DBT_DUCKDB_DATABASE_NAME
from .sales_constants import MODEL_COLUMN_MAPPER


def encode_sales_data(sales_df, model_type):
    # day of week (0-6) and, circular values, tend to confuse models
    # encoding them helps model interpret them better
    sales_df['DAY_SIN'] = np.sin(2 * np.pi * sales_df['DAY_OF_THE_WEEK'] / 7)
    sales_df['DAY_COS'] = np.cos(2 * np.pi * sales_df['DAY_OF_THE_WEEK'] / 7)

    sales_df['MONTH_SIN'] = np.sin(2 * np.pi * (sales_df['RECORD_MONTH']-1) / 12)
    sales_df['MONTH_COS'] = np.cos(2 * np.pi * (sales_df['RECORD_MONTH']-1) / 12)

    sales_df_x = sales_df[MODEL_COLUMN_MAPPER[model_type]['X_COLUMNS']].copy()
    sales_df_y = sales_df[MODEL_COLUMN_MAPPER[model_type]['Y_COLUMNS']].copy()
        
    return sales_df_x, sales_df_y

def encode_and_split_sales_data(sales_df, model_type):

    sales_df_x, sales_df_y = encode_sales_data(sales_df, model_type)
    # split data into two batches - 80% of all data towards training, 20% towards testing
    # since data is time based no random split is applied
    split_size = int(len(sales_df) * 0.8)

    training_data_x = sales_df_x.iloc[:split_size]
    testing_data_x = sales_df_x.iloc[split_size:]

    training_data_y = sales_df_y.iloc[:split_size]
    testing_data_y = sales_df_y.iloc[split_size:]

    return training_data_x, training_data_y, testing_data_x, testing_data_y

# normalize feature values. mean values of 0 with standart 
# deviation of 1. makes data more consistent, predictable and balanced
def fit_sales_scaler(x_data, model_type):
    scaler = StandardScaler()
    scaler.fit(x_data[MODEL_COLUMN_MAPPER[model_type]['NUMERIC_COLUMNS']])
    return scaler 

# scale passed x data using an already fitted scaler
def scale_sales_data(x_data, scaler, model_type):
    x_data[MODEL_COLUMN_MAPPER[model_type]['NUMERIC_COLUMNS']] = scaler.transform(x_data[MODEL_COLUMN_MAPPER[model_type]['NUMERIC_COLUMNS']])
    return x_data

def save_model_and_scaler(model_name, model, scaler_name, scaler, dagster_context):
    current_dir = Path.cwd()
    model_path = Path(current_dir / 'DjangoMartDagster' / 'MachineLearning' / 'models' / model_name)
    scaler_path = Path(current_dir / 'DjangoMartDagster' / 'MachineLearning' / 'scalers' / scaler_name)

    model.save(model_path)
    dump(scaler, scaler_path)

    dagster_context.log.info(f'Model saved to: {model_path}')
    dagster_context.log.info(f'Scaler saved to: {scaler_path}')

def retreive_model_and_scaler(model_name, scaler_name):
    current_dir = Path.cwd()
    model_path = Path(current_dir / 'DjangoMartDagster' / 'MachineLearning' /'models' / model_name)
    model = keras.models.load_model(model_path)
    scaler_path = Path(current_dir / 'DjangoMartDagster' / 'MachineLearning' /'scalers' / scaler_name)
    scaler = load(scaler_path)

    return model, scaler

def get_training_daily_sales_data_years(target_years):
    target_years_sql_string = ','.join(map(str, target_years))

    current_dir = Path.cwd()
    duckdb_database_path = Path(current_dir.parents[0] / DBT_DUCKDB_DATABASE_NAME)
    with duckdb.connect(duckdb_database_path) as con:
        daily_sales_data_table = 'main_modeled.djangomart_purchase_summary_daily'
        daily_sales_data_query = f"""
        SELECT
            *
        FROM {daily_sales_data_table}
        WHERE RECORD_YEAR IN ({target_years_sql_string})
        """

        daily_sales_df = con.execute(daily_sales_data_query).fetch_df()

    return daily_sales_df

def create_time_sequences(x_data, y_data, window_size):
    x_sequences, y_sequences = [], []
    for i in range(len(x_data) - window_size):
        x_sequences.append(x_data[i:(i + window_size)].values)
        y_sequences.append(y_data.iloc[i + window_size])
    return np.array(x_sequences), np.array(y_sequences)

def get_training_and_testing_data(training_years, model_type):
    daily_sales_df = get_training_daily_sales_data_years(training_years)
    training_data_x, training_data_y, testing_data_x, testing_data_y = encode_and_split_sales_data(daily_sales_df, model_type)

    scaler = fit_sales_scaler(training_data_x, model_type)
    training_data_x_scaled = scale_sales_data(training_data_x, scaler, model_type)
    testing_data_x_scaled = scale_sales_data(testing_data_x, scaler, model_type)

    model_input_data = {}
    model_input_data['training_x'] = training_data_x_scaled
    model_input_data['training_y'] = training_data_y
    model_input_data['testing_x'] = testing_data_x_scaled
    model_input_data['testing_y'] = testing_data_y

    return model_input_data, scaler

def sequence_training_and_testing_data(model_input_data, window_size):
    training_data_x_sequenced, training_data_y_sequenced = create_time_sequences(model_input_data['training_x'],
                                                                                model_input_data['training_y'],
                                                                                window_size) 
    
    testing_data_x_sequenced, testing_data_y_sequenced = create_time_sequences(model_input_data['testing_x'],
                                                                                model_input_data['testing_y'],
                                                                                window_size) 
    
    model_input_data['training_x'] = training_data_x_sequenced
    model_input_data['training_y'] = training_data_y_sequenced

    model_input_data['testing_x'] = testing_data_x_sequenced
    model_input_data['testing_y'] = testing_data_y_sequenced

    return model_input_data

def log_testing_results(context, model, model_input_data):
    test_loss, test_mae = model.evaluate(model_input_data['testing_x'], model_input_data['testing_y'], verbose=1)

    # mean squared error
    context.log.info(f'Test Loss (MSE): {test_loss:.2f}')

    # mean absolute error - average absolute difference between
    # predicted and actual values
    context.log.info(f'Test MAE: {test_mae:.2f}')