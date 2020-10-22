from fastapi import APIRouter, Depends

from app.api.api_v1.endpoints import auth, users
from app.api.dependencies import get_current_active_user

api_router = APIRouter()
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
