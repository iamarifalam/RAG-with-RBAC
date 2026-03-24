from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Atlas RAG Assistant"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    token_ttl_minutes: int = 90
    jwt_secret: str = "change-me-in-production"
    llm_mode: str = "mock"
    openai_compatible_base_url: str = ""
    openai_compatible_api_key: str = ""
    openai_compatible_model: str = ""
    max_context_chunks: int = 4
    min_retrieval_score: float = 0.08
    allowed_topics: list[str] = Field(
        default_factory=lambda: ["finance", "hr", "marketing", "operations", "policy", "security"]
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

