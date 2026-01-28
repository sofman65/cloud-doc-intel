from app.services.database.dynamodb_service import get_document_by_id
from app.services.storage.s3_service import generate_presigned_download_url


def get_document_download_url(document_id: str) -> str | None:
    doc = get_document_by_id(document_id)
    if not doc:
        return None

    # Do not allow downloads for deleted docs
    if doc.get("status") == "DELETED":
        return None

    return generate_presigned_download_url(
        bucket=doc["s3_bucket"],
        key=doc["s3_key"],
        expires_in_seconds=300,
    )
