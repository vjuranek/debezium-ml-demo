#!/usr/bin/env python3

import pandas as pd

COLUMNS = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "iris_class",
]

CREATE_STMT = "CREATE TABLE {}(id SERIAL NOT NULL PRIMARY KEY, {} float, {} float, {} float, {} float, {} varchar(32));"
INSERT_STMT = "INSERT INTO {}({}, {}, {}, {}, {}) VALUES({}, {}, {}, {}, '{}');\n"

df = pd.read_csv("./iris.data")

def prepare_sql(create_stmt, data, file_name, table_name):
    with open(file_name, 'w') as f:
        f.write(create_stmt.format(table_name, *COLUMNS))
        for row in data.values:
            f.write(INSERT_STMT.format(table_name, *COLUMNS, *row))

prepare_sql(CREATE_STMT, df, "iris.sql", "iris")
