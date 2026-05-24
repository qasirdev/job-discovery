from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field
from uuid import UUID

class Settings(BaseSettings):
    # Core settings
    next_public_api_url: str = "/api/v1"
    single_user_id: UUID = UUID("00000000-0000-0000-0000-000000000000")
    
    # DB settings (MVP 2+)
    database_url: PostgresDsn
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None
    
    # Auth & Redis
    secret_key: str = "super-secret-key-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    redis_url: str = "redis://localhost:6379"
    
    # LLM & External
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    litellm_api_base: str | None = None
    agent_router_token: str | None = None
    
    # Services (MVP 2+)
    temporal_server_url: str | None = None
    
    # Observability (MVP 3)
    otel_exporter_otlp_endpoint: str | None = None
    sentry_dsn: str | None = None

    model_config = {"env_file": ".env", "extra": "allow"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

type AppSettings = Annotated[Settings, Depends(get_settings)]
