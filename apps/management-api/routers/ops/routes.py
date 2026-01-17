from fastapi import APIRouter, Request, status, HTTPException

router = APIRouter(tags=["Operations"])


@router.get("/healthy")
async def liveness_probe():
    """Returns 200 OK to indicate the container is running."""
    return {"status": "alive"}


@router.get("/ready")
async def readiness_probe(request: Request):
    """
    Checks dependency health (Kafka and MongoDB) to determine if the container is ready.).
    Returns 503 to stop traffic if a dependency is missing.
    """
    mongo_connected = hasattr(request.app.state, "mongo_client")
    kafka_connected = hasattr(request.app.state, "kafka_consumer")

    if not mongo_connected or not kafka_connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "mongo": "up" if mongo_connected else "down",
                "kafka": "up" if kafka_connected else "down"
            }
        )

    return {"status": "ready", "mongo": "up", "kafka": "up"}
