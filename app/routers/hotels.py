from fastapi import HTTPException

from app.routers import router


@router.get("/hotels")
async def get_hotels():
    try:
        return {}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
