package io.debezium.transforms;

import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.connect.connector.ConnectRecord;
import org.apache.kafka.connect.data.Field;
import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.transforms.Transformation;

import java.util.List;
import java.util.Map;

public class ValueToCsv<R extends ConnectRecord<R>> implements Transformation<R> {
    @Override
    public R apply(R r) {
        final Struct value = (Struct) r.value();
        List<Field> fields = value.schema().fields();
        StringBuilder builer = new StringBuilder();
        for (Field field : fields) {
            if (field.schema().type() == Schema.Type.FLOAT64) {
                builer.append(value.getFloat64(field.name()).toString()).append(",");
            }
        }
        builer.deleteCharAt(builer.length() - 1);
        String key = value.getInt32("id").toString();
        String newValue = builer.toString();
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
