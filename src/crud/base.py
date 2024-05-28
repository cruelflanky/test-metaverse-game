import typing

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.manager import settings
from src.database.db import get_async_session
from src.schemas.jwt import JWTUser
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.http.exc_401 import http_401_token_credentials_request


class BaseCRUDInterface:
    def __init__(self, async_session: AsyncSession, authorization: str = Header(default=None)):
        self.async_session = async_session
        self.user_id = self.validate_access_token(authorization) if authorization else None

    def validate_access_token(self, authorization: str) -> str | None:
        if not authorization:
            return None

        prefix, token = authorization.split()
        if prefix.lower() != "bearer":
            raise http_401_token_credentials_request()

        jwt_user: JWTUser = jwt_generator.retrieve_details_from_token(
            token=token, secret_key=settings.JWT_SECRET_KEY_ACCESS_TOKEN
        )

        return jwt_user.user_id


def get_interface(
    interface_type: typing.Type[BaseCRUDInterface],
) -> typing.Callable[[AsyncSession], BaseCRUDInterface]:
    def _get_interface(
        async_session: AsyncSession = Depends(get_async_session), authorization: str = Header(default=None)
    ) -> BaseCRUDInterface:
        return interface_type(async_session=async_session, authorization=authorization)

    return _get_interface
