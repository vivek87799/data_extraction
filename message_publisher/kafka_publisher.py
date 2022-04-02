#!/usr/bin/env python3

# Logical implementaion
# 1) create_publisher
#    - Create a kafka publisher or producer
# 2) publish_message
#    - Publishes the message to the kafka topic


from kafka import KafkaProducer

from abc import ABC, abstractmethod

from typing import List, Tuple

# from message_publisher import MessagePublisher
from message_publisher.config import KafkaConfig



class KafkaPublisher:
    """
    A class to establish kafka producer

    ...

    Attributes
    ----------
    bootstrap_servers : list
        list of bootstrap_servers to connect to
    port: int
        port number to connect on kafka
    kafka_version: tuple
        kafka version in the format of a tuple # eg (2,7,0)

    Methods
    -------
    create_publisher():
        createes a kafka producer ## or say kafka publisher
    publish_message(message=""):
        Takes the 
    """

    def __init__(self, bootstrap_servers: List[str]=KafkaConfig.KAFKA_BOOTSTRAP_SERVERS, port: int=KafkaConfig.KAFKA_BOOTSTRAP_PORT, kafka_version: Tuple[int]=KafkaConfig.KAKFA_VERSION):
        
        self.bootstrap_servers = bootstrap_servers
        self.port = port
        self.kafka_version = kafka_version
        self.create_publisher()

    def create_publisher(self):
        """
        Creates a kafka producer ## or say kafka publisher
        
        Parameters
        ----------
        """
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, api_version=self.kafka_version)        
        
    def publish_message(self, topic: str=KafkaConfig.TOPIC, message="", timeout: int=KafkaConfig.TIMEOUT):
        """
        Publishes the message to the kafka topic
        
        Parameters
        ----------
        topic: str
            topic name to be published on kafka

        message: str
            str message to be published
        """

        try:
            print(f'message publisher....{message}')
            future = self.producer.send(topic, message.encode('utf-8'))
            
            print(f'message published')
            result = future.get(timeout=1)
            self.producer.flush()
        except Exception as error:
            raise Exception(error)

        

if __name__ == '__main__':
    kafka_pub = KafkaPublisher()
    kafka_pub.publish_message('Orders', '{"src": "Vorname", "target": "Pr\u00e9nom", "tuid": "810297288"}')
