from kafka import KafkaProducer

kafka_producer = KafkaProducer(bootstrap_servers='10.0.0.20:9092')

future = kafka_producer.send("Sensor.G01.hwc.message.sent", b'test')
result = future.get(timeout=60)