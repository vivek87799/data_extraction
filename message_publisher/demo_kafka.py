from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
"""
topic = 'Orders'
bootstrap_servers = ['broker-1:9092','broker-2:9092','broker-3:9092']
consumer = KafkaConsumer(
    topic, bootstrap_servers='broker-3:9092', auto_offset_reset='earliest')
for msg in consumer:
    print(msg)

"""
topic = 'Orders'
bootstrap_servers = ['broker-1:9092','broker-2:9092','broker-3:9092']
producer = KafkaProducer(bootstrap_servers=bootstrap_servers, api_version=(2,7,0))

# Generate 100 messages
for _ in range(100):
    message = {_: {_*_: f'message:{_}'}}
    msg = f'Kontext kafka msg: {_}'
    msg = json.dumps(message)
    future = producer.send(topic, msg.encode('utf-8'))
    print(f'Sending msg: {msg}')
    result = future.get(timeout=60)

metrics = producer.metrics()
print(metrics)