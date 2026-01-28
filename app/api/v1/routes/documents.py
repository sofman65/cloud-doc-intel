from fastapi import APIRouter, Query
from app.services.database.dynamodb_service import list_documents

router = APIRouter(tags=["documents"])


@router.get("/documents")
def get_documents(
    limit: int = Query(20, ge=1, le=100),
):
    documents = list_documents(limit=limit)

    return {
        "count": len(documents),
        "items": documents,
    }
