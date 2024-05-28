import typing

import fastapi

from src.cache.redis import async_redis
from src.database.events import dispose_db_connection, initialize_db_connection


def execute_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    async def launch_backend_server_events() -> None:
        async_redis.connect()
        await initialize_db_connection(backend_app=backend_app)

    return launch_backend_server_events


def terminate_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    async def stop_backend_server_events() -> None:
        async_redis.disconnect()
        await dispose_db_connection(backend_app=backend_app)

    return stop_backend_server_events
