from fastapi import APIRouter, Request, status, HTTPException

router = APIRouter(tags=["Operations"])

@router.get("/healthy")
async def liveness_probe():
    return {"status": "alive"}

@router.get("/ready")
async def readiness_probe(request: Request):
    # בדיקה פשוטה: האם הפרודוסר קיים בזיכרון?
    if not hasattr(request.app.state, "kafka_producer"):
        # אם לא - זרוק 503 מיד. קוברנטיס יבין לבד שזה לא מוכן.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kafka not connected"
        )
    return {"status": "ready"}