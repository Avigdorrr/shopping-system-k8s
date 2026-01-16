import asyncio
import json
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


async def init_kafka(app: FastAPI):
    logger.info(f"Connecting to Kafka Producer at {settings.KAFKA_BOOTSTRAP_SERVERS}...")

    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await producer.start()

            app.state.kafka_producer = producer
            logger.info("Kafka Producer connected successfully")

            return

        except Exception as e:
            logger.warning(f"Connection attempt {attempt}/{max_retries} failed: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

    logger.error("Could not connect to Kafka after retries")
    raise Exception("Kafka connection failed")


async def close_kafka(app: FastAPI):
    if hasattr(app.state, "kafka_producer"):
        logger.info("Stopping Kafka producer...")
        await app.state.kafka_producer.stop()
