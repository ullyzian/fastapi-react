import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request

from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.users import users_router
from app.core import config
from app.core.auth import get_current_active_user
from app.db.session import SessionLocal

app = FastAPI(
    title=config.PROJECT_NAME, redoc_url="/api/docs", openapi_url="/api"
)


def redoc_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Test api",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])

app.openapi = redoc_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
