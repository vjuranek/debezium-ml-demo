#!/usr/bin/env python3

import pandas as pd

SUSY_DATA = "./data/SUSY.csv.gz"
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
INSERT_STMT = "INSERT INTO susy({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(floor({}), {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});\n"
CHUNK_SIZE = 100

df = pd.read_csv(SUSY_DATA, compression="gzip", chunksize=CHUNK_SIZE, header=None, names=COLUMNS)
chunk = df.get_chunk()

with open("susy.sql", 'w') as f:
    for row in chunk.values:
        f.write(INSERT_STMT.format(*COLUMNS, *row))
