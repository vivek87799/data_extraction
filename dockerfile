FROM alpine:3.14

RUN apk update && apk upgrade
RUN apk --no-cache add curl
RUN apk --no-cache add bash
RUN apk --no-cache add openjdk11

# Install python/pip
# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight 
# to terminal (e.g. your container log) without being first buffered and that you can see the 
# output of your application (e.g. django logs) in real time.
ENV PYTHONUNBUFFERED=1 
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY . /home/workdir/
COPY tmx-file.tmx /home/workdir/
RUN pip3 install -r /home/workdir/requirements.txt
# CMD ["/home/workdir/data_cleaning.py"]



ENV KAFKA_VERSION 2.7.0
ENV SCALA_VERSION 2.13 

RUN  mkdir /tmp/kafka && \
    curl "https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" \
    -o /tmp/kafka/kafka.tgz && \
    mkdir /kafka && cd /kafka && \
    tar -xvzf /tmp/kafka/kafka.tgz --strip 1

COPY start-kafka.sh  /usr/bin
RUN chmod +x  /usr/bin/start-kafka.sh
ENTRYPOINT [ "/bin/bash" ]

CMD ["start-kafka.sh"]
   