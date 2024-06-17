#!/usr/bin/env python3

# from urllib.request import urlretrieve

from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.onprem.analytics import Flink
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Kafka


# # Download Debezim icon
# debezium_url = "https://design.jboss.org/debezium/logo/final/color/color_debezium_256px.png"
debezium_icon = "img/debezium.png"
# urlretrieve(debezium_url, debezium_icon)

graph_attr = {
     "bgcolor": "transparent",
}

with Diagram(show=False, graph_attr=graph_attr):

    with Cluster("Apache Flink"):
        debezium = Custom("Debezium", debezium_icon)
        flink = [Flink("Flink train"), Flink("Flink test")]
        debezium >> flink

    Postgresql("Postgres") >> debezium
    flink >> Kafka("Kafka predictions")
