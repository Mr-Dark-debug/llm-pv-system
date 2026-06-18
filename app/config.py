"""Environment-driven configuration for the LEI/PVA system."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables.

    Args:
        None.

    Returns:
        None.

    Raises:
        pydantic.ValidationError: If environment values cannot be parsed.
    """

    app_name: str = "LLMs as Linguistic Input Evaluation"
    database_url: str = "sqlite:///./lei_evaluation.db"
    debug: bool = False
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    groq_api_key: str | None = None
    openrouter_api_key: str | None = None
    ollama_base_url: str = "http://localhost:11434"
    mock_llm_when_unconfigured: bool = True
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings.

    Args:
        None.

    Returns:
        Settings: Parsed runtime settings.

    Raises:
        pydantic.ValidationError: If settings are invalid.
    """

    return Settings()
