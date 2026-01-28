from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env.local"


class Settings(BaseSettings):
    # App
    app_name: str = "cloud-doc-intel"
    app_env: str = "local"  # local | dev | prod
    log_level: str = "INFO"

    # AWS
    aws_region: str = "eu-east-1"

    # Storage
    s3_bucket_name: str = "cloud-doc-intel-dev"
    s3_prefix: str = "documents/"

    # Database
    dynamodb_table_name: str = "documents-dev"

    # Features
    enable_ai: bool = False
    enable_auth: bool = False

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_ignore_empty=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
