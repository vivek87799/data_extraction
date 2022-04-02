from abc import ABC, abstractmethod

class IMessagePublisher(ABC):
    @abstractmethod
    def create_publisher(self, bootstrap_servers, port):
        """
        Takes the bootstrap_servers and port number as input and createes a publisher
        """
        pass

    @abstractmethod
    def publish_message(self, topic, message):
        """
        This function takes the topic and message as input and publishes the message on to topic
        """
        pass