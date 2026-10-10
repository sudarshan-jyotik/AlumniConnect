"""
Configuration settings for AlumniConnect.
"""
from dotenv import load_dotenv
load_dotenv()

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Union
import json

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings."""

    # ===== Application =====
    APP_NAME: str = "AlumniConnect"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ===== Database =====
    DATABASE_URL: str | None = None
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = "alumniconnect"
    DATABASE_USERNAME: str = "postgres"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ===== JWT Authentication =====
    SECRET_KEY: str = "alumniconnect-default-secret-key-32-chars-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ===== CORS =====
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("CORS_ORIGINS")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # ===== Email (SMTP) =====
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "AlumniConnect"

    # ===== Redis (Optional - for future use) =====
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # ===== Logging =====
    LOG_LEVEL: str = "INFO"

    # ===== File Upload =====
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".doc", ".docx"]

    # ===== Rate Limiting =====
    RATE_LIMIT_ENABLED: bool = True

    # ===== Frontend URL =====
    FRONTEND_URL: str = "http://localhost:3000"

    # ===== Verification =====
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
