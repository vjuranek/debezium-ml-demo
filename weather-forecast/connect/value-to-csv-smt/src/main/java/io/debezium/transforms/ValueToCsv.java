package io.debezium.transforms;

import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.connect.connector.ConnectRecord;
import org.apache.kafka.connect.data.Field;
import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.errors.DataException;
import org.apache.kafka.connect.transforms.Transformation;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;

public class ValueToCsv<R extends ConnectRecord<R>> implements Transformation<R> {
    private static final Logger LOGGER = LoggerFactory.getLogger(ValueToCsv.class);

    @Override
    public R apply(R r) {
        final Struct value = (Struct) r.value();

        try {
            value.get("id");
        } catch(DataException e) {
            LOGGER.warn("Unexpected message {}, skipping SMT", value);
            return r;
        }

        List<Field> fields = value.schema().fields();
        StringBuilder builder = new StringBuilder();
        for (Field field : fields) {
            if (field.schema().type() == Schema.Type.FLOAT32) {
                builder.append(value.getFloat32(field.name()).toString()).append(",");
            }
            if (field.schema().type() == Schema.Type.FLOAT64) {
                builder.append(value.getFloat64(field.name()).toString()).append(",");
            }
        }
        if (builder.length() > 0) {
            builder.deleteCharAt(builder.length() - 1);
        }
        String key = value.getInt32("id").toString();
        String newValue = builder.toString();
        return r.newRecord(r.topic(), r.kafkaPartition(), Schema.INT32_SCHEMA, key, Schema.STRING_SCHEMA, newValue, r.timestamp());
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
