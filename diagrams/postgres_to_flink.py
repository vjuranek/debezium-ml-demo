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

    with Cluster("Kafka Connect"):
        debezium = Custom("Debezium", debezium_icon)
        kafka = [Kafka("Kafka train"), Kafka("Kafka test")]
        debezium >> kafka

    Postgresql("Postgres") >> debezium
    kafka >> Flink("Apache Flink") >> Kafka("Kafka predictions")
