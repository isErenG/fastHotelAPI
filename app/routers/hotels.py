from app.routers import router

@router.get("/hotels")
async def get_hotels():
    return {"hotels": "hotels"}