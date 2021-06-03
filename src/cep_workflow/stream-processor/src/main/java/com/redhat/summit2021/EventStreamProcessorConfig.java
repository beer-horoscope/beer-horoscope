package com.redhat.summit2021;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.common.config.SslConfigs;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.Properties;
import java.util.StringTokenizer;

public class EventStreamProcessorConfig {
    private static final Logger log = LogManager.getLogger(EventStreamProcessorConfig.class);

    private static final int DEFAULT_COMMIT_INTERVAL_MS = 5000;
    private final String bootstrapServers;
    private final String applicationId;
    private final String sourceTopic;
    private final int commitIntervalMs;
    private final String trustStorePassword;
    private final String trustStorePath;
    private final String keyStorePassword;
    private final String keyStorePath;
    private final String additionalConfig;
    private final int trainingDataTriggerThreshold;

    public EventStreamProcessorConfig(String bootstrapServers, String applicationId, String sourceTopic, int commitIntervalMs, String trustStorePassword, String trustStorePath, String keyStorePassword, String keyStorePath, String additionalConfig, int trainingDataTriggerThreshold) {
        this.bootstrapServers = bootstrapServers;
        this.applicationId = applicationId;
        this.sourceTopic = sourceTopic;
        this.commitIntervalMs = commitIntervalMs;
        this.trustStorePassword = trustStorePassword;
        this.trustStorePath = trustStorePath;
        this.keyStorePassword = keyStorePassword;
        this.keyStorePath = keyStorePath;
        this.additionalConfig = additionalConfig;
        this.trainingDataTriggerThreshold = trainingDataTriggerThreshold;
    }

    public static EventStreamProcessorConfig fromEnv() {
        String bootstrapServers = System.getenv("BOOTSTRAP_SERVERS");
        String sourceTopic = System.getenv("SOURCE_TOPIC");
        String applicationId = System.getenv("APPLICATION_ID");
        int commitIntervalMs = System.getenv("COMMIT_INTERVAL_MS") == null ? DEFAULT_COMMIT_INTERVAL_MS : Integer.parseInt(System.getenv("COMMIT_INTERVAL_MS"));
        String trustStorePassword = System.getenv("TRUSTSTORE_PASSWORD") == null ? null : System.getenv("TRUSTSTORE_PASSWORD");
        String trustStorePath = System.getenv("TRUSTSTORE_PATH") == null ? null : System.getenv("TRUSTSTORE_PATH");
        String keyStorePassword = System.getenv("KEYSTORE_PASSWORD") == null ? null : System.getenv("KEYSTORE_PASSWORD");
        String keyStorePath = System.getenv("KEYSTORE_PATH") == null ? null : System.getenv("KEYSTORE_PATH");
        String additionalConfig = System.getenv().getOrDefault("ADDITIONAL_CONFIG", "");
        int trainingDataTriggerThreshold = System.getenv("TRAINING_DATA_TRIGGER_THRESHOLD") == null ? 10000 : Integer.parseInt(System.getenv("TRAINING_DATA_TRIGGER_THRESHOLD"));

        return new EventStreamProcessorConfig(bootstrapServers, applicationId, sourceTopic, commitIntervalMs, trustStorePassword, trustStorePath, keyStorePassword, keyStorePath, additionalConfig, trainingDataTriggerThreshold);
    }

    public static Properties createProperties(EventStreamProcessorConfig config) {
        Properties props = new Properties();

        props.put(StreamsConfig.APPLICATION_ID_CONFIG, config.getApplicationId());
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, config.getBootstrapServers());
        props.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, config.getCommitInterval());
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put("consumer.override.auto.offset.reset", "latest");


        if (!config.getAdditionalConfig().isEmpty()) {
            StringTokenizer tok = new StringTokenizer(config.getAdditionalConfig(), ", \t\n\r");
            while (tok.hasMoreTokens()) {
                String record = tok.nextToken();
                int endIndex = record.indexOf('=');
                if (endIndex == -1) {
                    throw new RuntimeException("Failed to parse Map from String");
                }
                String key = record.substring(0, endIndex);
                String value = record.substring(endIndex + 1);
                props.put(key.trim(), value.trim());
            }
        }

        if (config.getTrustStorePassword() != null && config.getTrustStorePath() != null)   {
            log.info("Configuring truststore");
            props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SSL");
            props.put(SslConfigs.SSL_TRUSTSTORE_TYPE_CONFIG, "PKCS12");
            props.put(SslConfigs.SSL_TRUSTSTORE_PASSWORD_CONFIG, config.getTrustStorePassword());
            props.put(SslConfigs.SSL_TRUSTSTORE_LOCATION_CONFIG, config.getTrustStorePath());
        }

        if (config.getKeyStorePassword() != null && config.getKeyStorePath() != null)   {
            log.info("Configuring keystore");
            props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SSL");
            props.put(SslConfigs.SSL_KEYSTORE_TYPE_CONFIG, "PKCS12");
            props.put(SslConfigs.SSL_KEYSTORE_PASSWORD_CONFIG, config.getKeyStorePassword());
            props.put(SslConfigs.SSL_KEYSTORE_LOCATION_CONFIG, config.getKeyStorePath());
        }

        return props;
    }

    public String getBootstrapServers() {
        return bootstrapServers;
    }

    public String getApplicationId() {
        return applicationId;
    }

    public String getSourceTopic() {
        return sourceTopic;
    }

    public int getCommitInterval() {
        return commitIntervalMs;
    }

    public String getTrustStorePassword() {
        return trustStorePassword;
    }

    public String getTrustStorePath() {
        return trustStorePath;
    }

    public String getKeyStorePassword() {
        return keyStorePassword;
    }

    public String getKeyStorePath() {
        return keyStorePath;
    }

    public String getAdditionalConfig() {
        return additionalConfig;
    }

    public int getTrainingDataTriggerThreshold() {
        return trainingDataTriggerThreshold;
    }

    @Override
    public String toString() {
        return "KafkaStreamsConfig{" +
                "bootstrapServers='" + bootstrapServers + '\'' +
                ", applicationId='" + applicationId + '\'' +
                ", sourceTopic='" + sourceTopic + '\'' +
                ", commitIntervalMs=" + commitIntervalMs +
                ", trustStorePassword='" + trustStorePassword + '\'' +
                ", trustStorePath='" + trustStorePath + '\'' +
                ", keyStorePassword='" + keyStorePassword + '\'' +
                ", keyStorePath='" + keyStorePath + '\'' +
                ", additionalConfig='" + additionalConfig + '\'' +
                '}';
    }
}
