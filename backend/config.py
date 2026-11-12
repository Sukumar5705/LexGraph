"""
Application configuration.

Loads settings from the project-root .env file.
No default secrets or credentials are hardcoded here.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )

    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model_name: str = ""

    embedding_provider: str = ""
    embedding_api_key: str = ""
    embedding_model_name: str = ""

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = ""
    neo4j_password: str = ""
    neo4j_database: str = "neo4j"

    vector_store_provider: str = ""
    vector_store_url: str = ""
    vector_store_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()