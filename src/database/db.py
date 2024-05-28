from typing import AsyncGenerator

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool, Pool

from src.config.manager import settings

DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    settings.DB_POSTGRES_SCHEMA,
    settings.DB_POSTGRES_USERNAME,
    settings.DB_POSTGRES_PASSWORD,
    settings.DB_POSTGRES_HOST,
    settings.DB_POSTGRES_PORT,
    settings.DB_POSTGRES_NAME,
)


class AsyncDatabase:
    def __init__(self):
        self.postgres_uri: PostgresDsn = PostgresDsn(url=DATABASE_URL)
        self.async_engine: AsyncEngine = create_async_engine(
            url=self.async_postgres_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=AsyncAdaptedQueuePool,
        )
        self.async_session = async_sessionmaker(bind=self.async_engine)
        self.pool: Pool = self.async_engine.pool

    @property
    def async_postgres_uri(self) -> str:
        return self.postgres_uri.unicode_string().replace(settings.DB_POSTGRES_SCHEMA, "postgresql+asyncpg")


async_db: AsyncDatabase = AsyncDatabase()


async def get_async_session() -> AsyncGenerator:
    async with async_db.async_session() as s:
        yield s
