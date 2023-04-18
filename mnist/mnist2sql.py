#!/usr/bin/env python3

import gzip
import struct

MNIST_LABEL_MAGIC = 2049
MNIST_IMAGE_MAGIC = 2051

CREATE_STMT = "CREATE TABLE {}(id SERIAL NOT NULL PRIMARY KEY,  label SMALLINT, pixels BYTEA);\n"
INSERT_STMT = "INSERT INTO {}(label, pixels) VALUES({}, '\\x{}');\n"

def prepare_sql(label_file, img_file, sql_file, table_name):
    with open(sql_file, 'w') as f:
        f.write(CREATE_STMT.format(table_name))

        with gzip.open(label_file, "rb") as fl:
            with gzip.open(img_file, "rb") as fi:
                magic_label, num_label = struct.unpack(">II", fl.read(8))
                magic_img, num_img, rows, columns = struct.unpack(">IIII", fi.read(16))
 
                if MNIST_LABEL_MAGIC != magic_label:
                    raise ValueError("Unexpected label magic: %r" % magic_label)
                if MNIST_IMAGE_MAGIC != magic_img:
                    raise ValueError("Unexpected image magic: %r" % magic_img)
                if num_label != num_img:
                    raise ValueError("Size of labels (%r) doesn't match with size of image sample (%r)" % (num_label, num_img))

                img_size = rows * columns
                for i in range(0, num_label):
                    label = struct.unpack(">b", fl.read(1))
                    pixels = fi.read(img_size)
                    f.write(INSERT_STMT.format(table_name, label[0], pixels.hex()))

prepare_sql(
    "../data/train-labels-idx1-ubyte.gz",
    "../data/train-images-idx3-ubyte.gz",
    "postgres/mnist-train.sql",
    "mnist_train"
)

prepare_sql(
    "../data/t10k-labels-idx1-ubyte.gz",
    "../data/t10k-images-idx3-ubyte.gz",
    "postgres/mnist-test.sql",
    "mnist_test"
)

