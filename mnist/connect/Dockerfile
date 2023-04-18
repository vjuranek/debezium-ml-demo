FROM quay.io/debezium/connect:2.2
ENV KAFKA_CONNECT_MNIST_DIR=$KAFKA_CONNECT_PLUGINS_DIR/kafka-connect-mnist

RUN mkdir $KAFKA_CONNECT_MNIST_DIR
COPY key-value-smt/target/mnist-to-csv-1.0-SNAPSHOT.jar $KAFKA_CONNECT_MNIST_DIR