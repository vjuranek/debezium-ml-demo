#!/usr/bin/env python3

from keras.datasets import boston_housing

SQL_DATA_TRAIN = "./postgres/boston-train.sql"
TABLE_NAME_TRAIN = "boston_train"
SQL_DATA_TEST = "./postgres/boston-test.sql"
TABLE_NAME_TEST = "boston_test"
COLUMNS = [
    "crim",
    "zn",
    "indus",
    "chas",
    "nox",
    "rm",
    "age",
    "dis",
    "rad",
    "tax",
    "ptratio",
    "lstat",
    "medv",
    "target"
]
CREATE_STMT = "CREATE TABLE {}(id SERIAL NOT NULL PRIMARY KEY, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float);"
INSERT_STMT = "INSERT INTO {}({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});\n"

def prepare_sql(data, file_name, table_name):
    with open(file_name, 'w') as f:
        f.write(CREATE_STMT.format(table_name, *COLUMNS))
        for row in data:
            f.write(INSERT_STMT.format(table_name, *COLUMNS, *row[0], row[1]))

(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()            
prepare_sql(zip(train_data, train_targets), SQL_DATA_TRAIN, TABLE_NAME_TRAIN)
prepare_sql(zip(test_data, test_targets), SQL_DATA_TEST, TABLE_NAME_TEST)
