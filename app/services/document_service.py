from uuid import uuid4
from fastapi import UploadFile
from botocore.exceptions import ClientError

from app.services.storage.s3_service import upload_to_s3
from app.services.database.dynamodb_service import (
    save_document_metadata,
    get_document_by_id,
    mark_deleting,
    mark_deleted,
    rollback_to_active,
)
from app.services.storage.s3_service import delete_from_s3


async def upload_service(file: UploadFile) -> dict:
    """
    Orchestrates document upload.

    This will later:
    - store file in S3
    - persist metadata in DynamoDB
    """

    document_id = str(uuid4())

    if not file.filename:
        raise ValueError("Filename is required")

    filename: str = file.filename

    s3_result = await upload_to_s3(file)

    save_document_metadata(
        document_id=document_id,
        filename=filename,
        s3_bucket=s3_result.bucket,
        s3_key=s3_result.key,
        content_type=file.content_type,
    )

    return {
        "document_id": document_id,
        "s3_bucket": s3_result.bucket,
        "s3_key": s3_result.key,
    }


def delete_document(document_id: str) -> bool:
    """
    Returns:
      True  -> document existed (deleted or already deleted)
      False -> document not found
    """
    doc = get_document_by_id(document_id)
    if not doc:
        return False

    # Idempotency: if already deleted, treat as success
    if doc.get("status") == "DELETED":
        return True

    # Phase 1: mark DELETING (coordination)
    try:
        mark_deleting(document_id)
    except ClientError:
        raise

    # Phase 2: delete S3 object
    try:
        delete_from_s3(bucket=doc["s3_bucket"], key=doc["s3_key"])
    except ClientError:
        # Rollback metadata so it stays usable
        rollback_to_active(document_id)
        raise

    # Phase 3: mark metadata DELETED
    try:
        mark_deleted(document_id)
    except ClientError:
        # At this point S3 is gone but Dynamo still exists.
        # We keep status as DELETING/whatever it currently is and fail loudly,
        # so you can retry deletion later.
        raise

    return True
