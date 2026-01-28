from fastapi import APIRouter, Query, HTTPException, status
from app.services.database.dynamodb_service import list_documents, get_document_by_id

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


@router.get("/documents/{document_id}")
def get_document(document_id: str):
    document = get_document_by_id(document_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document
