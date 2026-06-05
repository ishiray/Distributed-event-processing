import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time


producer = None


def get_producer():
    global producer

    if producer is None:
        retries = 10

        while retries > 0:
            try:
                producer = KafkaProducer(
                    bootstrap_servers="kafka:9092",
                    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                )

                print("Kafka producer connected successfully")

                return producer

            except NoBrokersAvailable:
                print("Kafka not ready yet, retrying...")
                retries -= 1
                time.sleep(2)

        raise Exception("Could not connect to Kafka")

    return producer


def publish_incident_created(event_data: dict):
    producer = get_producer()

    producer.send("incident.created", event_data)
    producer.flush()

    print(f"Published event: {event_data}")