from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from research_copilot import __version__


class Settings(BaseSettings):
    app_name: str = "ai-research-copilot"
    app_version: str = __version__
    app_env: str = "development"
    log_level: str = "INFO"
    data_dir: Path = Path("data")
    api_base_url: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
