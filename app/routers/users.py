from app.routers import router

@router.get("/users")
async def get_users():
    return {"users": "user"}