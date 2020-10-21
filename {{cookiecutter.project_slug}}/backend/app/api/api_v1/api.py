from fastapi import APIRouter, Depends

from app.api.api_v1.endpoints import auth, users
from app.core.auth import get_current_active_user

api_router = APIRouter()
api_router.include_router(
    users.router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
api_router.include_router(auth.router, prefix="/api", tags=["auth"])
