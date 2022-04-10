# Data Extraction: Producer
Module that parses the TMX file and puts the raw parsed data into the kafka topic

## Logical implementaion
1) tmx_node_producer (single process)
   - Parse the TMX file
   - extracts the source and target message form the tmx file
2) tmx_message_publisher (multi process)
   - read the message from the queue_data
   - call the kafka_publisher and push the message into kafka topic

## To Run
- Use the dockerfile provided to set up the container and installing the package
- Configs are provided in config.py and message_publisher/config.py
- A separate dockerfile is provided to build and run this container
- Attach the to the running conatiner and run the data extraction module using the below command

```
python data_extraction.py
```

## Requirements
- Requires that the kafka zookeeper is running on the same network