from typing import Dict
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.document_service import upload_service

router = APIRouter(tags=["documents"])


@router.post("upload", status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile = File(...)) -> Dict:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )

    result = await upload_service(file)

    return {
        "message": "Upload accepted",
        "document_id": result["document_id"],
        "filename": file.filename,
    }
