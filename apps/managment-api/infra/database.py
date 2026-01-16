from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

async def init_mongo(app: FastAPI):
    logger.info(f"Connecting to MongoDB at {settings.MONGO_URI}...")
    
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        
        await client.server_info()
        
        app.state.mongo_client = client
        app.state.db = client[settings.MONGO_DB_NAME]
        app.state.collection = app.state.db[settings.MONGO_COLLECTION_NAME]
        
        logger.info("MongoDB connected successfully")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e

async def close_mongo(app: FastAPI):
    if hasattr(app.state, "mongo_client"):
        logger.info("Closing MongoDB connection...")
        app.state.mongo_client.close()