Ver. 0.1
by Eric Eikrem

Introduction

This is a simple bridge between an mqtt and a Kafka broker. It may be useful for test
deployments, air-gapped setups, and similar. In production, and with access to the cloud,
you may be better off using Kafka Connect, or similar.

Configuration

The configuration is done by editing config.ini. See comments in the file for details.



References

I have built on the ideas of others, in particular the following:

1."MQTT and Kafka - How to combine two complementary technologies"
Walkthrough of a lot of different ways to connect mqtt and Kafka.
https://medium.com/python-point/mqtt-and-kafka-8e470eff606b

2.Apache Kafka + MQTT = End-to-End IoT Integration (Code, Slides, Video)
https://www.kai-waehner.de/blog/2018/09/10/apache-kafka-mqtt-end-to-end-iot-integration-demo-scripts-github/

3.asyncio-mqtt 0.16.1
https://pypi.org/project/asyncio-mqtt/

4."Python MQTT Bridge Project"
A bridge between mqtt brokers. Can be used in combination with
the mqtt/Kafka-bridge for topic aggregation.
http://www.steves-internet-guide.com/python-mqtt-bridge-project/