from sklearn.preprocessing import StandardScaler
import numpy as np

NUMERIC_SALES_COLUMNS = ['TOTAL_TRANSACTIONS_COUNT', 'LAST_DAY_SALES', 'LAST_7_DAYS_SALES',
                    'LAST_14_DAYS_SALES', 'LAST_30_DAYS_SALES']

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

    sales_df_x = sales_df[X_columns].copy()
    sales_df_y = sales_df[Y_columns].copy()

    return sales_df_x, sales_df_y

def encode_and_split_sales_data(sales_df):

    sales_df_x, sales_df_y = encode_sales_data(sales_df)
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
def fit_sales_scaler(x_data):
    scaler = StandardScaler()
    scaler.fit(x_data[NUMERIC_SALES_COLUMNS])
    return scaler 

# scale passed x data using an already fitted scaler
def scale_sales_data(x_data, scaler):
    x_data[NUMERIC_SALES_COLUMNS] = scaler.transform(x_data[NUMERIC_SALES_COLUMNS])
    return x_data