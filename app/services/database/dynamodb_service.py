from __future__ import annotations

from datetime import datetime, timezone

import boto3
from botocore.client import BaseClient
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

    response = dynamodb.get_item(
        TableName=settings.dynamodb_table_name,
        Key={"document_id": {"S": document_id}},
    )

    item = response.get("Item")
    if not item:
        return None

    # status is optional for older items
    status = item.get("status", {}).get("S", "ACTIVE")

    return {
        "document_id": item["document_id"]["S"],
        "filename": item["filename"]["S"],
        "s3_bucket": item["s3_bucket"]["S"],
        "s3_key": item["s3_key"]["S"],
        "content_type": item.get("content_type", {}).get("S"),
        "created_at": item["created_at"]["S"],
        "status": status,
        "deleted_at": item.get("deleted_at", {}).get("S"),
    }


def mark_deleting(document_id: str) -> None:
    dynamodb = get_dynamodb_client()

    dynamodb.update_item(
        TableName=settings.dynamodb_table_name,
        Key={"document_id": {"S": document_id}},
        # If item exists and is not already DELETED, allow transition to DELETING
        UpdateExpression="SET #st = :deleting",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={
            ":deleting": {"S": "DELETING"},
            ":deleted": {"S": "DELETED"},
        },
        ConditionExpression="attribute_exists(document_id) AND (attribute_not_exists(#st) OR #st <> :deleted)",
    )


def rollback_to_active(document_id: str) -> None:
    dynamodb = get_dynamodb_client()

    dynamodb.update_item(
        TableName=settings.dynamodb_table_name,
        Key={"document_id": {"S": document_id}},
        UpdateExpression="SET #st = :active REMOVE deleted_at",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={":active": {"S": "ACTIVE"}},
    )


def mark_deleted(document_id: str) -> None:
    dynamodb = get_dynamodb_client()
    now = datetime.now(timezone.utc).isoformat()

    dynamodb.update_item(
        TableName=settings.dynamodb_table_name,
        Key={"document_id": {"S": document_id}},
        UpdateExpression="SET #st = :deleted, deleted_at = :ts",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={
            ":deleted": {"S": "DELETED"},
            ":ts": {"S": now},
        },
    )
