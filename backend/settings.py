from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM providers
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    
    # Auth & Redis
    secret_key: str = "super-secret-key-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    redis_url: str = "redis://localhost:6379"

    # LLM & External
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    litellm_api_base: str | None = None
    
    # DB & Services (MVP 2+)
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    temporal_server_url: str | None = None
    
    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

type AppSettings = Annotated[Settings, Depends(get_settings)]
