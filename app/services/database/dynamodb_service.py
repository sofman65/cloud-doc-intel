from __future__ import annotations

from datetime import datetime, timezone

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from typing import List, Dict, Optional

from app.core.config import get_settings

settings = get_settings()


def get_dynamodb_client() -> BaseClient:
    return boto3.client("dynamodb", region_name=settings.aws_region)


def save_document_metadata(
    *,
    document_id: str,
    filename: str,
    s3_bucket: str,
    s3_key: str,
    content_type: str | None,
) -> None:
    dynamodb = get_dynamodb_client()

    dynamodb.put_item(
        TableName=settings.dynamodb_table_name,
        Item={
            "document_id": {"S": document_id},
            "filename": {"S": filename},
            "s3_bucket": {"S": s3_bucket},
            "s3_key": {"S": s3_key},
            "content_type": {"S": content_type or "unknown"},
            "created_at": {"S": datetime.now(timezone.utc).isoformat()},
        },
    )


def list_documents(limit: int = 20) -> List[Dict]:
    dynamodb = get_dynamodb_client()

    response = dynamodb.scan(
        TableName=settings.dynamodb_table_name,
        Limit=limit,
    )

    items = response.get("Items", [])

    # Convert DynamoDB AttributeValues → normal dict
    documents = []
    for item in items:
        documents.append(
            {
                "document_id": item["document_id"]["S"],
                "filename": item["filename"]["S"],
                "s3_bucket": item["s3_bucket"]["S"],
                "s3_key": item["s3_key"]["S"],
                "content_type": item.get("content_type", {}).get("S"),
                "created_at": item["created_at"]["S"],
            }
        )

    return documents


def get_document_by_id(document_id: str) -> Optional[Dict]:
    dynamodb = get_dynamodb_client()

    try:
        response = dynamodb.get_item(
            TableName=settings.dynamodb_table_name,
            Key={
                "document_id": {"S": document_id},
            },
        )
    except ClientError:
        raise

    item = response.get("Item")

    if not item:
        return None

    return {
        "document_id": item["document_id"]["S"],
        "filename": item["filename"]["S"],
        "s3_bucket": item["s3_bucket"]["S"],
        "s3_key": item["s3_key"]["S"],
        "content_type": item.get("content_type", {}).get("S"),
        "created_at": item["created_at"]["S"],
    }
