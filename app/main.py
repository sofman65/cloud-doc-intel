from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1.router import api_router

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.include_router(
    api_router,
    prefix="/api/v1",
)
