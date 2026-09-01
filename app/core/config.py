from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Document Q&A Assistant"
    app_version: str = "0.1.0"
    environment: str = "development"

    gemini_api_key: str = Field(
        default="",
        validation_alias="GEMINI_API_KEY",
    )

    chunk_size: int = Field(
        default=500,
        validation_alias="CHUNK_SIZE",
    )

    chunk_overlap: int = Field(
        default=50,
        validation_alias="CHUNK_OVERLAP",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()