import configparser
import logging
import time
import asyncio
import asyncio_mqtt
from pykafka import KafkaClient


# Setting up logging
log_file = "bridge.log"
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.DEBUG)

# Reading configuration
config_file = "config.ini"
config = configparser.ConfigParser()
config.read(config_file)
mqtt_broker = config["mqtt_broker"]["address"]
mqtt_broker_max_wait = config["mqtt_broker"]["maximum_wait_ms"]
kafka_broker = config["kafka_broker"]["address"]
kafka_brokers_max_wait = config["kafka_broker"]["maximum_wait_ms"]
message_topics = config["messages"]["topics"]
print(message_topics)

kafka_client = KafkaClient(hosts=kafka_broker)
kafka_topic = kafka_client.topics[message_topics]
kafka_producer = kafka_topic.get_sync_producer()


def mqtt_on_connect(client, userdata, flags, rc):
    # The callback for when the client receives a CONNACK response from the server.
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


def mqtt_on_message(client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server.
    print(msg.topic + " " + str(msg.payload))


async def read_message():
    print("Read")
    await asyncio.sleep(2)


async def transmit_message():
    print("Transmit")
    await asyncio.sleep(2)


async def main():
    mqtt_host_ip = str.split(mqtt_broker, ":")[0]
    mqtt_host_port = int(str.split(mqtt_broker, ":")[1])

    async with asyncio_mqtt.Client(hostname=mqtt_host_ip, port=mqtt_host_port) as client:
        async with client.messages() as messages:
            await client.subscribe(message_topics)
            async for message in messages:
                print(message.payload)


if __name__ == '__main__':
    
    asyncio.run(main())

# event_loop = asyncio.get_event_loop()
# event_loop.create_task(read_message())
# event_loop.create_task(transmit_message())
# event_loop.run_forever()
