from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


async def init_mongo(app: FastAPI):
    """
    Initializes MongoDB connection with a strict Retry Pattern.
    Uses an infinite loop to keep trying to connect until connection succeeds.
    Essential for Kubernetes/Docker environments where MongoDB might take longer to start than this service.
    """
    mongo_uri = f"mongodb://{settings.MONGO_HOSTNAME}:{settings.MONGO_PORT}/"
    logger.info(f"Connecting to MongoDB at {mongo_uri}...")

    while True:
        try:
            client = AsyncIOMotorClient(mongo_uri)

            # throws an exception if connection fails
            await client.server_info()

            app.state.mongo_client = client
            app.state.db = client[settings.MONGO_DB_NAME]
            app.state.collection = app.state.db[settings.MONGO_COLLECTION_NAME]

            logger.info("MongoDB connected successfully")
            return

        except Exception as e:
            logger.warning(f"Failed to connect to MongoDB: {e}. Retrying in 5 seconds...")


async def close_mongo(app: FastAPI):
    """ Close the mongo client """
    if hasattr(app.state, "mongo_client"):
        logger.info("Closing MongoDB connection...")
        app.state.mongo_client.close()
