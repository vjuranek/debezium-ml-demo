#!/usr/bin/env python3

import pandas as pd

CSV_DATA = "./data/SUSY.csv.gz"
SQL_DATA_TRAIN = "./postgres/susy-train.sql"
SQL_DATA_TEST = "./postgres/susy-test.sql"
COLUMNS = [
    #  labels
    'class',
    #  low-level features
    'lepton_1_pT',
    'lepton_1_eta',
    'lepton_1_phi',
    'lepton_2_pT',
    'lepton_2_eta',
    'lepton_2_phi',
    'missing_energy_magnitude',
    'missing_energy_phi',
    #  high-level derived features
    'MET_rel',
    'axial_MET',
    'M_R',
    'M_TR_2',
    'R',
    'MT2',
    'S_R',
    'M_Delta_R',
    'dPhi_r_b',
    'cos_theta_r1'
]
CREATE_STMT = "CREATE TABLE {}(id SERIAL NOT NULL PRIMARY KEY, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float, {} float);"
INSERT_STMT = "INSERT INTO {}({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});\n"
CHUNK_SIZE = 5000

df = pd.read_csv(CSV_DATA, compression="gzip", chunksize=CHUNK_SIZE, header=None, names=COLUMNS)

# train data set
chunk = df.get_chunk()
with open(SQL_DATA_TRAIN, 'w') as f:
    f.write(CREATE_STMT.format("susy_train", *COLUMNS))
    for row in chunk.values:
        f.write(INSERT_STMT.format("susy_train", *COLUMNS, *row))

# test data set
chunk = df.get_chunk()
with open(SQL_DATA_TEST, 'w') as f:
    # f.write(CREATE_STMT.format("susy_test", *COLUMNS))
    for row in chunk.values:
        f.write(INSERT_STMT.format("susy_test", *COLUMNS, *row))
