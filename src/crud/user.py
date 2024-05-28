import typing
from uuid import UUID

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.cache.redis import async_redis
from src.crud.base import BaseCRUDInterface
from src.models.user import User
from src.schemas.routes.user import UserInCreateType, UserInLoginType, UserInUpdateType
from src.securities.hashing.password import pwd_generator
from src.securities.verifications.credentials import credential_verifier
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from src.utilities.exceptions.password import PasswordDoesNotMatch


class UserCRUDInterface(BaseCRUDInterface):
    async def create_user(self, user_create: UserInCreateType) -> User:
        new_user = User(username=user_create.username, email=user_create.email, is_logged_in=True)

        new_user.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        new_user.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=new_user.hash_salt, new_password=user_create.password
            )
        )

        self.async_session.add(instance=new_user)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_user)

        await async_redis.set(f"user:{new_user.id}", new_user.__dict__)

        return new_user

    async def read_users(self) -> typing.Sequence[User]:
        stmt = sqlalchemy.select(User)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_user_by_id(self, pk: UUID) -> User:
        cache_key = f"user:{pk}"
        cached_user = await async_redis.get(cache_key)
        if cached_user:
            return User(**cached_user)

        stmt = sqlalchemy.select(User).where(User.id == pk)
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist("User with id `{id}` does not exist!")

        await async_redis.set(cache_key, db_user.__dict__)
        return db_user

    async def read_user_by_username(self, username: str) -> User:
        cache_key = f"user:username:{username}"
        cached_user = await async_redis.get(cache_key)
        if cached_user:
            return User(**cached_user)

        stmt = sqlalchemy.select(User).where(User.username == username)
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist("User with username `{username}` does not exist!")

        await async_redis.set(cache_key, db_user.__dict__)
        return db_user

    async def read_user_by_email(self, email: str) -> User:
        cache_key = f"user:email:{email}"
        cached_user = await async_redis.get(cache_key)
        if cached_user:
            return User(**cached_user)

        stmt = sqlalchemy.select(User).where(User.email == email)
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist("User with email `{email}` does not exist!")

        await async_redis.set(cache_key, db_user.__dict__)
        return db_user

    async def read_user_by_password_authentication(self, user_login: UserInLoginType) -> User:
        stmt = sqlalchemy.select(User).where(User.email == user_login.email)
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist("Wrong username or wrong email!")

        if not pwd_generator.is_password_authenticated(
            hash_salt=db_user.hash_salt, password=user_login.password, hashed_password=db_user.hashed_password
        ):
            raise PasswordDoesNotMatch("Password does not match!")

        return db_user  # type: ignore

    async def update_user_by_id(self, pk: UUID, user_update: UserInUpdateType) -> User:
        new_user_data = user_update.dict()

        select_stmt = sqlalchemy.select(User).where(User.id == pk)
        query = await self.async_session.execute(statement=select_stmt)
        update_user = query.scalar()

        if not update_user:
            raise EntityDoesNotExist(f"User with id `{pk}` does not exist!")  # type: ignore

        update_stmt = (
            sqlalchemy.update(table=User)
            .where(User.id == update_user.id)
            .values(updated_at=sqlalchemy_functions.now())
        )

        if new_user_data["username"]:
            update_stmt = update_stmt.values(username=new_user_data["username"])

        if new_user_data["email"]:
            update_stmt = update_stmt.values(username=new_user_data["email"])

        if new_user_data["password"]:
            update_user.set_hash_salt(hash_salt=pwd_generator.generate_salt)
            update_user.set_hashed_password(
                hashed_password=pwd_generator.generate_hashed_password(
                    hash_salt=update_user.hash_salt, new_password=new_user_data["password"]
                )
            )

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_user)

        await async_redis.set(f"user:{update_user.id}", update_user.__dict__)

        return update_user

    async def delete_user_by_id(self, pk: UUID) -> str:
        select_stmt = sqlalchemy.select(User).where(User.id == pk)
        query = await self.async_session.execute(statement=select_stmt)
        delete_user = query.scalar()

        if not delete_user:
            raise EntityDoesNotExist(f"User with id `{pk}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=User).where(User.id == delete_user.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        await async_redis.delete(f"user:{pk}")
        await async_redis.delete(f"user:username:{delete_user.username}")
        await async_redis.delete(f"user:email:{delete_user.email}")

        return f"User with id '{pk}' is successfully deleted!"

    async def is_username_taken(self, username: str) -> bool:
        username_stmt = sqlalchemy.select(User.username).select_from(User).where(User.username == username)
        username_query = await self.async_session.execute(username_stmt)
        db_username = username_query.scalar()

        if not credential_verifier.is_username_available(username=db_username):
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")  # type: ignore

        return True

    async def is_email_taken(self, email: str) -> bool:
        email_stmt = sqlalchemy.select(User.email).select_from(User).where(User.email == email)
        email_query = await self.async_session.execute(email_stmt)
        db_email = email_query.scalar()

        if not credential_verifier.is_email_available(email=db_email):
            raise EntityAlreadyExists(f"The email `{email}` is already registered!")  # type: ignore

        return True
