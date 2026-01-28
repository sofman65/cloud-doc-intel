from uuid import uuid4
from fastapi import UploadFile

from app.services.storage.s3_service import upload_to_s3


async def upload_service(file: UploadFile) -> dict:
    """
    Orchestrates document upload.

    This will later:
    - store file in S3
    - persist metadata in DynamoDB
    """

    document_id = str(uuid4())

    s3_result = await upload_to_s3(file)

    return {
        "document_id": document_id,
        "s3_bucket": s3_result.bucket,
        "s3_key": s3_result.key,
    }
