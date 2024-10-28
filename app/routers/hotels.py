from fastapi import HTTPException

from app.routers import router, hotel_repository


@router.get("/hotels")
async def get_hotels():
    try:
        return await hotel_repository.get_all_hotels()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
