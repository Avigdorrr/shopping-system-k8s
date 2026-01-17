import asyncio

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from routers.v1 import v1_router
from routers.ops import ops_router
from infra.kafka import init_kafka, close_kafka
from core.logger import get_logger

logger = get_logger("management-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting up")
    asyncio.create_task(init_kafka(app))

    yield

    logger.info("Application is shutting down")
    await close_kafka(app)


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)
app.include_router(ops_router)


def main():
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)


if __name__ == "__main__":
    main()
