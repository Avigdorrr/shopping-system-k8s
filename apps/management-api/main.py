import asyncio
import os
import sys

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from routers.v1 import v1_router
from routers.ops import ops_router
from infra.database import init_mongo, close_mongo
from infra.kafka import init_kafka, close_kafka
from core.logger import get_logger

logger = get_logger("management-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifecycle of infrastructure connections.
    """
    logger.info("Application is starting up")
    asyncio.create_task(init_kafka(app)) # Runs the Consumer infinite loop. Must be a task to avoid blocking the API.
    asyncio.create_task(init_mongo(app)) # Initialized in parallel to speed up startup time.

    yield

    logger.info("Application is shutting down")
    # Close connections
    await close_kafka(app)
    await close_mongo(app)


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router) # App logic routes
app.include_router(ops_router) # Liveness/Readiness probes


def main():
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)


if __name__ == "__main__":
    main()
