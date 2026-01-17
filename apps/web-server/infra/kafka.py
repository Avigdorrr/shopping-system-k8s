import asyncio
import json
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


async def init_kafka(app: FastAPI):
    logger.info(f"Connecting to Kafka Producer at {settings.KAFKA_BOOTSTRAP_SERVERS}...")

    while True:
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
            logger.warning(f"Connection attempt failed: {e}. Retrying in 5s...")
            await asyncio.sleep(5)


async def close_kafka(app: FastAPI):
    if hasattr(app.state, "kafka_producer"):
        logger.info("Stopping Kafka producer...")
        await app.state.kafka_producer.stop()
