package io.debezium.transforms;

import java.util.Map;

import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.connect.connector.ConnectRecord;
import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.transforms.Transformation;

public class MnistToCsv<R extends ConnectRecord<R>> implements Transformation<R> {

    private static final int IMG_SIZE = 784;

    @Override
    public R apply(R r) {
        final Struct value = (Struct) r.value();
        String key = value.getInt16("label").toString();

        StringBuilder builder = new StringBuilder();
        for (byte pixel : value.getBytes("pixels")) {
            builder.append(pixel & 0xFF).append(",");
        }
        if (builder.length() > 0) {
            builder.deleteCharAt(builder.length() - 1);
        }
        String newValue = builder.toString();

        return r.newRecord(r.topic(), r.kafkaPartition(), Schema.STRING_SCHEMA, key, Schema.STRING_SCHEMA, newValue, r.timestamp());
    }

    @Override
    public ConfigDef config() {
        return new ConfigDef();
    }

    @Override
    public void close() {
    }

    @Override
    public void configure(Map<String, ?> map) {
    }
}

