# Data Extraction: Producer
Module that parses the TMX file and puts the raw parsed data into the kafka topic
## Data Extraction
- A single process runs to extract the tmx file 
- multiple worker nodes run to filter and put the messages into the kafka topic

## To Run
- Use the docker file provided to set up the container and installing the package
- Configs are provided in config.py and message_publisher/config.py
```
python data_extraction.py
```

## Requirements
- Requires that the kafka zookeeper is running