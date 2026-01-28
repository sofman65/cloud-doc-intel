from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

import boto3
from botocore.client import BaseClient
from fastapi import UploadFile

from app.core.config import get_settings

settings = get_settings()


@dataclass(frozen=True)
class S3UploadResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    content_type: Optional[str] = None
    original_filename: Optional[str] = None


def get_s3_client() -> BaseClient:
    # Credentials are resolved automatically:
    # - local: AWS_PROFILE / aws configure
    # - AWS: IAM role (Lambda execution role)
    return boto3.client("s3", region_name=settings.aws_region)


def build_object_key(filename: str) -> str:
    safe_name = filename.strip().replace("/", "_")
    return f"{settings.s3_prefix}{uuid4()}-{safe_name}"


async def upload_to_s3(file: UploadFile, *, key: str | None = None) -> S3UploadResult:
    """
    Upload a FastAPI UploadFile to S3 using streaming (no full read into memory).
    """
    if not file.filename:
        raise ValueError("Missing filename")

    s3 = get_s3_client()
    object_key = key or build_object_key(file.filename)

    extra_args = {}
    if file.content_type:
        extra_args["ContentType"] = file.content_type

    # UploadFile.file is a SpooledTemporaryFile (file-like object).
    # upload_fileobj streams it to S3 efficiently.
    file.file.seek(0)
    s3.upload_fileobj(
        Fileobj=file.file,
        Bucket=settings.s3_bucket_name,
        Key=object_key,
        ExtraArgs=extra_args or None,
    )

    # Optional: fetch ETag (S3 doesn't return it from upload_fileobj directly)
    head = s3.head_object(Bucket=settings.s3_bucket_name, Key=object_key)

    return S3UploadResult(
        bucket=settings.s3_bucket_name,
        key=object_key,
        etag=head.get("ETag"),
        content_type=file.content_type,
        original_filename=file.filename,
    )
