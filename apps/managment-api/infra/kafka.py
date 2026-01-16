import asyncio
import json
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

async def consume_loop(app: FastAPI):
    consumer = app.state.kafka_consumer
    collection = app.state.collection
    
    logger.info("Starting consumer loop...")
    try:
        async for msg in consumer:
            try:
                purchase_data = msg.value
                logger.info(f"Processing event for user: {purchase_data.get('username')}")
                
                await collection.insert_one(purchase_data)
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                
    except asyncio.CancelledError:
        logger.info("Consumer loop cancelled")
    except Exception as e:
        logger.error(f"Critical error in consumer loop: {e}")

async def init_kafka(app: FastAPI):
    logger.info(f"Connecting to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}...")
    
    for i in range(1, 6):
        try:
            consumer = AIOKafkaConsumer(
                settings.KAFKA_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=settings.KAFKA_GROUP_ID,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='earliest'
            )
            await consumer.start()
            
            app.state.kafka_consumer = consumer
            logger.info("Kafka connected successfully")
            
            app.state.consumer_task = asyncio.create_task(consume_loop(app))
            return
            
        except Exception as e:
            logger.warning(f"Connection attempt {i}/5 failed. Retrying in 5s...")
            await asyncio.sleep(5)
            
    logger.error("Could not connect to Kafka after retries")
    raise Exception("Kafka connection failed")

async def close_kafka(app: FastAPI):
    
    if hasattr(app.state, "consumer_task"):
        app.state.consumer_task.cancel()
        
    if hasattr(app.state, "kafka_consumer"):
        logger.info("Stopping Kafka consumer...")
        await app.state.kafka_consumer.stop()