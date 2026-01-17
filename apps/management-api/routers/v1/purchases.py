from typing import List
from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel


class PurchaseResponse(BaseModel):
    userid: str
    username: str
    price: float
    timestamp: float


router = APIRouter(tags=["Purchases"])


@router.get("/purchases/{userid}", response_model=List[PurchaseResponse])
async def get_user_history(userid: str, request: Request):
    """
    Fetches purchase history directly from MongoDB.

    Behavior:
    - Returns 200 OK with the list of items found.
    - If no items are found, MongoDB returns an empty list [], not a 404 error.
    - Sort by _id descending to show the newest purchases first.
    """
    if not hasattr(request.app.state, "collection"):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database not initialized")

    collection = request.app.state.collection

    try:
        cursor = collection.find(
            {"userid": userid},
            {"_id": 0}
        )

        cursor.sort("_id", -1)

        items = await cursor.to_list(length=100) # won't fetch over 100 items. avoiding unnecessary load

        return items

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
