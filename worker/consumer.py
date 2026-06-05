import json
import time

import redis
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_kafka_consumer():
    retries = 10

    while retries > 0:
        try:
            consumer = KafkaConsumer(
                "incident.created",
                bootstrap_servers="kafka:9092",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="incident-workers"
            )

            logger.info("Kafka consumer connected")

            return consumer

        except NoBrokersAvailable:
            logger.info("Kafka not ready, retrying...")
            retries -= 1
            time.sleep(2)

    raise Exception("Could not connect to Kafka")


redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

consumer = get_kafka_consumer()

logger.info("Worker started listening...")

for message in consumer:
    event = message.value

    logger.info(f"Received event: {event}")

    incident_id = event["incident_id"]
    logger.info("Processing incident...")
    time.sleep(5)
    redis_client.set(
        f"incident:{incident_id}",
        "processed"
    )

    logger.info(f"Updated Redis for incident {incident_id}")