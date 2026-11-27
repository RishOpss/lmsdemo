from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str
    SQL_ECHO: bool = True

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore[call-arg]