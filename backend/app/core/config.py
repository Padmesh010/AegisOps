import os
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.enums import EnvironmentType

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Core Environment Settings
    ENVIRONMENT: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)
    PROJECT_NAME: str = "AegisOps"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="SUPER_SECRET_AEGIS_OPS_KEY_CHANGE_ME_IN_PRODUCTION")
    
    # JWT Settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # Database Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "aegisops"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str) and v:
            return v
        data = info.data
        server = data.get("POSTGRES_SERVER")
        user = data.get("POSTGRES_USER")
        password = data.get("POSTGRES_PASSWORD")
        db = data.get("POSTGRES_DB")
        port = data.get("POSTGRES_PORT")
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_URL: Optional[str] = None

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str) and v:
            return v
        data = info.data
        host = data.get("REDIS_HOST")
        port = data.get("REDIS_PORT")
        db = data.get("REDIS_DB")
        password = data.get("REDIS_PASSWORD")
        auth = f":{password}@" if password else ""
        return f"redis://{auth}{host}:{port}/{db}"

    # CORS Allowed Hosts
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # AI Configurations
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Fallback configuration
    AI_FALLBACK_CHAIN: List[str] = ["groq", "openai", "ollama"]

# Dependency Injection helper
from functools import lru_cache
from typing import Any

@lru_cache()
def get_settings() -> Settings:
    return Settings()
