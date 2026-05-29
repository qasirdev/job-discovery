from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMSettings(BaseSettings):
    """LLM configuration settings for LiteLLM/OpenRouter."""
    OPENROUTER_API_KEY: str = "sk-or-mock-key"
    DEFAULT_MODEL: str = "openrouter/anthropic/claude-3-haiku"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.1

    #model_config = {"env_file": ".env", "extra": "ignore"}
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

llm_settings = LLMSettings()
