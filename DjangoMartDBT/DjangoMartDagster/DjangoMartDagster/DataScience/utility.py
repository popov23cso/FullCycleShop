from sklearn.preprocessing import StandardScaler
import numpy as np

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