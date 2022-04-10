#!/usr/bin/env python3

# Logical implementaion
# 1) tmx_node_producer (single process)
#    - Parse the TMX file
#    - extract the tuid, src and target tags from the node and store it as dict
#    - use json.dumps to conver the dict to string
#    - put the message into the queue_data
# 2) tmx_message_publisher (multi process)
#    - read the message from the queue_data
#    - call the kafka_publisher and push the message into kafka topic

from pathlib import Path
from multiprocessing import JoinableQueue, Process
from typing import Dict
import queue
import time
import xml.etree.ElementTree as ET
import json

import logging
from logger_module.logger_module import log
from message_publisher.kafka_publisher import KafkaPublisher
from config import Field, Tag, ErrorMessage, Parameters

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('data_extraction.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', force=True)
class ParseTMXFile:
    """
    A class to parse the tmx file and publish the message into kafka topic

    ...

    Attributes
    ----------
    file_path : str
        file path of tmx file

    Methods
    -------
    tmx_node_producer(queue_data):
        Parse the tmx file and extracts the required message
    tmx_message_publisher(queue_data):
        takes the message from the queue_data and publishes the message to kafka topic
    tmx_parse_manager():
        Creates and manages the process 
    """

    def __init__(self, file_path:str, publisher: KafkaPublisher, queue_size: int=20):
        """
        """
        self.file_path = Path(file_path)        
        self.publisher = publisher
        # assert file check
        logger.info("check if the file exists")
        assert self.file_path.is_file(), ErrorMessage.FILE_NOT_FOUND
    
    @log
    def tmx_node_producer(self, queue_data: JoinableQueue):
        """
        Parse the tmx file and put the nodes into the queue_data
        
        Parameters
        ----------
        queue_data: Joinable
            queue_data to share the data between the process
        """
        try:
            for event, node in ET.iterparse(self.file_path, events=(Field.START, Field.END)):
                message = {}
                if node.tag == Tag.TU and event == Field.END:
                    tuid = node.attrib[Tag.TUID]
                    translation_text = []
                    for e1 in node:
                        if e1.tag in [Tag.TUV]:                
                            for e2 in e1:
                                if e2.tag in [Tag.SEG]:
                                    translation_text.append(e2.text)
                    
                    message=dict(zip([Field.SRC, Field.TARGET], translation_text))
                    message[Field.TUID]=tuid

                    # Put the filtered messages into the nodes queue without waiting
                    queue_data.put(json.dumps(message))
                    logger.debug(f'Queue size after adding: {queue_data.qsize()}')
                    
                    node.clear() # to be cleared
            queue_data.join()  
            logger.debug(f'Done adding')          
        
        except Exception as error:
            raise Exception(error)

            
    @log
    def publish_message_worker(self, queue_data: JoinableQueue,  topic: str=Parameters.TOPIC):
        """
        takes the node from the queue_data and publishes the message to kafka topic
        
        Parameters
        ----------
        queue_data : Joinable
            queue_data to share the data between the process
        
        topic: str
            topic name to be published on kafka
        """

        # create a kafka producer for each publisher node
        try:       
            kafka_pub = KafkaPublisher()
            while True:
                # get the messages from the message queue
                
                if queue_data.qsize():
                    message = queue_data.get()
                    logger.debug(f'Publishing to the topic: {Parameters.TOPIC} ; message:  {message}')
                    kafka_pub.publish_message(topic, message)
                    
                    # Notify the queue that the work item has been processed
                    queue_data.task_done()
                else:
                    logger.debug(f'queue_data size empty: {queue_data.qsize()}')
                    continue
        except Exception as error:
            raise Exception(error)    
    
    
    @log
    def tmx_parse_manager(self):
        """
        Creates and manages the process 
        
        Parameters
        ----------
        """
        try:        
            queue_data = JoinableQueue()
            # Create producers to extract the nodes
            tmx_node_producers = [Process(target=self.tmx_node_producer, args=(queue_data,)) for _ in range(1)]

            # Create workers to publish the processed nodes
            publish_message_workers = [Process(target=self.publish_message_worker, args=(queue_data,  Parameters.TOPIC, ), daemon=True) for _ in range(Parameters.MAX_WORKERS)]
            
            for worker in tmx_node_producers+publish_message_workers:
                worker.start()

            for producer in tmx_node_producers:
                producer.join()

        except Exception as error:
            raise Exception(error)

if __name__ == '__main__':
    file_path  = '/home/workdir/tmx-file.tmx'
    publisher = KafkaPublisher()
    parser_obj = ParseTMXFile(file_path, publisher)
    parser_obj.tmx_parse_manager()