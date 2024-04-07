from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """configuration settings for the API"""
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_prefix": "EDUAPI_",
    }

    database_url: str = "sqlite+aiosqlite:///database.db"
    access_token_secret_key: str = "ogiZtn79TWzwL7lMnDoxhw9MzCkH8VkI"
    access_token_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60
    bot_token: str
    tg_storage_chat_id: str


@lru_cache
def get_settings() -> Settings:
    """global cached settings for the API. Can be used as dependency"""

    return Settings()  # type: ignore
