import redis.asyncio as redis
from pydantic import RedisDsn
from redis.client import ConnectionPool, Redis

from src.config.manager import settings

REDIS_URL = "{}://{}:{}".format(settings.REDIS_SCHEMA, settings.REDIS_HOST, settings.REDIS_PORT)


class AsyncRedis:
    def __init__(self):
        self.redis_url: RedisDsn = RedisDsn(url=REDIS_URL)
        self.redis: Redis | None = None
        self.pool: ConnectionPool | None = None

    def connect(self):
        self.redis = redis.from_url(
            self.redis_url.unicode_string(), encoding="utf-8", db=settings.REDIS_DB, decode_responses=True
        )
        self.pool = self.redis.connection_pool

    def disconnect(self):
        self.redis.close()
        self.pool.disconnect()

    async def get(self, key: str) -> str | None:
        async with self.redis as session:
            return await session.get(key)

    async def set(self, key: str, value: str | dict) -> None:
        async with self.redis as session:
            await session.set(key, value, ex=settings.REDIS_EXPIRATION_TIME)

    async def delete(self, key: str) -> None:
        async with self.redis as session:
            await session.delete(key)


async_redis: AsyncRedis = AsyncRedis()
