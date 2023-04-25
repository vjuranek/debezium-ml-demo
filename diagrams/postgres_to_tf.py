#!/usr/bin/env python3

# from urllib.request import urlretrieve

from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Kafka


# # Download Debezim icon
# debezium_url = "https://design.jboss.org/debezium/logo/final/color/color_debezium_256px.png"
debezium_icon = "img/debezium.png"
# urlretrieve(debezium_url, debezium_icon)

# # Download TensorFlow icon
# tensorflow_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Tensorflow_logo.svg/224px-Tensorflow_logo.svg.png"
tensorflow_icon = "img/tensorflow.png"
# urlretrieve(tensorflow_url, tensorflow_icon)

# # Download Jupyter icon
# jupyter_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/207px-Jupyter_logo.svg.png"
jupyter_icon = "img/jupyter.png"
# urlretrieve(jupyter_url, jupyter_icon)


with Diagram(show=False):

    with Cluster("Kafka Connect"):
        debezium = Custom("Debezium", debezium_icon)
        kafka = Kafka("Kafka")
        debezium >> kafka

    with Cluster("TensorFlow with Jupyter notebook"):
            tensorflow = Custom("TensorFlow", tensorflow_icon)
            jupyter = Custom("Jupyter notebook", jupyter_icon)
            tensorflow >> jupyter

    Postgresql("Postgres") >> debezium
    kafka >> tensorflow
