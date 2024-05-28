import logging
import os
import pathlib
from enum import Enum

from dotenv import load_dotenv
from pydantic import BaseConfig
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
ENV_FILE_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE_PATH)


class Environment(str, Enum):
    TEST: str = "TEST"
    PROD: str = "PROD"


class Settings(BaseSettings):
    TITLE: str = "EXO AUTH"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = True

    BACKEND_SERVER_HOST: str = os.getenv("BACKEND_SERVER_HOST", "127.0.0.1")
    BACKEND_SERVER_PORT: int = int(os.getenv("BACKEND_SERVER_PORT", 8002))
    BACKEND_SERVER_WORKERS: int = int(os.getenv("BACKEND_SERVER_WORKERS", 5))
    API_PREFIX: str = ""
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/swagger"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    DB_POSTGRES_NAME: str = os.getenv("DB_POSTGRES_NAME")
    DB_POSTGRES_PASSWORD: str = os.getenv("DB_POSTGRES_PASSWORD")
    DB_POSTGRES_HOST: str = os.getenv("DB_POSTGRES_HOST")
    DB_POSTGRES_PORT: int = int(os.getenv("DB_POSTGRES_PORT", 5432))
    DB_POSTGRES_SCHEMA: str = os.getenv("DB_POSTGRES_SCHEMA", "postgresql+psycopg2")
    DB_POSTGRES_USERNAME: str = os.getenv("DB_POSTGRES_USERNAME")
    DB_MAX_POOL_CON: int = int(os.getenv("DB_MAX_POOL_CON", 0))
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", 0))
    DB_POOL_OVERFLOW: int = int(os.getenv("DB_POOL_OVERFLOW", 0))
    DB_TIMEOUT: int = int(os.getenv("DB_TIMEOUT", 0))

    IS_DB_ECHO_LOG: bool = os.getenv("IS_DB_ECHO_LOG", "false").lower() in ["true", "1", "t"]
    IS_DB_FORCE_ROLLBACK: bool = os.getenv("IS_DB_FORCE_ROLLBACK", "false").lower() in ["true", "1", "t"]
    IS_DB_EXPIRE_ON_COMMIT: bool = os.getenv("IS_DB_EXPIRE_ON_COMMIT", "false").lower() in ["true", "1", "t"]

    HASHING_ALGORITHM_LAYER_1: str = os.getenv("HASHING_ALGORITHM_LAYER_1")
    HASHING_ALGORITHM_LAYER_2: str = os.getenv("HASHING_ALGORITHM_LAYER_2")
    HASHING_SALT: str = os.getenv("HASHING_SALT")

    JWT_SUBJECT: str = os.getenv("JWT_SUBJECT")
    JWT_TOKEN_PREFIX: str = os.getenv("JWT_TOKEN_PREFIX")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_SECRET_KEY_ACCESS_TOKEN: str = os.getenv("JWT_SECRET_KEY_ACCESS_TOKEN")
    JWT_SECRET_KEY_REFRESH_TOKEN: str = os.getenv("JWT_SECRET_KEY_REFRESH_TOKEN")
    JWT_ACCESS_TOKEN_EXPIRATION_TIME_MIN: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRATION_TIME_MIN", 180))
    JWT_REFRESH_TOKEN_EXPIRATION_TIME_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRATION_TIME_DAYS", 30))

    IS_ALLOWED_CREDENTIALS: bool = os.getenv("IS_ALLOWED_CREDENTIALS", "false").lower() in ["true", "1", "t"]
    ALLOWED_ORIGINS: list[str] = [
        # List remains unchanged
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    REDIS_SCHEMA: str = os.getenv("REDIS_SCHEMA", "redis")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: str = os.getenv("REDIS_DB")
    REDIS_POOL_MIN_SIZE: int = int(os.getenv("REDIS_POOL_MIN_SIZE", 5))
    REDIS_POOL_MAX_SIZE: int = int(os.getenv("REDIS_POOL_MAX_SIZE", 10))
    REDIS_CACHE_EXPIRE: int = int(os.getenv("REDIS_CACHE_EXPIRE", 3600))
    REDIS_TIMEOUT: int = int(os.getenv("REDIS_TIMEOUT", 5))

    class Config(BaseConfig):
        extra = "ignore"
        case_sensitive: bool = True
        env_file: str = str(ENV_FILE_PATH)
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
