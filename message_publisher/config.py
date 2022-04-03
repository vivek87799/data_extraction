class KafkaConfig:

    KAFKA_BOOTSTRAP_SERVERS = ['broker-1:9092','broker-2:9092','broker-3:9092']
    KAFKA_BOOTSTRAP_PORT = 9092
    KAKFA_VERSION = (2,7,0)
    TIMEOUT = 60
    TOPIC = 'rawdata'