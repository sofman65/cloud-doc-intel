from uuid import uuid4
from fastapi import UploadFile


async def upload_service(file: UploadFile) -> dict:
    """
    Orchestrates document upload.

    This will later:
    - store file in S3
    - persist metadata in DynamoDB
    """

    document_id = str(uuid4())

    # placeholder for now
    return {
        "document_id": document_id,
    }
