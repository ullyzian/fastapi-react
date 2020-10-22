import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request

from app.api.api_v1.routers import api_router
from app.core.config import settings
from app.core.database import SessionLocal

app = FastAPI(
    title=settings.PROJECT_NAME,
    redoc_url="/api/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


def redoc_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.API_V1_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = redoc_openapi


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


# Routers
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
