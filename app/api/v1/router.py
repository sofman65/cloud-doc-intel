from fastapi import APIRouter
from app.api.v1.routes import health
from app.api.v1.routes import scalar
from app.api.v1.routes import upload

api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="",
)

api_router.include_router(
    scalar.router,
    prefix="",
)

api_router.include_router(
    upload.router,
    prefix="",
)
