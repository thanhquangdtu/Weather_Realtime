from kafka import KafkaProducer
import json

def create_producer():
    producer = KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    return producer


def send_message(producer, topic, data):
    producer.send(topic, value=data)
    producer.flush()
