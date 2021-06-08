# Adding Connectors to Kafka

## Install Binary Connectors

Before ArgoCD Synchronization, this is a necessary step. Do this only once, prior to synchronization.

```bash
# start a build to upload the connector via s2i
oc start-build my-connect-cluster-connect --from-dir=connectors --follow
```

## Additional Helpful Commands

```bash
# check available connectors (periodically check this until the connector has been fully added)
oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- curl -s http://my-connect-cluster-connect-api:8083/connector-plugins | jq

# check connector status
oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- curl -s http://my-connect-cluster-connect-api:8083/connectors/debezium-mysql-kafka-connector/status | jq 

# list topics
oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- bin/kafka-topics.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --list

# check recieved messages
oc exec -i `oc get pods --field-selector status.phase=Running -l strimzi.io/name=my-connect-cluster-connect -o=jsonpath='{.items[0].metadata.name}'` -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic dbserver.testdb.test_table --from-beginning | jq
```

## Reference

https://camel.apache.org/camel-kafka-connector/latest/try-it-out-on-openshift-with-strimzi.html