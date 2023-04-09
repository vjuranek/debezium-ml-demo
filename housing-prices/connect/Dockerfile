FROM quay.io/debezium/connect:2.2
ENV KAFKA_CONNECT_SUSY_DIR=$KAFKA_CONNECT_PLUGINS_DIR/kafka-connect-val-to-csv

RUN mkdir $KAFKA_CONNECT_SUSY_DIR
COPY value-to-csv-smt/target/value-to-csv-1.0-SNAPSHOT.jar $KAFKA_CONNECT_SUSY_DIR