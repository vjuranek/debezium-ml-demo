package io.debezium.transforms;

import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.connect.connector.ConnectRecord;
import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.transforms.Transformation;

import java.util.Map;

public class SusyFlatten<R extends ConnectRecord<R>> implements Transformation<R> {
    private static final String[] COLUMNS = {
            // low-level features
            "lepton_1_pT",
            "lepton_1_eta",
            "lepton_1_phi",
            "lepton_2_pT",
            "lepton_2_eta",
            "lepton_2_phi",
            "missing_energy_magnitude",
            "missing_energy_phi",
            // high-level derived features
            "MET_rel",
            "axial_MET",
            "M_R",
            "M_TR_2",
            "R",
            "MT2",
            "S_R",
            "M_Delta_R",
            "dPhi_r_b",
            "cos_theta_r1"
    };

    @Override
    public R apply(R r) {
        final Struct value = (Struct) r.value();
        StringBuilder builer = new StringBuilder();
        for (String column : COLUMNS) {
            builer.append(value.getFloat64(column.toLowerCase()).toString()).append(",");
        }
        builer.deleteCharAt(builer.length() - 1);
        String key = value.getFloat64("class").toString();
        String newValue = builer.toString();
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
