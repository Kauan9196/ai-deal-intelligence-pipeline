import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str = "dummy_key_for_now"
    AMAZON_AFFILIATE_TAG: str = "my_amazon_tag-20"
    AWIN_NETWORK_ID: str = "123456"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
