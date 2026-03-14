from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    EMBED_MODEL: str
    NUMBER_CLUSTERS: int

    model_config = ConfigDict(env_file=".env")


settings = Settings()
print(settings.EMBED_MODEL)