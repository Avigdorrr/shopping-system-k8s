import time
import aiohttp
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel
from core.config import settings
from core.logger import get_logger

router = APIRouter(tags=["Buys"])
logger = get_logger("web-server-router")


class PurchaseRequest(BaseModel):
    username: str
    userid: str
    price: float


@router.post("/buy", status_code=status.HTTP_202_ACCEPTED)
async def buy_item(purchase: PurchaseRequest, request: Request):
    if not hasattr(request.app.state, "kafka_producer"):
        logger.error("Kafka producer is not initialized")
        raise HTTPException(status_code=503, detail="Service Unavailable")

    producer = request.app.state.kafka_producer

    try:
        purchase_data: dict = purchase.model_dump()
        purchase_data['timestamp'] = time.time()

        logger.info(f"Producing event: {purchase_data}")

        await producer.send_and_wait(
            topic=settings.KAFKA_TOPIC,
            value=purchase_data
        )

        return {
            "status": "success",
            "message": "Purchase recorded",
            "data": purchase_data
        }

    except Exception as e:
        logger.error(f"Failed to send to Kafka: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/getAllUserBuys/{userid}")
async def get_user_history(userid: str):
    target_url = f"http://{settings.MANAGEMENT_API_ENDPOINT}/api/v1/purchases/{userid}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url, timeout=5) as response:
                if response.status == 200:
                    return await response.json()
                if response.status == 404:
                    return []

                logger.error(f"Management API error: {response.status}")
                raise HTTPException(status_code=response.status, detail="Failed to fetch history")

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Proxy Error")
