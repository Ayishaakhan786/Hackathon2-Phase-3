from pydantic_settings import SettingsConfigDict, BaseSettings
import os
from typing import Optional
from decouple import config
import re


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str = config('DATABASE_URL', default='postgresql://user:password@localhost/dbname')
    API_HOST: str = config('API_HOST', default='0.0.0.0')
    API_PORT: int = config('API_PORT', cast=int, default=8000)
    DEBUG: bool = config('DEBUG', cast=bool, default=False)
    LOG_LEVEL: str = config('LOG_LEVEL', default='info')

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Better Auth settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    DATABASE_URL_BETTER_AUTH: str = os.getenv("DATABASE_URL_BETTER_AUTH", "")

    model_config = SettingsConfigDict(env_file=".env")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Validation
        if not self.DATABASE_URL or self.DATABASE_URL == 'postgresql://user:password@localhost/dbname':
            raise ValueError("DATABASE_URL environment variable is required")

        # Validate DATABASE_URL format (should be a valid PostgreSQL connection string)
        if not re.match(r'^postgresql(\+asyncpg)?://', self.DATABASE_URL):
            raise ValueError("DATABASE_URL must be a valid PostgreSQL connection string")

        # Validate API_PORT range (1024-65535)
        if not (1024 <= self.API_PORT <= 65535):
            raise ValueError("API_PORT must be between 1024 and 65535")

        # Additional validation for Neon PostgreSQL connection
        if 'neon.tech' not in self.DATABASE_URL:
            raise ValueError("DATABASE_URL must be a valid Neon PostgreSQL connection")


settings = Settings()