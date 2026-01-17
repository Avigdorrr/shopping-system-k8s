from fastapi import APIRouter, Request, status, HTTPException

router = APIRouter(tags=["Operations"])

@router.get("/healthy")
async def liveness_probe():
    """Returns 200 OK to indicate the container is running."""
    return {"status": "alive"}

@router.get("/ready")
async def readiness_probe(request: Request):
    """
    Checks dependency health (Kafka).
    Returns 503 to stop traffic if the producer isn't connected yet.
    """
    if not hasattr(request.app.state, "kafka_producer"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kafka not connected"
        )
    return {"status": "ready"}