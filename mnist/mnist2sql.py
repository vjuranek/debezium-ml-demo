#!/usr/bin/env python3

import gzip
import struct

MNIST_LABEL_MAGIC = 2049
MNIST_IMAGE_MAGIC = 2051

CREATE_STMT = ("CREATE TABLE {}(id SERIAL NOT NULL PRIMARY KEY, "
               "label SMALLINT, pixels BYTEA);\n")
INSERT_STMT = "INSERT INTO {}(label, pixels) VALUES({}, '\\x{}');\n"


def prepare_sql(label_path, img_path, sql_path, table_name):
    """
    Combines label file with images from the other file and create new file
    with SQL commands for creating and populating specified DB table with
    these values. Images bytes are encoded as HEX strings.
    """
    with open(sql_path, mode='w', encoding="utf-8") as sql_file:
        sql_file.write(CREATE_STMT.format(table_name))

        with gzip.open(label_path, "rb") as label_file:
            with gzip.open(img_path, "rb") as image_file:
                magic_label, num_label = struct.unpack(
                    ">II", label_file.read(8))
                magic_img, num_img, rows, columns = struct.unpack(
                    ">IIII", image_file.read(16))

                if MNIST_LABEL_MAGIC != magic_label:
                    raise ValueError("Unexpected label magic: {magic_label}")
                if MNIST_IMAGE_MAGIC != magic_img:
                    raise ValueError("Unexpected image magic: {magic_img}")
                if num_label != num_img:
                    raise ValueError(
                        "Size of labels {num_label} doesn't match with size of"
                        " image sample {num_img}")

                img_size = rows * columns
                for _ in range(0, num_label):
                    label = struct.unpack(">b", label_file.read(1))
                    pixels = image_file.read(img_size)
                    sql_file.write(
                        INSERT_STMT.format(table_name, label[0], pixels.hex()))

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
