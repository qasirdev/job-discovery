from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # LLM providers
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    litellm_api_base: str | None = None
    
    # DB & Services (MVP 2+)
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    database_url: str | None = None
    redis_url: str | None = "redis://localhost:6379"
    temporal_server_url: str | None = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

type AppSettings = Annotated[Settings, Depends(get_settings)]
