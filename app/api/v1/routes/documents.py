from fastapi import APIRouter, Query, HTTPException, status
from botocore.exceptions import ClientError
from app.services.database.dynamodb_service import list_documents, get_document_by_id
from app.services.document_service import delete_document
from app.services.download_service import get_document_download_url


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


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document_endpoint(document_id: str):
    try:
        existed = delete_document(document_id)
    except ClientError:
        # surface a clean API error; log e in real app
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to delete document from AWS",
        )

    if not existed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # 204 = success with no body
    return


@router.get("/documents/{document_id}/download")
def download_document(document_id: str):
    url = get_document_download_url(document_id)

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or not available for download",
        )

    return {
        "download_url": url,
        "expires_in_seconds": 300,
    }
