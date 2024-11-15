from fastapi import Depends, HTTPException, status

from app.models.admin import Admin
from app.models.user import User
from app.utils.jwt_helper import get_current_user


async def admin_dependency(
        current_user: User | Admin = Depends(get_current_user)
) -> Admin:
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins are allowed to access this resource.",
        )
    return current_user
