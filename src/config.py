from typing import Any
from enum import Enum
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    This class defines the settings for the app
    """
    #  DB Related
    DEBUG: int
    ENVIRONMENT_AREA: str
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str
    SQL_HOST: str
    SQL_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_ENGINE: str
    DATABASE: str

    #  Redis Related
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    # AI Related
    MODEL_NAME: str

    ASYNC_DATABASE_URI: PostgresDsn | str = ""
    ASYNC_TEST_DATABASE_URI: PostgresDsn | str = ""

    @field_validator("ASYNC_DATABASE_URI", mode="after")
    def assemble_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            if v == "":
                return PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=info.data["POSTGRES_USER"],
                    password=info.data["POSTGRES_PASSWORD"],
                    host=info.data["SQL_HOST"],
                    port=info.data["SQL_PORT"],
                    path=info.data["POSTGRES_DB"],
                )
        return v

    @field_validator("ASYNC_TEST_DATABASE_URI", mode="after")
    def assemble_test_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            if v == "":
                return PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=info.data["POSTGRES_USER"],
                    password=info.data["POSTGRES_PASSWORD"],
                    host=info.data["SQL_HOST"],
                    port=info.data["SQL_PORT"],
                    path=info.data["POSTGRES_TEST_DB"],
                )
        return v

    # hardcoded `env/.env.dev` for dev instance
    model_config = SettingsConfigDict(env_file="env/.env.dev", extra="ignore")


settings = Settings()
