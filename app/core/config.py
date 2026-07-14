from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    LOCAL = "local"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = ""
    app_name: str = "API Key Manager"
    debug: bool = True
    env: Environment = Environment.LOCAL


settings = Settings()
