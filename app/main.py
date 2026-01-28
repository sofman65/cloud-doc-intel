from fastapi import FastAPI, HTTPException
from scalar_fastapi import get_scalar_api_reference
from app.core.config import get_settings

settings = get_settings()
app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok", "env": settings}


@app.get("/scalar_docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
