from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env"
        )
    
    MODEL_NAME: str
    OLLAMA_URL: str
    DB_URL: str


settings = Settings()
