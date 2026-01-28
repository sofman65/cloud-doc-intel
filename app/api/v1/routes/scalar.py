from fastapi import APIRouter
from scalar_fastapi import get_scalar_api_reference

router = APIRouter()


@router.get("/scalar", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="Cloud Doc Intel API",
    )
