from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:post12345@localhost:5432/book_mgt"
    JWT_SECRET_KEY: str = "2ec2fecb89f4bfcddfbd5d0d9e9cae03"
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).parent.parent}/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

Config = Settings()