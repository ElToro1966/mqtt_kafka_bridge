# Bridge between mqtt and kafka
# Asynchronous version (Note: the Kafka producer is asynchronous by default)

import configparser
import logging
import asyncio
import asyncio_mqtt
from kafka import KafkaProducer
import os


def path_to_cwd(filename):
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, filename)


log_file = path_to_cwd("bridge.log")
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.DEBUG)

config_file = path_to_cwd("config.ini")
config = configparser.ConfigParser()
config.read(config_file)

mqtt_broker = config["mqtt_broker"]["address"]
mqtt_broker_max_wait = config["mqtt_broker"]["maximum_wait_ms"]
mqtt_message_topics = config["messages"]["topics"]
mqtt_message_topics = str.split(mqtt_message_topics, ",")

kafka_broker = config["kafka_broker"]["address"]
kafka_brokers_max_wait = config["kafka_broker"]["maximum_wait_ms"]


def mqtt_to_kafka_topic_conversion(mqtt_message_topic):
    # Convert an mqtt message topic to a kafka message topic

    # Remove leading and trailing whitespace
    mqtt_message_topic = str(mqtt_message_topic).strip()
    # Replace prohibited characters in mqtt message topic with characters allowed in kafka
    kafka_message_topic = mqtt_message_topic.replace("/", ".")
    kafka_message_topic = kafka_message_topic.replace(" ", "_")
    # Due to limitations in kafka metric names, topics with a period ('.') or underscore ('_') could collide.
    # To avoid issues it is best to use either, but not both.
    kafka_message_topic = kafka_message_topic.replace("_", ".")
    return kafka_message_topic


async def main():
    mqtt_host_ip = str.split(mqtt_broker, ":")[0]
    mqtt_host_port = int(str.split(mqtt_broker, ":")[1])
    kafka_producer = KafkaProducer(bootstrap_servers=[kafka_broker])

    async with asyncio_mqtt.Client(hostname=mqtt_host_ip, port=mqtt_host_port) as client:
        async with client.messages() as messages:
            for mqtt_message_topic in mqtt_message_topics:
                print("MQTT message topic: " + mqtt_message_topic)
                await client.subscribe(mqtt_message_topic)
            async for message in messages:
                print("Kafka message payload: " + message.payload.decode())
                message.topic = mqtt_to_kafka_topic_conversion(message.topic)
                print("Kafka message topic: " + message.topic)
                kafka_producer.send(message.topic, message.payload)

if __name__ == '__main__':
    
    asyncio.run(main())
