"""
Application Configuration
Uses pydantic-settings for environment variable management
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application Info
    APP_NAME: str = "SchemaGenius AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    # Database
    DATABASE_URL: str
    SANDBOX_DATABASE_URL: str

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = ""
    FIREBASE_CREDENTIALS_JSON: str = ""

    # Gemini AI
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # Security
    SECRET_KEY: str

    # Sandbox Settings
    SANDBOX_MAX_EXECUTION_TIME_SECONDS: int = 30
    SANDBOX_MAX_QUERY_LENGTH: int = 10000
    SANDBOX_MAX_TABLES_PER_SESSION: int = 50

    # Rate Limiting
    AI_GENERATION_RATE_LIMIT: int = 10
    API_RATE_LIMIT: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
