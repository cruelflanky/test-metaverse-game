from typing import Sequence
from uuid import UUID

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.redis import async_redis
from src.crud.base import BaseCRUDInterface
from src.models.character import Character
from src.schemas.routes.character import CharacterCreateType
from src.utilities.exceptions.database import EntityDoesNotExist


class CharacterCRUDInterface(BaseCRUDInterface):
    async def create_character(self, character_create: CharacterCreateType) -> Character:
        new_character = Character(user_id=character_create.user_id, name=character_create.name)

        self.async_session.add(instance=new_character)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_character)

        return new_character

    async def read_characters(self) -> Sequence[Character]:
        stmt = sqlalchemy.select(Character)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_character_by_id(self, pk: UUID) -> Character:
        cache_key = f"character:{pk}"
        cached_character = await async_redis.get(cache_key)
        if cached_character:
            return Character(**cached_character)

        stmt = sqlalchemy.select(Character).where(Character.id == pk)
        query = await self.async_session.execute(statement=stmt)
        db_character = query.scalar()

        if not db_character:
            raise EntityDoesNotExist("Character with id `{id}` does not exist!")

        await async_redis.set(cache_key, db_character.__dict__)
        return db_character
