import logging
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}


class Settings(BaseSettings):
    # App
    HOST: str
    PORT: int
    APP_URL: str
    # Postgres
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URI_ASYNC: Optional[AsyncPostgresDsn] = None

    # Redis
    REDIS_URL: RedisDsn

    # Deployment
    IS_LOCAL: bool

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("SQLALCHEMY_DATABASE_URI_ASYNC", pre=True)
    def assemble_async_db_connection(
        cls, v: Optional[str], values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type:ignore


logging.basicConfig(
    level=logging.INFO,
    filename="./logs/logfile.log",
    format="%(asctime)s.%(msecs)03d %(levelname)s %(thread)d - %(message)s",
)
logging.info("Start server running")
