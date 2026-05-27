from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
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
    openrouter_api_key: str | None = None  # OpenRouter for gpt-oss-120b — Local LLM support (MVP 2+)
    agent_router_token: str | None = None
    
    # Services (MVP 2+)
    temporal_server_url: str | None = None

    # API Gateway (MVP 2+) — JD-103
    kong_admin_url: str | None = None
    kong_proxy_url: str | None = None

    # Proxy Abstraction Layer (MVP 2+) — JD-104
    # PROXY_POOL_URLS: comma-separated list of datacenter proxy URLs
    # e.g. "http://user:pass@proxy1.example.com:8080,http://user:pass@proxy2.example.com:8080"
    proxy_pool_urls: str | None = None
    # RESIDENTIAL_PROXY_URL: single residential proxy endpoint (opt-in, anti-bot escalation only)
    # e.g. "http://user:pass@residential.proxy.net:8080"
    residential_proxy_url: str | None = None

    # Observability (MVP 3)
    otel_exporter_otlp_endpoint: str | None = None
    sentry_dsn: str | None = None
    environment: str = "development"
    app_version: str = "1.0.0"

    # Agent Feature Flags (MVP 2+ JD-120)
    feature_linkedin_agent: bool = True
    feature_jobserve_agent: bool = True
    feature_ranking_agent: bool = True
    feature_rag_agent: bool = True
    feature_cover_letter_agent: bool = True
    feature_question_answer_agent: bool = True
    feature_security_agent: bool = True
    feature_orchestrator_agent: bool = True
    feature_quality_critic_agent: bool = True
    feature_observability_agent: bool = True
    feature_application_assistant_agent: bool = False  # Post-MVP 3
    feature_interview_prep_agent: bool = False  # Post-MVP 3

    # Agent Model Overrides (MVP 2+ JD-130)
    model_override_linkedin: str | None = None
    model_override_jobserve: str | None = None
    model_override_ranking: str | None = None
    model_override_rag: str | None = None
    model_override_cover_letter: str | None = None
    model_override_question_answer: str | None = None
    model_override_security: str | None = None
    model_override_orchestrator: str | None = None
    model_override_quality_critic: str | None = None
    model_override_application_assistant: str | None = None
    model_override_interview_prep: str | None = None


    model_config = {"env_file": ".env", "extra": "allow"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

type AppSettings = Annotated[Settings, Depends(get_settings)]
