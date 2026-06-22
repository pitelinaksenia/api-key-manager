from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/api_key_manager"
    app_name: str = "API Key Manager"
    debug: bool = True

    class Config:
        env_file =  ".env"


settings = Settings()