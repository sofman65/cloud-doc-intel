from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "env": settings.app_env,
    }
