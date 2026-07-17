"""
Configuration settings for AlumniConnect.
"""
from dotenv import load_dotenv
load_dotenv()

import os
print("Loaded DB Host =", os.getenv("DATABASE_HOSTNAME"))

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # ===== Application =====
    APP_NAME: str = "AlumniConnect"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ===== Database =====
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int = 5432
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ===== JWT Authentication =====
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ===== CORS =====
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

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

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model_config = SettingsConfigDict(
    env_file=str(BASE_DIR / ".env"),
    env_file_encoding="utf-8",
    case_sensitive=True,
)



@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
