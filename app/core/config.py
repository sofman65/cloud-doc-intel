from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "cloud-doc-intel"
    app_env: str = "local"  # local | dev | prod
    log_level: str = "INFO"

    # AWS
    aws_region: str = "eu-west-1"

    # Storage
    s3_bucket_name: str = "cloud-doc-intel-dev"
    s3_prefix: str = "documents/"

    # Database
    dynamodb_table_name: str = "Dynamo"

    # Features
    enable_ai: bool = False
    enable_auth: bool = False

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_ignore_empty=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
