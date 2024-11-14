from typing import Union

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.models.admin import Admin
from app.models.user import User
from app.utils.jwt_helper import get_current_user


class AdminOnlyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin"):
            try:
                current_user: Union[User, Admin] = await get_current_user(request=request)
                if not isinstance(current_user, Admin):
                    raise HTTPException(status_code=403, detail="Forbidden access")
            except HTTPException as e:
                return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        response = await call_next(request)
        return response
