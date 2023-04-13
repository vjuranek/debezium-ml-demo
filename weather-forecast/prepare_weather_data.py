#!/usr/bin/env python3

import os

import numpy as np
import pandas as pd
import tensorflow as tf

WEATHER_DATA_URL = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip"
WEATHER_DATA_FILE_NAME = "jena_climate_2009_2016.csv.zip"

SQL_DATA_TRAIN = "./postgres/weather-train.sql"
TABLE_NAME_TRAIN = "weather_train"
SQL_DATA_TEST = "./mysql/weather-test.sql"
TABLE_NAME_TEST = "weather_test"
COLUMNS = [
    "p",
    "T",
    "Tpot",
    "Tdew",
    "rh",
    "VPmax",
    "VPact",
    "VPdef",
    "sh",
    "H2OC",
    "rho",
    "Wx",
    "Wy",
    "max_Wx",
    "max_Wy",
    "Day_sin",
    "Day_cos",
    "Year_sin",
    "Year_cos",
]

# SERIAL in Postgres results into int32, while in MySQL into int64 which complicates SMT,
# therefore each DB as its own create table statement.
CREATE_STMT_POSTGRES = "CREATE TABLE {}(id SERIAL NOT NULL PRIMARY KEY, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float);"
CREATE_STMT_MYSQL = "CREATE TABLE {}(id int AUTO_INCREMENT NOT NULL PRIMARY KEY, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float);"
INSERT_STMT = "INSERT INTO {}({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});\n"

def get_data():
    zip_path = tf.keras.utils.get_file(
        origin=WEATHER_DATA_URL,
        fname=WEATHER_DATA_FILE_NAME,
        extract=True)
    csv_path, _ = os.path.splitext(zip_path)
    df = pd.read_csv(csv_path)
    # Slice [start:stop:step], starting from index 5 take every 6th record.
    df = df[5::6]
    return df

def fix_wind_data(df):
    wv = df['wv (m/s)']
    bad_wv = wv == -9999.0
    wv[bad_wv] = 0.0

    max_wv = df['max. wv (m/s)']
    bad_max_wv = max_wv == -9999.0
    max_wv[bad_max_wv] = 0.0

    return df


def transform_wind_vector(df):
    wv = df.pop('wv (m/s)')
    max_wv = df.pop('max. wv (m/s)')
    
    # Convert to radians.
    wd_rad = df.pop('wd (deg)')*np.pi / 180
    
    # Calculate the wind x and y components.
    df['Wx'] = wv*np.cos(wd_rad)
    df['Wy'] = wv*np.sin(wd_rad)

    # Calculate the max wind x and y components.
    df['max Wx'] = max_wv*np.cos(wd_rad)
    df['max Wy'] = max_wv*np.sin(wd_rad)

    return df

def transform_timestamp_vector(df):
    day = 24*60*60
    year = (365.2425)*day

    date_time = pd.to_datetime(df.pop('Date Time'), format='%d.%m.%Y %H:%M:%S')
    timestamp_s = date_time.map(pd.Timestamp.timestamp)

    df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

    return df
    
def prepare_sql(create_stmt, data, file_name, table_name):
    with open(file_name, 'w') as f:
        f.write(create_stmt.format(table_name, *COLUMNS))
        for row in data.values:
            f.write(INSERT_STMT.format(table_name, *COLUMNS, *row))

df = transform_timestamp_vector(transform_wind_vector(fix_wind_data(get_data())))
# n = len(df)
n = 1000
train_df = df[0:int(n*0.7)]
val_df = df[int(n*0.7):int(n*0.9)]
# test_df = df[int(n*0.9):]
test_df = df[int(n*0.9):n]

prepare_sql(CREATE_STMT_POSTGRES, train_df, SQL_DATA_TRAIN, TABLE_NAME_TRAIN)
prepare_sql(CREATE_STMT_MYSQL, test_df, SQL_DATA_TEST, TABLE_NAME_TEST)
